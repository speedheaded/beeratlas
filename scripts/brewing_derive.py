"""
Technologická část stránky piva — двуязычная.

Ничего о пивоварне не выдумывается: шаги без подтверждённых данных помечаются
как типовые для стиля. Выведенные абзацы считаются из чисел самого сорта:

    zbytkový extrakt  AE = OE − ABV / 0.5162
    prokvašení       ADF = (OE − AE) / OE
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import brewing_text as EN          # noqa: E402
import brewing_text_cs as CS       # noqa: E402

MOD = {"en": EN, "cs": CS}
ING_ICON = {"water": "drop", "malt": "grain", "adjuncts": "sugar", "hops": "hop"}


def attenuation(oe, abv):
    if not oe or not abv:
        return None
    ae = oe - abv / 0.5162
    return {"oe": round(oe, 1), "ae": round(ae, 1), "adf": round((oe - ae) / oe * 100)}


# ── выведенные абзацы ─────────────────────────────────────────────────────

def _body(a, loc):
    adf, ae = a["adf"], a["ae"]
    if loc == "cs":
        if adf >= 82:
            return (f"Kvasnice to dotáhly hodně nízko — prokvasilo zhruba <b>{adf}&nbsp;%</b> "
                    f"mladiny a ve sklenici zůstalo asi <b>{ae}°</b> extraktu. Proto se pivo "
                    f"pije lehčeji, než jeho stupňovitost napovídá: alkohol tu je, plnost ne.")
        if adf >= 76:
            return (f"Kvašení došlo zhruba k <b>{adf}&nbsp;%</b> a zůstalo kolem <b>{ae}°</b> "
                    f"zbytkového extraktu — běžná česká rovnováha, dost sladu na to, aby pivo "
                    f"neslo, a ne tolik, aby tížilo.")
        if adf >= 70:
            return (f"Kvašení se zastavilo poměrně brzy, kolem <b>{adf}&nbsp;%</b>, a v pivu "
                    f"zůstalo asi <b>{ae}°</b>. Ten nezkvašený slad cítíte jako plnost, a proto "
                    f"tohle chutná plněji než piva stejné síly.")
        return (f"Prokvasilo jen asi <b>{adf}&nbsp;%</b> mladiny a zůstalo zhruba <b>{ae}°</b> "
                f"— hodně sladu pořád ve sklenici. Čekejte znatelnou váhu vůči alkoholu.")
    if adf >= 82:
        return (f"The yeast took it a long way down — about <b>{adf}&nbsp;%</b> of the wort "
                f"fermented out, leaving roughly <b>{ae}°</b> in the glass. That is why it drinks "
                f"lighter than its gravity suggests: the alcohol is there, the body is not.")
    if adf >= 76:
        return (f"Fermentation ran to about <b>{adf}&nbsp;%</b>, leaving around <b>{ae}°</b> of "
                f"residual extract — the ordinary Czech balance, enough malt left to carry the "
                f"beer without weighing it down.")
    if adf >= 70:
        return (f"Fermentation stopped comparatively early, near <b>{adf}&nbsp;%</b>, and about "
                f"<b>{ae}°</b> stayed in the beer. That unfermented malt is what you feel as "
                f"body, and it is why this tastes fuller than beers of the same strength.")
    return (f"Only about <b>{adf}&nbsp;%</b> of the wort fermented, leaving roughly <b>{ae}°</b> "
            f"behind — a lot of malt still in the glass. Expect real weight relative to the alcohol.")


def _hop(f, oe, loc):
    bit, prof = f["bitterness"], f["hopProfile"]
    r = bit / (oe / 12) if oe else bit
    if loc == "cs":
        if prof >= 6:
            return ("Chmel je novosvětský, ne český: velká část aromatu pochází z chmele "
                    "přidaného po kvašení, ne ve varně — hořkost z kotle, vůně ze studeného "
                    "chmelení.")
        if r >= 7:
            return ("Chmeleno tvrdě na svou stupňovitost. V zemi, která prodává jemnost, je "
                    "tohle záměrná výjimka: hořkost je tu produkt, ne vedlejší efekt.")
        if r >= 5.5:
            return ("Podle mezinárodních měřítek pevně chmeleno, podle českých normálně. "
                    "Žatecký chmel má málo alfa kyselin, a tak se ho dává štědře — hořkost "
                    "doznívá, aniž by kdy zpryskyřičněla.")
        if r >= 3.5:
            return ("Chmeleno spíš pro rovnováhu než pro efekt. Žatecký charakter se ozve víc "
                    "v aromatu než v závěru.")
        return ("Chmeleno velmi lehce. Vede slad a chmel je tu od toho, aby pivo nechutnalo "
                "sladce, ne aby byl sám cítit.")
    if prof >= 6:
        return ("The hops are New World rather than Czech, and much of the aroma comes from hops "
                "added after fermentation rather than in the kettle — bitterness from the boil, "
                "smell from the dry hop.")
    if r >= 7:
        return ("Hopped hard for its gravity. In a country that sells smoothness this is the "
                "deliberate exception: the bitterness is the product, not a by-product.")
    if r >= 5.5:
        return ("Firmly hopped by international standards and normal by Czech ones. Saaz is low "
                "in alpha acid, so it is used generously — the bitterness lingers without ever "
                "turning resinous.")
    if r >= 3.5:
        return ("Hopped for balance rather than statement. The Saaz character shows in the aroma "
                "more than in the finish.")
    return ("Very lightly hopped. The malt leads, and the hop is here to stop the beer tasting "
            "sweet rather than to be tasted itself.")


def _malt(f, loc):
    roast, sweet = f["roast"], f["maltSweetness"]
    if loc == "cs":
        if roast >= 6:
            return ("Barva a kávový tón pocházejí z pražených a karamelových sladů na světlém "
                    "základu. Karamelový slad přináší sladkost s barvou, pražený suchou hranu — "
                    "a který z nich vede, je celý rozdíl mezi českým tmavým ležákem a stoutem.")
        if roast >= 3.5:
            return ("Zlomek karamelového sladu v jinak světlé sypanině: dost na barvu a "
                    "karamelový tón, málo na praženost.")
        if sweet >= 6.5:
            return ("Sladově vedená světlá sypanina. Český humnový ječný slad je zdrojem "
                    "chlebového, lehce medového základu, a rmutování ho prohlubuje.")
        return ("Přímočará světlá sypanina — český plzeňský slad dělá všechnu práci, a to je "
                "nejtěžší druh piva, ve kterém se dá něco schovat.")
    if roast >= 6:
        return ("Colour and the coffee note come from roasted and caramel malt on a pale base. "
                "Caramel malt brings sweetness with the colour, roasted malt brings the dry edge "
                "— which of the two leads is the whole difference between a Czech dark lager and "
                "a stout.")
    if roast >= 3.5:
        return ("A fraction of caramel malt in an otherwise pale grist: enough for the colour and "
                "a toffee note, not enough for roast.")
    if sweet >= 6.5:
        return ("A malt-forward pale grist. Czech floor-malted barley is where the bready, faintly "
                "honeyed base comes from, and decoction mashing deepens it.")
    return ("A straightforward pale grist — Czech Pilsner malt doing all the work, which is the "
            "hardest kind of beer to hide anything in.")


# ── сборка ────────────────────────────────────────────────────────────────

def build(beer, flavour, loc="en"):
    m = MOD[loc]
    oe = (beer.get("plato") or {}).get("value")
    abv = (beer.get("abv") or {}).get("value")

    known = m.P.get(beer["id"])
    known_en = EN.P.get(beer["id"])            # уровень достоверности берём из основного
    spec = {**m.STYLE.get(beer["style"], {}), **(known or {})}
    if known_en and known_en.get("pasteurised") is False:
        spec["pasteurised"] = False

    days = {**EN.style_days(beer["style"], (beer.get("plato") or {}).get("value")),
            **EN.DAYS.get(beer["id"], {})}
    days_known = beer["id"] in EN.DAYS

    def lvl(key):
        return "brewery" if known_en and key in known_en else "style"

    ingredients = [{"k": label, "v": spec[key], "icon": ING_ICON[key], "lvl": lvl(key)}
                   for key, label in m.LABELS if key in ING_ICON and spec.get(key)]

    def stage(sid, params, note=None, rng=None):
        name, what, body = m.STAGE_WHAT[sid]
        return {"id": sid, "name": name, "what": what, "body": body,
                "params": [p for p in params if p["v"]], "note": note, "days": rng}

    lab = dict(m.LABELS)
    stages = [
        stage("mash", [{"k": lab["mash"], "v": spec.get("mash"), "lvl": lvl("mash")}]),
        stage("boil", [{"k": lab["hops"], "v": spec.get("hops"), "lvl": lvl("hops")}],
              note=_hop(flavour, oe, loc)),
        stage("ferment", [{"k": lab["ferment"], "v": spec.get("ferment"), "lvl": lvl("ferment")}],
              note=_body(attenuation(oe, abv), loc) if oe and abv else None,
              rng=days.get("ferment")),
        stage("lager", [{"k": lab["lagerTemp"], "v": spec.get("lagerTemp"), "lvl": lvl("lagerTemp")},
                        {"k": lab["lagerDays"], "v": spec.get("lagerDays"), "lvl": lvl("lagerDays")}],
              rng=days.get("lager")),
        stage("finish", [
            {"k": lab["filtration"], "v": spec.get("filtration"), "lvl": lvl("filtration")},
            {"k": "Pasterizace" if loc == "cs" else "Pasteurisation",
             "v": ((CS.PASTEUR_NO if loc == "cs" else "Unpasteurised — filtered but never heated.")
                   if spec.get("pasteurised") is False else None),
             "lvl": lvl("pasteurised")}]),
    ]

    f_lo, f_hi = days.get("ferment", (6, 10))
    l_lo, l_hi = days.get("lager", (21, 45))
    dn = "dní" if loc == "cs" else "days"
    timeline = {
        "brew": 1, "ferment": (f_lo + f_hi) / 2, "lager": (l_lo + l_hi) / 2,
        "fermentLabel": f"{f_lo}–{f_hi} {dn}" if f_lo != f_hi else f"{f_lo} {dn}",
        "lagerLabel": f"{l_lo}–{l_hi} {dn}" if l_lo != l_hi else f"{l_lo} {dn}",
        "total": round(1 + (f_lo + f_hi) / 2 + (l_lo + l_hi) / 2),
        "lvl": "brewery" if days_known else "style",
    }

    return {
        "attenuation": attenuation(oe, abv),
        "ingredients": ingredients,
        "maltLine": _malt(flavour, loc),
        "stages": stages,
        "timeline": timeline,
        "note": spec.get("note"),
        "hasBrewery": bool(known_en),
        "allBrewery": bool(known_en) and all(
            p["lvl"] == "brewery" for s in stages for p in s["params"]) and bool(ingredients),
    }
