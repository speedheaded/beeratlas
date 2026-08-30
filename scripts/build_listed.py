# -*- coding: utf-8 -*-
"""
Второй уровень каталога: сорта, которые мы знаем, но не описали.

    python scripts/build_listed.py

Читает data/lineups_raw.json и data/shelf_raw.json, пишет data/listed.json.

Зачем второй уровень. Полная страница сорта стоит дорого: ведущий абзац на
двух языках, девять осей вкуса, разбор технологии. Поэтому их сорок. Снятого
с сайтов пивоварен — под сотню, и на той же глубине это втрое больше всей
содержательной работы проекта.

Строка каталога даёт меньше и не притворяется: имя, степень, крепость,
пивоварня, где выпить, адрес источника и дата. **Никакого придуманного
описания вкуса.** Этого хватает, чтобы ответить на главный вопрос сайта, и
хватает, чтобы фотография бутылки не упиралась в сорок сортов.

Уровень — про то, СКОЛЬКО мы можем сказать, а не про то, насколько уверены.
Провенанс отдельный и по каждому значению: строка со степенью с сайта
пивоварни несёт `official` и ссылку, а полные сорок страниц до сих пор стоят
на `unverified`, набранном по знанию. По доказательности второй уровень
сейчас сильнее первого.

Утверждение — правилом, а не руками. Строка проходит, если у неё есть живая
пивоварня с пражским заведением, вменяемое имя, хотя бы одно число с адресом
источника, и она не помечена «проверить». Всё остальное уходит в отчёт
исключений, где решает человек. Отчёт: python scripts/build_listed.py --skip
"""
import json
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TODAY = date.today().isoformat()

# хвосты, которые пивоварни вешают на заголовок страницы сорта
TAIL = re.compile(r"\s+[-–—]\s+.*$")
NOISE_NAME = re.compile(r"(?i)(kategorie|sdružen|sdruzen|vše o pivu|vse o pivu|"
                        r"e-?shop|novinky|kontakt|cookies|stálá nabídka|stala nabidka|"
                        r"IBU|EBC|hořkost|horkost|barva:|naše piva|nase piva)")
# на сайтах пивоварен продаётся не только пиво: у Únětického в том же списке
# сидр, рислинг и южноафриканское вино с крепостью 12 %
# остатки разметки и строки, которые вообще не про сорт: ценник, открытка,
# «tuplák» — это размер кружки, а «alk. (» — хвост от вырезанного числа
ARTIFACT = re.compile(r"(?i)(alk\.|obsah alkoholu|\bcena\b|pohlednice|tuplak|tuplák|"
                      r"\bks\b|objednat|koupit)")
NOT_BEER = re.compile(r"(?i)(cider|cidre|víno|vino\b|riesling|rulandsk|sauvignon|"
                      r"limonád|limonad|kombucha|medovina|gin\b|rum\b|whisk)")


def fold(s):
    s = unicodedata.normalize("NFKD", s or "")
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def key(s):
    return re.sub(r"[^a-z0-9]+", "", fold(s))


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", fold(s)).strip("-")


def clean_name(raw):
    n = (raw or "").split("|")[0]          # «Hvozd | Naše piva | Pivovar Cvikov»
    n = TAIL.sub("", n.strip())
    n = re.sub(r"\s+,", ",", n)            # «Únětické pivo , filtrované»
    n = re.sub(r"[(,]\s*$", "", n)
    n = re.sub(r"\s{2,}", " ", n).strip(" -–—:·|,(")
    return n


# имена, которые на самом деле подписи к числам, а не названия сортов
LABEL_ONLY = {"epm", "max", "min", "alk", "plato", "nealko", "obsah", "ibu", "ebc"}


def is_label(name):
    letters = "".join(c for c in fold(name) if c.isalpha())
    return len(letters) < 3 or fold(name).strip(" .:,") in LABEL_ONLY


def implausible(plato, abv):
    """Пара чисел, которая не может принадлежать одному пиву.

    Крепость у пива составляет примерно треть степени. 15° и 6,5 % —
    согласованная пара. 10° и 6,2 % — числа с двух разных строк, склеенные
    заголовком. Крепость выше 9,5 % без степени — скорее вино, чем пиво:
    у Únětického в списке рислинг.
    """
    try:
        p = float(plato) if plato is not None else None
        a = float(abv) if abv is not None else None
    except (TypeError, ValueError):
        return "число не разбирается"
    if p is not None and a is not None:
        r = a / p if p else 0
        if not (0.30 <= r <= 0.50):
            return "степень и крепость не сходятся (%.2f)" % r
    if p is None and a is not None and a > 9.5:
        return "крепость выше 9,5 % без степени — возможно, не пиво"
    return None


def load(path):
    p = DATA / path
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else []


def candidates():
    """Сводит сырьё из обоих источников к одному виду."""
    out = []
    for r in load("lineups_raw.json"):
        for x in r["beers"]:
            out.append({
                "breweryId": r["breweryId"], "name": clean_name(x["name"]),
                "plato": x["plato"], "abv": x["abv"],
                "needsReview": x["needsReview"], "url": x["url"],
                "ean": None, "image": None, "nonAlcoholic": False,
                "method": "official", "origin": "the brewery's own site",
            })
    for r in load("shelf_raw.json"):
        out.append({
            "breweryId": r["breweryId"], "name": clean_name(r["name"]),
            "plato": r["plato"], "abv": str(r["abv"]) if r["abv"] is not None else None,
            "needsReview": r["needsReview"], "url": r["source"]["source"],
            "ean": r["ean"], "image": r["image"], "nonAlcoholic": r["nonAlcoholic"],
            "method": "official", "origin": "Open Food Facts, ODbL",
        })
    return out


# origin попадает в интерфейс через T(): пишем по-английски, перевод в словаре.
# Рабочий язык проекта русский, и он один раз уже протёк на страницу.
def sourced(value, method, url, origin):
    if value is None:
        return None
    try:
        v = float(value)
        v = int(v) if v == int(v) else v
    except (TypeError, ValueError):
        return None
    return {"value": v, "method": method, "source": url,
            "origin": origin, "checkedAt": TODAY}


def main():
    breweries = json.loads((DATA / "breweries.json").read_text(encoding="utf-8"))
    venues = json.loads((DATA / "venues.json").read_text(encoding="utf-8"))
    beers = json.loads((DATA / "beers.json").read_text(encoding="utf-8"))

    by_id = {b["id"]: b for b in breweries}
    with_venue = set()
    for v in venues:
        with_venue.update(v.get("breweryIds", []))

    # то, что уже описано полностью, вторым уровнем не дублируем
    described = set()
    for b in beers:
        for n in (b["name"], b.get("menuNameCs")):
            if n:
                described.add((b["breweryId"], key(n)))

    kept, skipped, seen = {}, [], set()
    for c in candidates():
        bid, name = c["breweryId"], c["name"]

        def drop(why):
            skipped.append((why, bid, name or "(без имени)", c["url"]))

        if not bid or bid not in by_id:
            drop("пивоварня не подтверждена")
            continue
        if bid not in with_venue:
            drop("нет пражского заведения — правило публикации")
            continue
        if not name or len(name) < 3 or len(name) > 60 or NOISE_NAME.search(name):
            drop("имя не похоже на сорт")
            continue
        if c["plato"] is None and c["abv"] is None:
            drop("ни одного числа")
            continue
        if c["needsReview"]:
            drop("число двусмысленно, нужен человек")
            continue
        if is_label(name):
            drop("подпись к числу, а не название сорта")
            continue
        if ARTIFACT.search(name):
            drop("остаток разметки, не имя сорта")
            continue
        if NOT_BEER.search(name):
            drop("не пиво")
            continue
        if c["nonAlcoholic"]:
            drop("безалкогольное — отдельный разговор")
            continue
        bad = implausible(c["plato"], c["abv"])
        if bad:
            drop(bad)
            continue
        if (bid, key(name)) in described:
            drop("уже есть полная страница")
            continue

        k = (bid, key(name))
        if k in seen:                      # тот же сорт из двух источников
            row = kept[k]
            for f in ("plato", "abv"):
                if row[f] is None and c[f] is not None:
                    row[f] = sourced(c[f], c["method"], c["url"], c["origin"])
            row["ean"] = row["ean"] or c["ean"]
            row["image"] = row["image"] or c["image"]
            continue
        seen.add(k)
        kept[k] = {
            "id": slug(bid + "-" + name), "breweryId": bid, "name": name,
            "menuNameCs": name,            # снято с чешского источника как есть
            "tier": "listed",
            "plato": sourced(c["plato"], c["method"], c["url"], c["origin"]),
            "abv": sourced(c["abv"], c["method"], c["url"], c["origin"]),
            "ean": c["ean"], "image": c["image"],
            "nonAlcoholic": c["nonAlcoholic"],
        }

    rows = sorted(kept.values(), key=lambda r: (by_id[r["breweryId"]]["name"], r["name"]))
    (DATA / "listed.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")

    per = {}
    for r in rows:
        per[r["breweryId"]] = per.get(r["breweryId"], 0) + 1
    print("записано data/listed.json: строк каталога %d у %d пивоварен"
          % (len(rows), len(per)))
    print("  со степенью: %d   с крепостью: %d   со штрихкодом: %d   с этикеткой: %d"
          % (sum(1 for r in rows if r["plato"]), sum(1 for r in rows if r["abv"]),
             sum(1 for r in rows if r["ean"]), sum(1 for r in rows if r["image"])))
    print("  каталог всего: %d полных + %d строк = %d"
          % (len(beers), len(rows), len(beers) + len(rows)))

    why = {}
    for w, *_ in skipped:
        why[w] = why.get(w, 0) + 1
    print("\nне прошло: %d" % len(skipped))
    for w, n in sorted(why.items(), key=lambda x: -x[1]):
        print("   %-42s %d" % (w, n))

    if "--skip" in sys.argv:
        print("\n── исключения ──")
        for w, bid, name, url in skipped:
            print("  %-42s %-26s %s" % (w, name[:26], url[:52]))
    else:
        print("\nразбор исключений: python scripts/build_listed.py --skip")


if __name__ == "__main__":
    main()
