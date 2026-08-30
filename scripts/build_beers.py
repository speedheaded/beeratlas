"""
Каталог сортов для пивоварен, у которых есть пражские заведения.

ВАЖНО про достоверность. Все числа здесь набраны по знанию, а не сняты с
этикетки, поэтому уровень — `unverified`, и в публикацию они не идут.
Вкусовые профили выведены из стиля и параметров — уровень `inferred`.

Это ровно тот случай, ради которого сделана система провенанса: макет можно
показывать, ничего не выдавая за факт. Перед запуском сайта каждая строка
`unverified` либо подтверждается с этикетки, либо удаляется.

    python scripts/build_beers.py
"""

import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from beer_text import L as LEADS, N as NOTES  # noqa: E402
from beer_text_cs import L as LEADS_CS, N as NOTES_CS  # noqa: E402
import brewing_derive  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TODAY = date.today().isoformat()

AXES = ["bitterness", "maltSweetness", "body", "dryness", "roast",
        "fruitEster", "sourness", "hopAroma", "hopProfile"]

# name | brewery | czech menu name | style | °P | ABV | 9 осей | tastesLike
ROWS = [
    # ── Plzeňský Prazdroj ────────────────────────────────────────────────
    ("Pilsner Urquell", "plzensky-prazdroj", "Plzeňský Prazdroj 12°", "Czech pale lager", 12, 4.4,
     [6.5, 5.5, 5, 6, 1, 2, 1, 5, 1], ["Heineken, but far more bitter and malty"]),
    ("Pilsner Urquell Nefiltrovaná", "plzensky-prazdroj", "Prazdroj nefiltrovaný 12°", "Czech pale lager, unfiltered", 12, 4.4,
     [6, 6, 5.5, 5, 1, 3, 1, 6, 1], []),
    # ── Velké Popovice ───────────────────────────────────────────────────
    ("Kozel Světlý", "pivovar-velke-popovice", "Velkopopovický Kozel 10°", "Czech pale lager", 10, 4.0,
     [3.5, 5.5, 4, 4.5, 1, 2, 1, 2.5, 1], []),
    ("Kozel 11", "pivovar-velke-popovice", "Velkopopovický Kozel 11°", "Czech pale lager", 11, 4.6,
     [4, 6.5, 5, 4, 1, 2, 1, 3, 1], ["softer and sweeter than Pilsner Urquell"]),
    ("Kozel Černý", "pivovar-velke-popovice", "Velkopopovický Kozel Černý 10°", "Czech dark lager", 10, 3.8,
     [3, 8, 5.5, 3, 6.5, 2, 1, 2, 1], ["what people order expecting Guinness — it is not"]),
    # ── Gambrinus ────────────────────────────────────────────────────────
    ("Gambrinus Originál 10", "pivovar-gambrinus-plzen", "Gambrinus 10°", "Czech pale lager", 10, 4.1,
     [4, 5, 4, 5, 1, 2, 1, 3, 1], []),
    ("Gambrinus Originál 11", "pivovar-gambrinus-plzen", "Gambrinus Originál 11°", "Czech pale lager", 11, 4.7,
     [4.5, 5.5, 4.5, 5, 1, 2, 1, 3.5, 1], []),
    # ── Staropramen ──────────────────────────────────────────────────────
    ("Staropramen Světlý", "pivovary-staropramen", "Staropramen 10°", "Czech pale lager", 10, 4.0,
     [3.5, 5, 4, 5, 1, 2, 1, 2.5, 1.5], []),
    ("Staropramen Ležák", "pivovary-staropramen", "Staropramen Ležák 12°", "Czech pale lager", 12, 5.0,
     [4.5, 5.5, 5, 5, 1, 2, 1, 3.5, 1.5], []),
    ("Staropramen Granát", "pivovary-staropramen", "Staropramen Granát 11°", "Czech amber lager", 11, 4.8,
     [3, 7.5, 5.5, 3.5, 4.5, 2.5, 1, 2, 1], ["halfway to a dark lager"]),
    # ── Únětický pivovar ─────────────────────────────────────────────────
    ("Únětická 10", "uneticky-pivovar", "Únětická desítka 10°", "Czech pale lager, unfiltered", 10, 4.0,
     [5, 5.5, 4.5, 5.5, 1, 2.5, 1, 4, 1], []),
    ("Únětická 12", "uneticky-pivovar", "Únětická dvanáctka 12°", "Czech pale lager, unfiltered", 12, 5.0,
     [6, 6, 5.5, 5.5, 1, 2.5, 1, 5, 1], ["Pilsner Urquell, but unfiltered and rounder"]),
    ("Únětická tmavá 12", "uneticky-pivovar", "Únětická tmavá 12°", "Czech dark lager", 12, 4.6,
     [4, 7.5, 6, 4, 7, 2.5, 1, 2.5, 1], ["the dark beer people wanted when they ordered Kozel Černý"]),
    # ── Svijany ──────────────────────────────────────────────────────────
    ("Svijanský Máz", "pivovar-svijany", "Svijanský Máz 11°", "Czech pale lager", 11, 4.8,
     [4.5, 6, 5, 4.5, 1, 2, 1, 3.5, 1], []),
    ("Svijanský Rytíř", "pivovar-svijany", "Svijanský Rytíř 12°", "Czech pale lager", 12, 5.0,
     [5, 6, 5.5, 5, 1, 2, 1, 4, 1], ["closest regional match to Pilsner Urquell"]),
    ("Svijanská Kněžna", "pivovar-svijany", "Svijanská Kněžna 13°", "Czech pale special", 13, 5.6,
     [5, 7, 6.5, 4, 2, 3, 1, 4, 1], []),
    ("Svijany 450", "pivovar-svijany", "Svijany 450 11°", "Czech pale lager, unfiltered", 11, 4.8,
     [4.5, 6.5, 5.5, 4, 1, 3, 1, 4.5, 1], []),
    # ── Radegast ─────────────────────────────────────────────────────────
    ("Radegast Originál", "pivovar-radegast", "Radegast Originál 12°", "Czech pale lager", 12, 4.0,
     [5.5, 5, 4.5, 6, 1, 1.5, 1, 3.5, 1], []),
    ("Radegast Ryze Hořká 12", "pivovar-radegast", "Radegast Ryze hořká 12°", "Czech pale lager", 12, 4.7,
     [8, 4.5, 4.5, 7, 1, 1.5, 1, 4.5, 1], ["the most bitter mainstream Czech lager"]),
    # ── Budvar ───────────────────────────────────────────────────────────
    ("Budweiser Budvar Original", "budejovicky-budvar", "Budvar 12°", "Czech pale lager", 12, 5.0,
     [5, 6.5, 5.5, 4.5, 1, 3, 1, 4, 1], ["rounder and sweeter than Pilsner Urquell"]),
    ("Budvar Tmavý ležák", "budejovicky-budvar", "Budvar tmavý ležák", "Czech dark lager", 12, 4.7,
     [4, 7.5, 6, 4, 6.5, 3, 1, 3, 1], []),
    # ── Krušovice ────────────────────────────────────────────────────────
    ("Krušovice Světlé", "kralovsky-pivovar-krusovice", "Krušovice 10°", "Czech pale lager", 10, 4.2,
     [3.5, 5.5, 4, 4.5, 1, 2, 1, 2.5, 1], []),
    ("Krušovice Černé", "kralovsky-pivovar-krusovice", "Krušovice Černé", "Czech dark lager", 10, 3.8,
     [3, 8, 5.5, 3, 6, 2, 1, 2, 1], []),
    # ── прочие региональные с пражскими точками ──────────────────────────
    ("Březňák Světlý ležák", "breznak", "Březňák 12°", "Czech pale lager", 12, 4.9,
     [5.5, 5.5, 5, 5.5, 1, 2, 1, 4, 1], []),
    ("Klášter Ležák", "pivovar-klaster", "Klášter 11°", "Czech pale lager", 11, 4.6,
     [4.5, 6, 5, 5, 1, 2, 1, 3.5, 1], []),
    ("Konrád 12", "konrad", "Konrád 12°", "Czech pale lager", 12, 5.0,
     [5, 5.5, 5, 5, 1, 2, 1, 4, 1], []),
    ("Braník Světlé výčepní", "pivovar-branik", "Braník 10°", "Czech pale lager", 10, 4.1,
     [3.5, 5, 4, 5, 1, 2, 1, 2.5, 1], []),
    ("Rychtář Fojt", "pivovar-rychtar", "Rychtář Fojt 12°", "Czech pale lager", 12, 5.0,
     [5, 6, 5, 5, 1, 2, 1, 3.5, 1], []),
    ("Cvikov Sklář", "pivovar-cvikov", "Cvikov Sklář 11°", "Czech pale lager", 11, 4.6,
     [5, 5.5, 4.5, 5.5, 1, 2, 1, 4, 1], []),
    ("Hubertus Premium", "hubertus", "Hubertus 11°", "Czech pale lager", 11, 4.8,
     [4.5, 6, 5, 4.5, 1, 2, 1, 3, 1], []),
    ("Černá Hora Ležák", "pivovar-cerna-hora", "Černá Hora 11°", "Czech pale lager", 11, 4.8,
     [5, 6, 5, 5, 1, 2, 1, 3.5, 1], []),
    # ── крафт ────────────────────────────────────────────────────────────
    ("Matuška Raptor", "matuska", "Matuška Raptor IPA", "American IPA", None, 6.3,
     [8, 4, 5, 6.5, 1, 5, 1, 9, 8.5], ["BrewDog Punk IPA"]),
    ("Matuška Zlatá Raketa", "matuska", "Matuška Zlatá raketa", "American pale ale", None, 5.4,
     [7, 4.5, 5, 6, 1, 4.5, 1, 8, 8], []),
]

# Международные якоря. Пива здесь не наливают — они существуют только как
# точка отсчёта: «как X, но …». Оттого и не подпадают под правило публикации.
ANCHORS = [
    ("Guinness Draught", "guinness", "Guinness", "Irish dry stout", None, 4.2,
     [5.5, 4, 5, 8, 9, 2, 2, 2, 1]),
    ("Stella Artois", "stella-artois", "Stella Artois", "Euro pale lager", None, 5.0,
     [4, 4.5, 3.5, 5.5, 1, 1.5, 1, 2, 1.5]),
    ("Corona Extra", None, "Corona", "Pale lager", None, 4.5,
     [1.5, 3.5, 2.5, 5, 1, 1.5, 1.5, 1, 1]),
    ("Heineken", None, "Heineken", "Euro pale lager", None, 5.0,
     [3.5, 4, 3.5, 5, 1, 2.5, 1, 2.5, 2]),
    ("BrewDog Punk IPA", None, "Punk IPA", "American IPA", None, 5.6,
     [7.5, 4, 4.5, 6.5, 1, 5, 1, 8.5, 9]),
    ("Hoegaarden", None, "Hoegaarden", "Witbier", None, 4.9,
     [2, 5, 4, 4, 1, 6, 3, 2, 2]),
    ("Weihenstephaner Hefeweissbier", None, "Hefeweizen", "German wheat beer", None, 5.4,
     [2, 6, 5.5, 3.5, 1, 7.5, 2, 2, 1]),
]


def slug(s):
    import re
    tr = str.maketrans("áčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ", "acdeeinorstuuyzACDEEINORSTUUYZ")
    return re.sub(r"[^a-z0-9]+", "-", s.translate(tr).lower()).strip("-")


def flavour(vals):
    return {"value": dict(zip(AXES, vals)), "method": "inferred",
            "source": "выведено из стиля и параметров", "checkedAt": TODAY}


def num(v):
    return None if v is None else {"value": v, "method": "unverified"}


def text(bid):
    """Авторский текст страницы. Провенанса нет — это не извлечённый факт."""
    out = {}
    if bid in LEADS:
        lead = {"en": LEADS[bid]}
        if bid in LEADS_CS:
            lead["cs"] = LEADS_CS[bid]
        out["lead"] = lead
    if bid in NOTES:
        cs = dict(zip([h for h, _ in NOTES[bid]], NOTES_CS.get(bid, [])))
        notes = []
        for i, (h, b) in enumerate(NOTES[bid]):
            src = NOTES_CS.get(bid, [])
            heading, body = {"en": h}, {"en": b}
            if i < len(src):
                heading["cs"], body["cs"] = src[i][0], src[i][1]
            notes.append({"heading": heading, "body": body})
        out["notes"] = notes
    return out


def main():
    beers = []
    for name, bid, cs, style, plato, abv, vals, likes in ROWS:
        beers.append({
            "id": slug(name), "breweryId": bid, "name": name, "menuNameCs": cs,
            "style": style, "plato": num(plato), "abv": num(abv),
            "flavour": flavour(vals), "tastesLike": likes,
            "availability": "core", "isAnchor": False,
            **text(slug(name)),
        })
        beers[-1]["production"] = {loc: brewing_derive.build(beers[-1], dict(zip(AXES, vals)), loc)
                                  for loc in ("en", "cs")}
    for name, bid, cs, style, plato, abv, vals in ANCHORS:
        beers.append({
            "id": slug(name), "breweryId": bid, "name": name, "menuNameCs": cs,
            "style": style, "plato": num(plato), "abv": num(abv),
            "flavour": flavour(vals), "tastesLike": [],
            "availability": "core", "isAnchor": True,
            **text(slug(name)),
        })
        beers[-1]["production"] = {loc: brewing_derive.build(beers[-1], dict(zip(AXES, vals)), loc)
                                  for loc in ("en", "cs")}

    out = ROOT / "data" / "beers.json"
    out.write_text(json.dumps(beers, ensure_ascii=False, indent=1), encoding="utf-8")
    czech = [b for b in beers if not b["isAnchor"]]
    print(f"записано: data/beers.json — {len(beers)} записей "
          f"({len(czech)} чешских, {len(beers) - len(czech)} якорей)")
    print("  все числа: unverified   все профили: inferred")
    br = sum(1 for b in beers if b["production"]["en"]["hasBrewery"])
    print(f"  технология: {br}/{len(beers)} с данными пивоварни, остальные — типовое для стиля")
    no_cs = [b["name"] for b in beers if "cs" not in (b.get("lead") or {})]
    print(f"  чешских описаний: {len(beers) - len(no_cs)}/{len(beers)}"
          + (f"   без CS: {', '.join(no_cs)}" if no_cs else ""))
    missing = [b["name"] for b in beers if "lead" not in b]
    print(f"  с описанием: {len(beers) - len(missing)}/{len(beers)}"
          + (f"   без описания: {', '.join(missing)}" if missing else ""))


if __name__ == "__main__":
    main()
