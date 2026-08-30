"""
Дописывает к собранным пивоварням то, чего нет ни в Wikidata, ни в OSM:
авторский текст страницы и точечные исправления заведомо неверных значений.

Запускается после ingest.py и перед build_mockup.py.
Курируемые правки помечаются уровнем `curated` — это не `official`, но и не
догадка: значение общеизвестно и проверяемо, просто источник отдал другое.

    python scripts/enrich_breweries.py
"""

import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from brewery_text import S as STORIES, FIXES  # noqa: E402
from brewery_text_cs import S as STORIES_CS  # noqa: E402

TODAY = date.today().isoformat()
p = ROOT / "data" / "breweries.json"
breweries = json.loads(p.read_text(encoding="utf-8"))

# Текст не может существовать для пивоварни, которой нет. Раньше STORIES
# содержал записи для `more`, `argus` и `nozib` — сущностей, придуманных из
# тега OSM, — и сайт утверждал про них факты. Проверка делает это невозможным.
ids = {b["id"] for b in breweries}
orphan = sorted(set(STORIES) - ids)
if orphan:
    print("ОСТАНОВ: текст написан для пивоварен, которых нет в data/breweries.json:")
    for o in orphan:
        print("   %-18s %s" % (o, STORIES[o][0][:70]))
    print("Удалите записи из scripts/brewery_text.py либо подтвердите марку")
    print("в CURATED_BRANDS (scripts/ingest.py), назвав основание.")
    sys.exit(1)

told = fixed = 0
for b in breweries:
    story = STORIES.get(b["id"])
    if story:
        lead, notes = story
        cs = STORIES_CS.get(b["id"])
        b["story"] = {"en": lead, **({"cs": cs[0]} if cs else {})}
        if notes:
            out = []
            for i, (h, t) in enumerate(notes):
                heading, body = {"en": h}, {"en": t}
                if cs and i < len(cs[1]):
                    heading["cs"], body["cs"] = cs[1][i][0], cs[1][i][1]
                out.append({"heading": heading, "body": body})
            b["notes"] = out
        told += 1
    fix = FIXES.get(b["id"])
    if fix:
        for k, v in fix.items():
            if b.get(k) != v:
                b[k] = v
                b.setdefault("curated", []).append(k)
                fixed += 1
        b.setdefault("source", {})
        b["source"] = {**b["source"], "curatedAt": TODAY}

p.write_text(json.dumps(breweries, ensure_ascii=False, indent=1), encoding="utf-8")

venues = json.loads((ROOT / "data" / "venues.json").read_text(encoding="utf-8"))
counts = {}
for v in venues:
    for bid in v.get("breweryIds", []):
        counts[bid] = counts.get(bid, 0) + 1
withv = [b for b in breweries if counts.get(b["id"])]
missing = [b["name"] for b in withv if "story" not in b]

no_cs = [b["name"] for b in breweries if b.get("story") and "cs" not in b["story"]]
print(f"описаний добавлено: {told}   исправлений: {fixed}   без чешского: {len(no_cs)}")
if no_cs:
    print("  ", ", ".join(no_cs))
print(f"пивоварен с пражскими точками: {len(withv)}, из них без текста: {len(missing)}")
if missing:
    print("  ", ", ".join(missing))
