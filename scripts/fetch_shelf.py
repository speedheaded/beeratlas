# -*- coding: utf-8 -*-
"""
Полка: чешское бутылочное пиво из Open Food Facts.

    python scripts/fetch_shelf.py

Пишет data/shelf_raw.json — СЫРЬЁ ДЛЯ ВЫЧИТКИ, как и lineups_raw.json.
В каталог ничего не попадает автоматически.

Зачем этот источник, если DATA-SOURCES.md называет его почти бесполезным.
Тот вывод был про наполнение каталога и остаётся верным: 139 позиций на всю
страну, имена введены людьми и грязные. Но здесь он закрывает ровно то, чего
не дают сайты пивоварен:

  1. Крепость крупной пятёрки. Prazdroj, Gambrinus, Staropramen, Radegast и
     Budvar не печатают числа в тексте страниц — проверено, оттуда не берётся
     ничего. В Open Food Facts они есть.
  2. EAN и фотография лицевой стороны. Штрихкод надёжнее распознавания
     этикетки, а телефон читает его сам, без зрительной модели. Данные под
     ODbL, изображения под свободной лицензией — в отличие от фотографий из
     магазинных фидов, которые остаются чужой собственностью.

Степень (°P) источник не хранит. Она часто стоит в самом названии — «Světlé
12», «Ryze hořká 12» — и вытаскивается тем же классификатором, что в
fetch_lineups.py, с той же пометкой needsReview: число в названии может
оказаться и объёмом, и годом.

Атрибуция обязательна: Open Food Facts, ODbL. Добавить на страницу источников
рядом с OpenStreetMap.
"""
import json
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
sys.path.insert(0, str(Path(__file__).resolve().parent))
# одна таблица «марка -> компания» на весь проект: Pilsner Urquell варит
# Plzensky Prazdroj, и знать об этом должен один файл, а не каждый сборщик
from ingest import BRAND_TO_COMPANY, SPELLING  # noqa: E402
TODAY = date.today().isoformat()
UA = "BeerAtlasResearch/0.1 (+https://beeratlas.eu; github.com/speedheaded/beeratlas)"
API = "https://world.openfoodfacts.org/api/v2/search"
FIELDS = ("code,product_name,generic_name,brands,quantity,image_front_url,"
          "nutriments,categories_tags,labels_tags")

# число в названии: «Světlé 12» — это степень, а не объём и не год
NAME_DEG = re.compile(r"(?<!\d)(\d{1,2})(?:\s*°|\b)")
VOL = re.compile(r"(?i)(\d+(?:[.,]\d+)?)\s*(ml|l\b|cl|g\b)")


def fold(s):
    s = unicodedata.normalize("NFKD", s or "")
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", fold(s)).strip("-")


def api(params, tries=4):
    """Open Food Facts отвечает 503 при частых запросах — ждём и повторяем."""
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    last = None
    for i in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            last = e
            wait = 8 * (i + 1)
            print("    %s — жду %d с" % (str(e)[:48], wait), flush=True)
            time.sleep(wait)
    raise last


def fetch_all():
    out, page = [], 1
    while True:
        d = api({"categories_tags_en": "beers", "countries_tags_en": "czech-republic",
                 "fields": FIELDS, "page_size": 100, "page": page})
        got = d.get("products", [])
        out += got
        total = d.get("count") or 0
        print("  страница %d: %d, всего %d" % (page, len(got), total), flush=True)
        if len(out) >= total or not got:
            break
        page += 1
        time.sleep(1.0)
    return out


def degree_from(name, abv):
    """Степень из названия. Возвращает (plato, needsReview) или (None, False)."""
    for raw in NAME_DEG.findall(name or ""):
        v = int(raw)
        if not (7 <= v <= 21):
            continue
        # если это на самом деле крепость, а не степень — не берём
        if abv is not None and abs(v - float(abv)) < 0.35:
            continue
        return str(v), True
    return None, False


def brewery_index(breweries):
    idx = {}
    have = {b["id"] for b in breweries}
    for brand, company in BRAND_TO_COMPANY.items():
        if company in have:
            idx[slug(brand)] = company
    for written, canonical in SPELLING.items():
        company = BRAND_TO_COMPANY.get(canonical)
        if company in have:
            idx.setdefault(written, company)
    for b in breweries:
        for nm in filter(None, (b["name"], b.get("nameEn"))):
            key = slug(re.sub(r"(?i)^(pivovar|pivovary|kralovsky pivovar|rodinny pivovar)\s+", "", nm))
            if key:
                idx.setdefault(key, b["id"])
            for tok in key.split("-"):
                if len(tok) >= 5:
                    idx.setdefault(tok, b["id"])
    return idx


def match_brewery(brands, idx):
    for part in re.split(r"[,;/]", brands or ""):
        k = slug(part)
        if not k:
            continue
        if k in idx:
            return idx[k], "exact"
        for tok in k.split("-"):
            if len(tok) >= 5 and tok in idx:
                return idx[tok], "token"
    return None, None


def main():
    breweries = json.loads((DATA / "breweries.json").read_text(encoding="utf-8"))
    idx = brewery_index(breweries)

    print("Open Food Facts: чешское пиво…", flush=True)
    prods = fetch_all()

    rows, unmatched = [], {}
    for p in prods:
        name = (p.get("product_name") or "").strip()
        brands = (p.get("brands") or "").strip()
        abv = (p.get("nutriments") or {}).get("alcohol_value")
        if abv is not None:
            try:
                abv = round(float(abv), 2)
            except (TypeError, ValueError):
                abv = None
        plato, review = degree_from(name or p.get("generic_name"), abv)

        bid, how = match_brewery(brands, idx)
        if bid is None and brands:
            unmatched[brands] = unmatched.get(brands, 0) + 1

        cats = p.get("categories_tags") or []
        rows.append({
            "ean": p.get("code"),
            "name": name,
            "brands": brands,
            "breweryId": bid,
            "matchedBy": how,
            "quantity": (p.get("quantity") or "").strip(),
            "abv": abv,
            "plato": plato,
            "needsReview": review,
            "nonAlcoholic": any("non-alcoholic" in c or "nealko" in c for c in cats),
            "image": p.get("image_front_url"),
            "source": {
                "method": "official",
                "source": "https://world.openfoodfacts.org/product/%s" % p.get("code"),
                "licence": "ODbL, Open Food Facts",
                "checkedAt": TODAY,
            },
        })

    rows.sort(key=lambda r: (r["breweryId"] is None, r["brands"].lower(), r["name"].lower()))
    (DATA / "shelf_raw.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")

    matched = sum(1 for r in rows if r["breweryId"])
    with_abv = sum(1 for r in rows if r["abv"] is not None)
    with_img = sum(1 for r in rows if r["image"])
    with_deg = sum(1 for r in rows if r["plato"])
    nonalc = sum(1 for r in rows if r["nonAlcoholic"])
    print("\nзаписано data/shelf_raw.json: позиций %d" % len(rows))
    print("  привязано к нашим пивоварням: %d" % matched)
    print("  с крепостью: %d   со степенью из названия: %d (все needsReview)" % (with_abv, with_deg))
    print("  с фотографией этикетки: %d   безалкогольных: %d" % (with_img, nonalc))
    if unmatched:
        top = sorted(unmatched.items(), key=lambda x: -x[1])[:12]
        print("  марки без пивоварни: %s" % ", ".join("%s(%d)" % t for t in top))


if __name__ == "__main__":
    sys.exit(main())
