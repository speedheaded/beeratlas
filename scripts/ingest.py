"""
Первичный сбор данных для Пивного атласа Праги.

Два бесплатных источника:
  * Wikidata (CC0)        — список чешских пивоварен
  * OpenStreetMap (ODbL)  — пражские заведения, телефоны, связь с пивоварней

Всё, что записывается, несёт провенанс: метод, источник, дату.
Ничего не додумывается: чего нет в источнике, того нет в файле.

    python scripts/ingest.py
"""

import json
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TODAY = date.today().isoformat()
UA = "BeerGraphResearch/0.1 (speedheaded@gmail.com)"

WIKIDATA = "https://query.wikidata.org/sparql"
OVERPASS = "https://overpass-api.de/api/interpreter"


def fetch(url, params=None, data=None, accept="application/json", tries=3):
    for attempt in range(tries):
        try:
            if params:
                url = url + "?" + urllib.parse.urlencode(params)
            body = data.encode("utf-8") if data else None
            req = urllib.request.Request(
                url, data=body, headers={"User-Agent": UA, "Accept": accept}
            )
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            if attempt == tries - 1:
                raise
            print(f"    повтор {attempt + 1}/{tries} после {e.__class__.__name__}")
            time.sleep(8 * (attempt + 1))


# ── Wikidata ────────────────────────────────────────────────────────────────

SPARQL = """
SELECT ?b ?bLabel ?bLabelEn ?site ?inception ?cityLabel ?hqLabel ?locLabel ?coord WHERE {
  ?b wdt:P31/wdt:P279* wd:Q131734 ; wdt:P17 wd:Q213 .
  OPTIONAL { ?b wdt:P856 ?site }
  OPTIONAL { ?b wdt:P571 ?inception }
  OPTIONAL { ?b wdt:P131 ?city }
  OPTIONAL { ?b wdt:P159 ?hq }
  OPTIONAL { ?b wdt:P276 ?loc }
  OPTIONAL { ?b wdt:P625 ?coord }
  OPTIONAL { ?b rdfs:label ?bLabel   FILTER(LANG(?bLabel) = "cs") }
  OPTIONAL { ?b rdfs:label ?bLabelEn FILTER(LANG(?bLabelEn) = "en") }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "cs,en" }
}
"""


def slug(s):
    tr = str.maketrans("áčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ", "acdeeinorstuuyzACDEEINORSTUUYZ")
    s = s.translate(tr).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def ingest_breweries():
    print("Wikidata: чешские пивоварни…")
    res = fetch(WIKIDATA, params={"query": SPARQL, "format": "json"},
                accept="application/sparql-results+json")
    rows = res["results"]["bindings"]

    by_qid = {}
    for r in rows:
        qid = r["b"]["value"].rsplit("/", 1)[-1]
        name = (r.get("bLabel") or r.get("bLabelEn") or {}).get("value")
        if not name or name == qid:
            continue
        rec = by_qid.setdefault(qid, {
            "id": slug(name),
            "wikidata": qid,
            "name": name,
            "nameEn": (r.get("bLabelEn") or {}).get("value"),
            "city": ((r.get("cityLabel") or r.get("hqLabel") or r.get("locLabel") or {})
                     .get("value")),
            "source": {"method": "official", "source": f"https://www.wikidata.org/wiki/{qid}",
                       "checkedAt": TODAY},
        })
        if not rec.get("city"):
            rec["city"] = ((r.get("cityLabel") or r.get("hqLabel") or r.get("locLabel") or {})
                           .get("value"))
        if "site" in r and "site" not in rec:
            rec["site"] = r["site"]["value"]
        if "inception" in r and "founded" not in rec:
            m = re.match(r"(-?\d{1,4})", r["inception"]["value"])
            if m:
                rec["founded"] = int(m.group(1))
        if "coord" in r and "lat" not in rec:
            m = re.match(r"Point\(([-\d.]+) ([-\d.]+)\)", r["coord"]["value"])
            if m:
                rec["lng"], rec["lat"] = float(m.group(1)), float(m.group(2))

    out = sorted(by_qid.values(), key=lambda x: x["name"])
    print(f"  получено: {len(out)}   с сайтом: {sum('site' in b for b in out)}"
          f"   с годом: {sum('founded' in b for b in out)}")
    return out


# ── OpenStreetMap ───────────────────────────────────────────────────────────

OVERPASS_Q = """
[out:json][timeout:180];
area["name"="Praha"]["admin_level"="6"]->.p;
(
  node(area.p)["amenity"~"^(pub|bar|biergarten)$"];
  way(area.p)["amenity"~"^(pub|bar|biergarten)$"];
);
out center tags;
"""

# Мусорные значения тега brewery — не марки
JUNK = {"yes", "no", "various", "různé", "ruzne", "mixed", "multiple", "*"}

# Тег OSM `brewery=*` — это ПОДСКАЗКА картографа, а не сущность. За ним лежат
# марки (Hubertus), владельцы концернов (AB InBev), названия пива
# (maisel's weisse) и прямой мусор (`more` из одного паба). Раньше каждое
# такое значение становилось пивоварней и получало сочинённый текст — то есть
# сайт утверждал существование объектов, которых нет.
#
# Правило: пивоварня заводится, только если есть подтверждение —
#   1) запись в Wikidata, либо
#   2) строка ниже: мы приняли её вручную и сказали, на каком основании.
# Всё остальное остаётся на заведении как brandHints: сохраняется, датируется,
# видно в данных, но не получает ни страницы, ни текста.
#
# Пополняется по мере доказательств: линейка, снятая с сайта пивоварни
# (scripts/fetch_lineups.py), или телефонный звонок переводят марку сюда.
CURATED_BRANDS = {
    "breznak":       "марку держит курируемый сорт Březňák Světlý ležák",
    "konrad":        "марку держит курируемый сорт Konrád 12",
    "hubertus":      "марку держит курируемый сорт Hubertus Premium",
    "matuska":       "марку держат курируемые сорта Matuška Raptor и Zlatá Raketa",
    "guinness":      "иностранная марка-якорь, нужна для сравнения",
    "stella-artois": "иностранная марка-якорь, нужна для сравнения",
}

# Приведение написаний из OSM к одной марке.
# Регистр, подчёркивания и опечатки в OSM не нормализованы — сводим руками.
SPELLING = {
    "pilsner-urquell": "Pilsner Urquell", "pilsener-urquell": "Pilsner Urquell",
    "plzensky-prazdroj": "Pilsner Urquell", "prazdroj": "Pilsner Urquell",
    "urquell": "Pilsner Urquell", "pilsner": "Pilsner Urquell",
    "kozel": "Velkopopovický Kozel", "velkopopovicky-kozel": "Velkopopovický Kozel",
    "vinohadsky-pivovar": "Vinohradský pivovar",  # опечатка в OSM
    "unetice": "Únětický pivovar", "uneticky-pivovar": "Únětický pivovar",
    "cerna-hora": "Černá Hora", "kout-na-sumave": "Kout na Šumavě",
    "molson-cors": "Molson Coors",
    # из тега OSM марки приходят как их набрал картограф, строчными
    "matuska": "Matuška", "breznak": "Březňák", "konrad": "Konrád",
    "hubertus": "Hubertus",
}

# Марка ≠ юридическое название. Wikidata знает компанию, OSM — то, что на кране.
# Это редакторское знание, а не извлечённые данные — помечается отдельно.
BRAND_TO_COMPANY = {
    "Pilsner Urquell": "plzensky-prazdroj",
    "Velkopopovický Kozel": "pivovar-velke-popovice",
    "Gambrinus": "pivovar-gambrinus-plzen",
    "Staropramen": "pivovary-staropramen",
    "Radegast": "pivovar-radegast",
    "Bernard": "rodinny-pivovar-bernard",
    "Budweiser Budvar": "budejovicky-budvar",
    "Svijany": "pivovar-svijany",
    "Zichovec": "pivovar-zichovec",
}

# Марки, которые в Праге наливают, но пивоварня не чешская.
# Без пометки они выглядят в списке как местные, а это враньё.
FOREIGN = {"guinness", "stella-artois", "molson-coors", "ab-inbev",
           "maisel-s-weisse", "heineken", "budweiser"}

# Слова, не различающие пивоварни
STOP = {"pivovar", "pivovary", "rodinny", "mestansky", "akciova", "spolecnost",
        "brewery", "family", "as", "sro", "a-s", "s-r-o"}


def norm_brewery(raw):
    key = slug(raw)
    if key.replace("-", " ") in JUNK or not key:
        return None
    return SPELLING.get(key, raw.strip())


def ingest_venues():
    print("OpenStreetMap: пражские пабы и бары…")
    res = fetch(OVERPASS, data="data=" + urllib.parse.quote(OVERPASS_Q))
    els = res["elements"]

    venues = []
    for e in els:
        t = e.get("tags", {})
        name = t.get("name")
        if not name:
            continue
        lat = e.get("lat") or (e.get("center") or {}).get("lat")
        lng = e.get("lon") or (e.get("center") or {}).get("lon")
        if lat is None:
            continue

        brands = []
        if "brewery" in t:
            for part in re.split(r"[;,]", t["brewery"]):
                n = norm_brewery(part)
                if n and n not in brands:
                    brands.append(n)

        v = {
            "id": f"osm-{e['type'][0]}{e['id']}",
            "name": name,
            "kind": {"pub": "pub", "bar": "bar", "biergarten": "biergarten"}[t["amenity"]],
            "lat": round(lat, 6), "lng": round(lng, 6),
            "breweryNames": brands,
            "source": {"method": "official", "source": f"https://www.openstreetmap.org/{e['type']}/{e['id']}",
                       "checkedAt": TODAY},
        }
        for src, dst in (("phone", "phone"), ("contact:phone", "phone"),
                         ("website", "website"), ("contact:website", "website"),
                         ("opening_hours", "openingHours"), ("addr:street", "street"),
                         ("addr:suburb", "district"), ("addr:city", "city")):
            if src in t and dst not in v:
                v[dst] = t[src]
        if t.get("microbrewery") == "yes" or t.get("brewery") == "yes":
            v["brewpub"] = True
        venues.append(v)

    with_phone = [v for v in venues if "phone" in v]
    with_brand = [v for v in venues if v["breweryNames"]]
    print(f"  заведений с названием: {len(venues)}")
    print(f"  с телефоном:           {len(with_phone)}   <- список для обзвона")
    print(f"  с маркой пивоварни:    {len(with_brand)}")
    return sorted(venues, key=lambda v: v["name"])


# ── районы из координат ─────────────────────────────────────────────────────

DISTRICTS_Q = """
[out:json][timeout:180];
area["name"="Praha"]["admin_level"="6"]->.p;
relation(area.p)["boundary"="administrative"]["admin_level"="9"];
out geom;
"""


def _inside(lat, lng, ring):
    """Луч вправо: нечётное число пересечений — точка внутри."""
    inside = False
    n = len(ring)
    for i in range(n):
        y1, x1 = ring[i]
        y2, x2 = ring[(i + 1) % n]
        if (x1 > lng) != (x2 > lng):
            t = (lng - x1) / (x2 - x1)
            if lat < y1 + t * (y2 - y1):
                inside = not inside
    return inside


def add_districts(venues):
    """
    OSM отдаёт addr:suburb меньше чем у трети заведений. Район восстанавливается
    из координат по границам городских частей — это точнее, чем оставлять пусто,
    и по-прежнему уровень `official`: данные те же, вычисление наше.
    """
    print("OpenStreetMap: границы городских частей…")
    try:
        res = fetch(OVERPASS, data="data=" + urllib.parse.quote(DISTRICTS_Q))
    except Exception as e:
        print(f"  не получилось ({e.__class__.__name__}), районы остаются как есть")
        return
    polys = []
    for r in res["elements"]:
        name = (r.get("tags") or {}).get("name")
        ring = [(m["lat"], m["lon"]) for m in r.get("members", [])
                if m.get("role") == "outer" for m in m.get("geometry") or []]
        if not name:
            continue
        ring = []
        for m in r.get("members", []):
            if m.get("role") == "outer":
                ring += [(g["lat"], g["lon"]) for g in (m.get("geometry") or [])]
        if len(ring) > 3:
            lats = [p[0] for p in ring]
            lngs = [p[1] for p in ring]
            polys.append((name, ring, min(lats), max(lats), min(lngs), max(lngs)))
    print(f"  границ получено: {len(polys)}")

    filled = 0
    for v in venues:
        if v.get("district"):
            continue
        for name, ring, la0, la1, ln0, ln1 in polys:
            if la0 <= v["lat"] <= la1 and ln0 <= v["lng"] <= ln1 and _inside(v["lat"], v["lng"], ring):
                v["district"] = name
                v["districtFrom"] = "geometry"
                filled += 1
                break
    print(f"  район восстановлен по координатам: {filled}")


# ── связывание ──────────────────────────────────────────────────────────────

def tokens(name):
    return {t for t in slug(name).split("-") if t and t not in STOP and len(t) > 2}


def link(breweries, venues):
    """
    Связывает заведения с пивоварнями. Три уровня, по убыванию надёжности:
      1. курируемая карта «марка → компания»
      2. точное совпадение названия или его короткой формы
      3. совпадение по различающему токену («svijany» в «Pivovar Svijany»)

    Марки, не найденные нигде, становятся заготовками пивоварен: граф не должен
    терять реальную пивоварню только потому, что Wikidata о ней не знает.
    """
    by_id = {b["id"]: b for b in breweries}
    exact, by_token = {}, {}
    for b in breweries:
        for nm in filter(None, (b["name"], b.get("nameEn"))):
            exact.setdefault(slug(nm), b["id"])
            exact.setdefault(re.sub(r"^(pivovar|pivovary|rodinny-pivovar|mestansky-pivovar)-",
                                    "", slug(nm)), b["id"])
        for t in tokens(b["name"]):
            by_token.setdefault(t, set()).add(b["id"])

    counts = {"curated": 0, "exact": 0, "token": 0}
    stubs, seen_brands = {}, {}

    unknown = {}
    for v in venues:
        ids, methods, hints = [], [], []
        for n in v["breweryNames"]:
            seen_brands[n] = seen_brands.get(n, 0) + 1
            bid = m = None
            if n in BRAND_TO_COMPANY and BRAND_TO_COMPANY[n] in by_id:
                bid, m = BRAND_TO_COMPANY[n], "curated"
            elif slug(n) in exact:
                bid, m = exact[slug(n)], "exact"
            else:
                cand = set()
                for t in tokens(n):
                    cand |= by_token.get(t, set())
                if len(cand) == 1:
                    bid, m = cand.pop(), "token"
            if bid:
                counts[m] += 1
                ids.append(bid)
                methods.append(m)
            elif slug(n) in CURATED_BRANDS:
                stub = stubs.setdefault(slug(n), {
                    "id": slug(n), "name": n, "wikidata": None,
                    "source": {"method": "unverified",
                               "source": "тег brewery в OpenStreetMap + " + CURATED_BRANDS[slug(n)],
                               "checkedAt": TODAY},
                    "needsResearch": True,
                    "curatedBrand": True,
                    "foreign": slug(n) in FOREIGN,
                })
                ids.append(stub["id"])
                methods.append("curated-brand")
            else:
                # подтверждения нет — марка остаётся подсказкой на заведении
                hints.append(n)
                unknown[slug(n)] = unknown.get(slug(n), 0) + 1
        v["breweryIds"] = sorted(set(ids))
        if hints:
            v["brandHints"] = sorted(set(hints))
        if methods:
            v["linkMethod"] = sorted(set(methods))

    print(f"  связано: курируемой картой {counts['curated']}, "
          f"точно {counts['exact']}, по токену {counts['token']}")
    print(f"  марок принято вручную: {len(stubs)}")
    if stubs:
        print("    ", ", ".join(sorted(s["name"] for s in stubs.values())))
    print(f"  марок без подтверждения: {len(unknown)} -> brandHints, не пивоварни")
    if unknown:
        print("    ", ", ".join(sorted(unknown)))
    breweries.extend(sorted(stubs.values(), key=lambda x: x["name"]))
    return seen_brands


def main():
    DATA.mkdir(exist_ok=True)
    breweries = ingest_breweries()
    venues = ingest_venues()
    add_districts(venues)
    brands = link(breweries, venues)

    for name, obj in (("breweries.json", breweries), ("venues.json", venues)):
        p = DATA / name
        p.write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"записано: {p.relative_to(ROOT)}  ({len(obj)})")

    stats = {
        "generatedAt": TODAY,
        "sources": {
            "wikidata": {"license": "CC0", "breweries": len(breweries)},
            "openstreetmap": {"license": "ODbL", "attribution": "© OpenStreetMap contributors",
                              "venues": len(venues)},
        },
        "venuesWithPhone": sum("phone" in v for v in venues),
        "venuesWithBrewery": sum(bool(v["breweryIds"]) for v in venues),
        "osmBrands": dict(sorted(brands.items(), key=lambda kv: -kv[1])),
    }
    (DATA / "stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=1), encoding="utf-8")
    print("записано: data/stats.json")


if __name__ == "__main__":
    sys.exit(main())
