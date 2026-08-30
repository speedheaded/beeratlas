# -*- coding: utf-8 -*-
"""
Извлечение линеек с сайтов пивоварен — уровень `official`.

    python scripts/fetch_lineups.py            # только пивоварни с пражской точкой
    python scripts/fetch_lineups.py --all      # все, у кого известен сайт
    python scripts/fetch_lineups.py --only svijany,unetice

Пишет data/lineups_raw.json — СЫРЬЁ ДЛЯ ВЫЧИТКИ, не каталог. В data/beers.json
ничего не попадает автоматически: каждое значение несёт исходную строку со
страницы и адрес, откуда взято, и подтверждается человеком.

Почему headless-браузер: у заметной части сайтов в HTML нет текста без JS
(проверено на bernard.cz — 726 символов и просьба включить JavaScript).

Ловушка, ради которой всё это писалось аккуратно: Svijany пишет СТЕПЕНЬ через
процент — «Svijanský Máz 11 %», а настоящий алкоголь стоит отдельной строкой
«Obsah alkoholu: 4,8 %». Наивный разбор записал бы 11 % ABV. Поэтому число
классифицируется по соседним словам, а спорное помечается needsReview.
"""
import json
import re
import subprocess
import sys
import html
import time
from datetime import date
from pathlib import Path
from urllib.parse import urljoin, urlparse

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TODAY = date.today().isoformat()

# сильный признак раздела линейки против слабого: слово «pivo» есть
# и в адресе отдельного сорта, а «naše piva» — только у раздела
LINEUP_STRONG = re.compile(r"(?i)(nase-?piva|nase_piva|/piva|sortiment|produkty|"
                           r"produkce|nabidka|our-beers|beers|vyrabime)")
LINEUP_WEAK = re.compile(r"(?i)(piv[ao]|beer)")
SKIP_LINK = re.compile(r"(?i)(eshop|e-shop|obchod|kosik|cart|facebook|instagram|youtube|"
                       r"\.pdf$|\.jpg$|\.png$|mailto:|tel:|/kontakt|/o-nas|/historie)")

PLATO_DEG = re.compile(r"(\d{1,2}(?:[.,]\d)?)\s*°")
ABV_LABEL = re.compile(r"(?i)(?:obsah\s+alkoholu|alkohol|alc\.?|abv)[^0-9]{0,12}(\d{1,2}[.,]\d{1,2})\s*%")
ABV_OBJ = re.compile(r"(\d{1,2}[.,]\d{1,2})\s*%\s*obj")
PCT_ANY = re.compile(r"(\d{1,2}(?:[.,]\d{1,2})?)\s*%")
NOISE = re.compile(r"(?i)(cookie|souhlas|přihlá|registr|copyright|všechna práva|menu|"
                   r"newsletter|odběr|mladistv|18 let)")


def render(url, budget=11000, tries=2):
    """DOM после исполнения JS. Простым запросом половина сайтов не берётся."""
    for _ in range(tries):
        try:
            out = subprocess.run(
                [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
                 "--virtual-time-budget=%d" % budget, "--dump-dom", url],
                capture_output=True, timeout=80)
            dom = out.stdout.decode("utf-8", "replace")
            if len(dom) > 500:
                return dom
        except Exception:
            pass
        time.sleep(1.5)
    return ""


def to_text(dom):
    dom = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", dom)
    dom = re.sub(r"(?s)<[^>]+>", "\n", dom)
    return html.unescape(dom)


def links(dom, base):
    out = []
    for href, label in re.findall(r'(?is)<a\b[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', dom):
        if SKIP_LINK.search(href):
            continue
        lab = re.sub(r"(?s)<[^>]+>", " ", label)
        lab = re.sub(r"\s+", " ", html.unescape(lab)).strip()
        out.append((urljoin(base, href), lab))
    return out


def same_host(a, b):
    return urlparse(a).netloc.replace("www.", "") == urlparse(b).netloc.replace("www.", "")


def classify(line):
    """(plato, abv, needsReview) для одной строки текста."""
    plato = abv = None
    review = False

    m = PLATO_DEG.search(line)
    if m:
        plato = m.group(1).replace(",", ".")

    m = ABV_LABEL.search(line) or ABV_OBJ.search(line)
    if m:
        abv = m.group(1).replace(",", ".")

    if abv is None:
        for raw in PCT_ANY.findall(line):
            val = float(raw.replace(",", "."))
            if "." in raw or "," in raw:
                if 2.0 <= val <= 14.0:      # десятичное с процентом — почти всегда алкоголь
                    abv = raw.replace(",", ".")
                    break
            elif plato is None and 7 <= val <= 20:
                # целое 7-20 с процентом в названии: у чехов это степень, а не алкоголь
                plato, review = raw, True
    return plato, abv, review


def beer_lines(text, url):
    found, seen = [], set()
    for raw in text.split("\n"):
        line = re.sub(r"\s+", " ", raw).strip()
        if not (8 <= len(line) <= 150) or NOISE.search(line):
            continue
        if "°" not in line and "%" not in line:
            continue
        plato, abv, review = classify(line)
        if plato is None and abv is None:
            continue
        name = PLATO_DEG.sub(" ", line)
        name = PCT_ANY.sub(" ", name)
        name = re.sub(r"(?i)\b(obj\.?|obsah alkoholu|alkohol|stupňovitost|alc\.?|abv)\b", " ", name)
        name = re.sub(r"\s{2,}", " ", name)
        name = re.sub(r"[\u2013\u2014-]\s*$", "", name).strip(" -\u2013\u2014:\u00b7|")
        if len(name) < 3 or len(name) > 70:
            name = ""
        key = (name.lower(), plato, abv)
        if key in seen:
            continue
        seen.add(key)
        found.append({"name": name, "plato": plato, "abv": abv,
                      "needsReview": review, "context": line[:140], "url": url})
    return found


H1 = re.compile(r"(?is)<h1[^>]*>(.*?)</h1>")
TITLE = re.compile(r"(?is)<title[^>]*>(.*?)</title>")


def page_record(dom, url):
    """Страница одного сорта: имя из заголовка, числа со всей страницы.

    На странице сорта алкоголь стоит отдельной строкой («Obsah alkoholu: 4,8 %»)
    и построчный разбор оставляет его без имени. Здесь имя даёт заголовок.
    """
    m = H1.search(dom) or TITLE.search(dom)
    if not m:
        return None
    head = re.sub(r"(?s)<[^>]+>", " ", m.group(1))
    head = re.sub(r"\s+", " ", html.unescape(head)).strip()
    head = re.split(r"\s*[|–—]\s*", head)[0].strip()
    if not (3 <= len(head) <= 90):
        return None

    text = to_text(dom)
    plato = abv = None
    review = False
    pm = PLATO_DEG.search(text)
    if pm:
        plato = pm.group(1).replace(",", ".")
    am = ABV_LABEL.search(text) or ABV_OBJ.search(text)
    if am:
        abv = am.group(1).replace(",", ".")
    if plato is None:
        p2, _, r2 = classify(head)
        if p2:
            plato, review = p2, r2
    if plato is None and abv is None:
        return None

    name = PCT_ANY.sub(" ", PLATO_DEG.sub(" ", head))
    name = re.sub(r"\s{2,}", " ", name).strip(" -–—:·|")
    if len(name) < 3:
        return None
    return {"name": name, "plato": plato, "abv": abv, "needsReview": review,
            "context": head[:140], "url": url}


def merge(beers):
    """Сводит записи об одном сорте: со списка приходит степень, со страницы — алкоголь."""
    out = {}
    order = []
    for x in beers:
        key = re.sub(r"[^a-z0-9]+", "", x["name"].lower()) or x["context"][:20].lower()
        if key not in out:
            out[key] = dict(x)
            order.append(key)
            continue
        cur = out[key]
        for f in ("plato", "abv"):
            if not cur.get(f) and x.get(f):
                cur[f] = x[f]
                if f == "abv":
                    cur["needsReview"] = cur["needsReview"] and not x["abv"]
        if len(x["name"]) > len(cur["name"]):
            cur["name"] = x["name"]
    return [out[k] for k in order]


def crawl(b, max_pages=22):
    """Обходит сайт пивоварни и собирает кандидатов в сорта.

    Раздел линейки не угадываем по словам в адресе — берём структуру: страницы
    сортов висят под общим родителем, и этот родитель собирает больше ссылок,
    чем любой другой раздел. У Svijany под /svijanske-pivo/ их тридцать, под
    /pivovar/ ни одной.
    """
    site = b["site"]
    home = render(site)
    if not home:
        return {"breweryId": b["id"], "brewery": b["name"], "site": site,
                "fetchedAt": TODAY, "error": "страница не отрисовалась",
                "pages": [], "beers": []}

    inside = [(u.split("#")[0], l) for u, l in links(home, site) if same_host(u, site)]
    groups = {}
    for u, l in inside:
        path = urlparse(u).path.rstrip("/")
        if not path or path.count("/") < 2:
            continue
        parent = path.rsplit("/", 1)[0]
        groups.setdefault(parent, []).append(u)

    def score(parent):
        hit = LINEUP_STRONG.search(parent) or LINEUP_WEAK.search(parent)
        return (0 if hit else 1, -len(set(groups[parent])))

    best = sorted(groups, key=score)[:1]
    urls = []
    if best and score(best[0])[0] == 0:
        parent = best[0]
        idx = urljoin(site, parent + "/")
        urls.append(idx)
        urls += sorted(set(groups[parent]))

    # запасной путь: раздел не опознан — берём ссылки с сильным признаком
    if len(urls) < 2:
        for u, l in inside:
            if LINEUP_STRONG.search(u) or LINEUP_STRONG.search(l):
                urls.append(u)

    pages, beers = [site], beer_lines(to_text(home), site)
    seen = {site}
    for u in urls[:max_pages]:
        if u in seen:
            continue
        seen.add(u)
        dom = render(u, 9000)
        if not dom:
            continue
        pages.append(u)
        rec = page_record(dom, u)
        if rec:
            beers.append(rec)
        beers += beer_lines(to_text(dom), u)

    out = merge(beers)
    # безымянная запись — это та же строка со страницы сорта, где имя дал
    # заголовок: если такое число уже есть у названного сорта, дубль убираем
    named = {(x["plato"], x["abv"], x["url"]) for x in out if x["name"]}
    out = [x for x in out if x["name"] or (x["plato"], x["abv"], x["url"]) not in named]

    return {"breweryId": b["id"], "brewery": b["name"], "site": site,
            "fetchedAt": TODAY, "pages": pages, "beers": out}


def main():
    br = json.loads((DATA / "breweries.json").read_text(encoding="utf-8"))
    ve = json.loads((DATA / "venues.json").read_text(encoding="utf-8"))
    cnt = {}
    for v in ve:
        for i in v.get("breweryIds", []):
            cnt[i] = cnt.get(i, 0) + 1

    only = None
    if "--only" in sys.argv:
        only = set(sys.argv[sys.argv.index("--only") + 1].split(","))
    targets = [b for b in br if b.get("site")]
    if only:
        targets = [b for b in targets if b["id"] in only]
    elif "--all" not in sys.argv:
        targets = [b for b in targets if cnt.get(b["id"])]
    targets.sort(key=lambda b: -cnt.get(b["id"], 0))

    out_path = DATA / "lineups_raw.json"
    print("целей: %d" % len(targets), flush=True)
    out = []
    for i, b in enumerate(targets, 1):
        r = crawl(b)
        out.append(r)
        print("  [%d/%d] %-30s страниц:%-3d сортов:%-3d %s"
              % (i, len(targets), b["name"][:30], len(r["pages"]), len(r["beers"]),
                 r.get("error", "")), flush=True)
        out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

    tot = sum(len(r["beers"]) for r in out)
    rev = sum(1 for r in out for x in r["beers"] if x["needsReview"])
    print("\nзаписано data/lineups_raw.json: пивоварен %d, кандидатов %d, спорных %d"
          % (len(out), tot, rev))


if __name__ == "__main__":
    main()
