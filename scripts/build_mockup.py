"""
Собирает рабочий макет из реальных собранных данных.

    python scripts/ingest.py        # сначала данные
    python scripts/build_mockup.py  # потом страница

Ничего не выдумывает: показывает ровно то, что лежит в data/, включая дыры.
"""

import collections
import io
import json
import sys
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "index.html"

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


def prov(x):
    """Происхождение числа — только когда оно официальное.

    Строки каталога уже носят src/origin/at рядом с числом, а сорок полных
    сортов отдавали одно значение без основания: читатель не мог отличить
    4,6 с этикетки от 4,4, выведенного из стиля. Для непроверенных возвращаем
    None — тогда шаблон рисует их точечными, как и рисовал.
    """
    x = x or {}
    if x.get("method") != "official":
        return None
    return {"origin": x.get("origin"), "src": x.get("source"), "at": x.get("checkedAt")}


slim_beer = []
for b in beers:
    fl = b["flavour"]["value"]
    slim_beer.append({
        "id": b["id"], "breweryId": b["breweryId"], "name": b["name"],
        "cs": b["menuNameCs"], "style": b["style"],
        "plato": (b.get("plato") or {}).get("value"),
        "abv": (b.get("abv") or {}).get("value"),
        "platoP": prov(b.get("plato")),
        "abvP": prov(b.get("abv")),
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

# Справочник штрихкодов для распознавания бутылки. Штрихкод читает сам
# телефон, локально: ни зрительной модели, ни бэкенда, ни платы за вызов.
# Ступени ответа, по убыванию точности:
#   beer    — есть полная страница сорта
#   listed  — есть строка каталога: числа с источником, без описания вкуса
#   brewery — сорт неизвестен, но пивоварню знаем, а значит знаем и где налить
#   none    — не знаем ничего; читаем с этикетки что можем и ведём в подбор
def _key(x):
    import unicodedata
    t = unicodedata.normalize("NFKD", x or "")
    return re.sub(r"[^a-z0-9]+", "", "".join(c for c in t if not unicodedata.combining(c)).lower())

full_idx, listed_idx = {}, {}
for b in beers:
    for nm in (b["name"], b.get("menuNameCs")):
        if nm:
            full_idx[(b["breweryId"], _key(nm))] = b["id"]
listed_rows = json.loads(listed_path.read_text(encoding="utf-8")) if listed_path.exists() else []
for r in listed_rows:
    listed_idx[(r["breweryId"], _key(r["name"]))] = r["id"]

shelf_path = DATA / "shelf_raw.json"
scan = {}
if shelf_path.exists():
    for x in json.loads(shelf_path.read_text(encoding="utf-8")):
        ean = x.get("ean")
        if not ean:
            continue
        bid = x.get("breweryId")
        key = (bid, _key(x.get("name")))
        if key in full_idx:
            kind, target = "beer", full_idx[key]
        elif key in listed_idx:
            kind, target = "listed", listed_idx[key]
        elif bid in keep:
            kind, target = "brewery", bid
        else:
            kind, target = "none", None
        scan[ean] = {
            "kind": kind, "id": target,
            "label": x.get("name") or "", "brand": x.get("brands") or "",
            "abv": x.get("abv"), "plato": x.get("plato"),
            "brewery": bid if bid in keep else None,
        }

# десять бутылок для показа — по всем четырём ступеням, чтобы видно было
# и попадание, и честный промах
demo, per, seen_b = [], {"beer": 0, "listed": 0, "brewery": 0, "none": 0}, set()
want = {"beer": 3, "listed": 3, "brewery": 2, "none": 2}
for ean, r in sorted(scan.items(), key=lambda kv: (kv[1]["kind"], -len(kv[1]["label"]))):
    lab = (r["label"] or "").lower()
    if per[r["kind"]] >= want[r["kind"]] or not r["label"]:
        continue
    if "nealko" in lab or "bez alkoholu" in lab:      # безалкогольное — не показ
        continue
    mark = (r["kind"], r["brewery"] or r["brand"].lower())
    if mark in seen_b:                                # по одному на пивоварню
        continue
    seen_b.add(mark)
    per[r["kind"]] += 1
    demo.append(ean)

# Разброс лежания для зелёной полосы на главной. Числа считаются здесь, а не
# пишутся в текст руками: поменяются данные — поменяется и фраза. Берётся сорт
# с самым долгим лежанием и обычный срок его же ступени Плато, чтобы сравнение
# шло между сопоставимыми пивами, а не между ležákem и алем.
def _lager_days(b):
    for st in ((b.get("production") or {}).get("en") or {}).get("stages", []):
        if st["id"] == "lager" and st.get("days"):
            return st["days"]
    return None


_lagers = [(b, d) for b in beers if not b.get("isAnchor")
           for d in [_lager_days(b)] if d]
_top, _top_days = max(_lagers, key=lambda t: t[1][1])
_tier = (_top.get("plato") or {}).get("value")
_peers = collections.Counter(
    tuple(d) for b, d in _lagers
    if (b.get("plato") or {}).get("value") == _tier and d != _top_days)
_peer = _peers.most_common(1)[0][0] if _peers else _top_days

payload = {
    "hints": slim_hints,
    "scan": scan,
    "scanDemo": demo,
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
        "lagerTier": _tier,
        "lagerPeerLow": _peer[0],
        "lagerPeerHigh": _peer[1],
        "lagerLongest": _top_days[1],
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
