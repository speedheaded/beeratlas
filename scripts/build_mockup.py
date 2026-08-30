"""
Собирает рабочий макет из реальных собранных данных.

    python scripts/ingest.py        # сначала данные
    python scripts/build_mockup.py  # потом страница

Ничего не выдумывает: показывает ровно то, что лежит в data/, включая дыры.
"""

import io
import json
import sys
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "mockup" / "index.html"

breweries = json.loads((DATA / "breweries.json").read_text(encoding="utf-8"))
venues = json.loads((DATA / "venues.json").read_text(encoding="utf-8"))
stats = json.loads((DATA / "stats.json").read_text(encoding="utf-8"))
beers = json.loads((DATA / "beers.json").read_text(encoding="utf-8"))

by_id = {b["id"]: b for b in breweries}

# сколько пражских заведений у каждой пивоварни
counts = {}
for v in venues:
    for bid in v.get("breweryIds", []):
        counts[bid] = counts.get(bid, 0) + 1

# в макет кладём только пивоварни, у которых есть пражское заведение,
# плюс те, что упомянуты в затравке сортов
seed_bids = {b["breweryId"] for b in beers if b["breweryId"]}
keep = {bid for bid in counts} | {b["id"] for b in breweries if b["id"] in seed_bids}

slim_br = []
for b in breweries:
    if b["id"] not in keep:
        continue
    slim_br.append({
        "id": b["id"], "name": b["name"], "nameEn": b.get("nameEn"),
        "city": b.get("city"), "founded": b.get("founded"), "site": b.get("site"),
        "wikidata": b.get("wikidata"), "stub": bool(b.get("needsResearch")),
        "foreign": bool(b.get("foreign")), "curated": b.get("curated") or [],
        "story": b.get("story"),
        "notes": [{"h": n["heading"], "b": n["body"]} for n in b.get("notes", [])],
        "venues": counts.get(b["id"], 0),
    })
slim_br.sort(key=lambda x: (-x["venues"], x["name"]))

slim_ve = []
for v in venues:
    slim_ve.append({
        "id": v["id"], "n": v["name"], "k": v["kind"],
        "d": v.get("district") or v.get("city"), "st": v.get("street"),
        "p": v.get("phone"), "h": v.get("openingHours"), "w": v.get("website"),
        "b": v.get("breweryIds", []), "bp": bool(v.get("brewpub")),
        # марки, которые заведение называет, но подтверждения им нет
        "bh": v.get("brandHints") or [],
        "dg": v.get("districtFrom") == "geometry",
        "lat": v["lat"], "lng": v["lng"],
    })

AXES = ["bitterness", "maltSweetness", "body", "dryness", "roast",
        "fruitEster", "sourness", "hopAroma", "hopProfile"]

slim_beer = []
for b in beers:
    fl = b["flavour"]["value"]
    slim_beer.append({
        "id": b["id"], "breweryId": b["breweryId"], "name": b["name"],
        "cs": b["menuNameCs"], "style": b["style"],
        "plato": (b.get("plato") or {}).get("value"),
        "abv": (b.get("abv") or {}).get("value"),
        "f": [fl[a] for a in AXES],
        "like": b.get("tastesLike") or [],
        "lead": b.get("lead"),
        "notes": [{"h": n["heading"], "b": n["body"]} for n in b.get("notes", [])],
        "prod": b.get("production"),
        "anchor": bool(b.get("isAnchor")),
        "venues": counts.get(b["breweryId"], 0),
    })

sys.path.insert(0, str(Path(__file__).resolve().parent))
# Чешский словарь — один источник: scripts/ui_cs.py. Раньше он же лежал
# литералом в шаблоне, и две копии приходилось править руками; за один
# день они разошлись на 34 ключа.
from ui_cs import UI as UI_CS  # noqa: E402
from brewing_text import PROCESS  # noqa: E402
from brewing_text_cs import PROCESS as PROCESS_CS  # noqa: E402

# второй уровень каталога: сорта, которые мы знаем, но не описали.
# Без вкусового профиля — значит, в подборе по якорю не участвуют.
listed_path = DATA / "listed.json"
slim_listed = []
if listed_path.exists():
    for r in json.loads(listed_path.read_text(encoding="utf-8")):
        if r["breweryId"] not in keep:
            continue
        slim_listed.append({
            "id": r["id"], "breweryId": r["breweryId"], "name": r["name"],
            "cs": r.get("menuNameCs") or r["name"],
            "plato": (r.get("plato") or {}).get("value"),
            "abv": (r.get("abv") or {}).get("value"),
            "src": (r.get("plato") or r.get("abv") or {}).get("source"),
            "origin": (r.get("plato") or r.get("abv") or {}).get("origin"),
            "at": (r.get("plato") or r.get("abv") or {}).get("checkedAt"),
            "ean": r.get("ean"),
            "venues": counts.get(r["breweryId"], 0),
        })

# марки, которые заведения называют, но подтверждения им нет: ни записи в
# Wikidata, ни линейки с сайта. Пивоварнями они не считаются (см. решение 13),
# но и молчать о них нечестно — заведение их действительно наливает.
hints = {}
for v in venues:
    for b in v.get("brandHints") or []:
        hints.setdefault(b, []).append(v["name"])
slim_hints = [{"brand": b, "venues": sorted(vs)} for b, vs in
              sorted(hints.items(), key=lambda kv: (-len(kv[1]), kv[0].lower()))]

payload = {
    "hints": slim_hints,
    "generatedAt": stats["generatedAt"],
    "listed": slim_listed,
    "process": [{"h": {"en": h, "cs": hc}, "b": {"en": b, "cs": bc}}
                for (h, b), (hc, bc) in zip(PROCESS, PROCESS_CS)],
    "breweries": slim_br,
    "venues": slim_ve,
    "beers": slim_beer,
    "stats": {
        "venuesTotal": len(venues),
        "venuesWithPhone": stats["venuesWithPhone"],
        "venuesWithBrewery": stats["venuesWithBrewery"],
        "breweriesWikidata": stats["sources"]["wikidata"]["breweries"],
        "breweriesTotal": len(breweries),
        "beersTotal": len([b for b in beers if not b.get("isAnchor")]),
        "beersWithVenue": len([b for b in slim_beer if not b["anchor"] and b["venues"] > 0]),
    },
}

# Паритет держится сборкой, а не памятью: строка, обёрнутая в T() без ключа
# в словаре, молча выходит английской. Полная проверка, включая необёрнутые
# литералы, — python scripts/check_cs.py
import check_cs  # noqa: E402
if check_cs.static(verbose=False):
    print("СБОРКА ОСТАНОВЛЕНА: у части строк нет чешского перевода")
    check_cs.static()
    sys.exit(1)

TPL = io.open(ROOT / "scripts" / "mockup_template.html", encoding="utf-8").read()
html = TPL.replace("/*__DATA__*/null", json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
assert "/*__UI_CS__*/" in html, "в шаблоне нет места для словаря"
html = html.replace("/*__UI_CS__*/null", json.dumps(UI_CS, ensure_ascii=False, separators=(",", ":")))
OUT.parent.mkdir(exist_ok=True)
OUT.write_text(html, encoding="utf-8")
print(f"записано: {OUT.relative_to(ROOT)}  ({len(html) // 1024} КБ)")
print(f"  пивоварен в макете: {len(slim_br)}   заведений: {len(slim_ve)}   сортов: {len(slim_beer)} полных + {len(slim_listed)} строк")
