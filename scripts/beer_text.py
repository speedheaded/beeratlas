"""
Тексты страниц сортов.

Это авторский контент, а не извлечённые данные, поэтому провенанса у него нет —
но и выдумывать в нём нечего: каждое утверждение либо общеизвестно, либо
согласовано с вектором вкуса. Задача текста одна: сказать туристу то, чего он
не найдёт на этикетке и о чём не догадается сам.

Структура на сорт:
    lead   — первый абзац страницы
    notes  — разделы ниже блока сравнения, только там, где есть что сказать
"""

L = {}   # id -> lead
N = {}   # id -> [(heading, body), ...]

# ── Plzeňský Prazdroj ──────────────────────────────────────────────────────
L["pilsner-urquell"] = (
    "The beer every other pale lager in the world is a copy of, brewed in Plzeň since "
    "1842. If you order one beer in Czechia, order this one first — everything else on "
    "the menu makes more sense once you know where the middle is.")
N["pilsner-urquell"] = [
    ("Why it tastes more bitter than you expected",
     "Saaz hops give a herbal, almost grassy bitterness that lingers, and the malt is "
     "kept dry underneath it. Next to an international lager it can seem severe for the "
     "first two mouthfuls, then stops seeming that way for good."),
    ("Tank and bottle are not the same drink",
     "Unpasteurised tank beer — <em>tankové</em> — is softer, fuller and noticeably fresher. "
     "Pubs that pour it advertise it, because it costs them more. It is the single biggest "
     "upgrade available to a visitor and usually costs nothing extra."),
]

L["pilsner-urquell-nefiltrovana"] = (
    "The same beer without filtration: hazier, rounder, with a soft yeast note the "
    "filtered version loses. Poured in a fraction of the pubs that carry the standard "
    "one, and worth crossing the river for if you have already had the ordinary Urquell.")

# ── Velké Popovice ─────────────────────────────────────────────────────────
L["kozel-svetly"] = (
    "The cheap everyday pour. Light, soft and made for drinking several over an "
    "afternoon rather than for thinking about. If a pub has one tap for locals and one "
    "for tourists, this is often the local one.")

L["kozel-11"] = (
    "A step up from the 10° in body and sweetness, and the version most people actually "
    "mean when they say they drink Kozel. Softer and maltier than Pilsner Urquell, with "
    "much less of the hop bite.")

L["kozel-cerny"] = (
    "The dark beer you will meet in almost every Prague pub, and the one most visitors "
    "order expecting a stout. It is not a stout — it is sweet, low in alcohol, and "
    "finishes clean rather than dry.")
N["kozel-cerny"] = [
    ("Is it like Guinness?",
     "No, and this is the most common disappointment in Prague. Guinness is dry, "
     "thin-bodied and poured with nitrogen; Kozel Černý is a sweet lager with caramel "
     "malt and normal carbonation. If you came for a stout, the closest thing on most "
     "Czech taps is a <em>tmavý speciál</em> at 13° — and you will usually have to leave "
     "the tourist centre to find one."),
]

# ── Gambrinus ──────────────────────────────────────────────────────────────
L["gambrinus-original-10"] = (
    "By volume, the beer Czechs actually drink. Unfashionable, cheap and everywhere — "
    "the pour you get when you walk into an ordinary neighbourhood pub and just say "
    "<em>pivo</em>.")

L["gambrinus-original-11"] = (
    "The middle Gambrinus: a little fuller and rounder than the 10°, still firmly an "
    "everyday beer. Brewed alongside Pilsner Urquell in Plzeň, and deliberately softer "
    "than it.")

# ── Staropramen ────────────────────────────────────────────────────────────
L["staropramen-svetly"] = (
    "Prague's own big brewery, on the river in Smíchov since 1869. The 10° is the light "
    "everyday version — inoffensive, widely available, and the beer most visitors drink "
    "without noticing they have.")

L["staropramen-lezak"] = (
    "The 12° lager, and the one worth ordering if the pub carries both. Fuller and "
    "hoppier than the 10°, though still gentler than a Plzeň lager.")

L["staropramen-granat"] = (
    "An amber lager sitting halfway between the pale and the dark: caramel sweetness, "
    "a little roast, no bitterness to speak of. A good answer if the dark beer sounds "
    "too heavy and the pale one too plain.")

# ── Únětický pivovar ───────────────────────────────────────────────────────
L["uneticka-10"] = (
    "From a village just outside Prague, unfiltered and quietly cult among locals. The "
    "10° is lighter than it tastes — a full, bready everyday beer at under 4 %.")

L["uneticka-12"] = (
    "Pilsner Urquell's shape, but unfiltered and rounder: the same firm Saaz bitterness "
    "with more body underneath and a yeast softness filtration would remove. One of the "
    "most rewarding beers within twenty minutes of the city.")

L["uneticka-tmava-12"] = (
    "The dark beer most visitors were hoping for when they ordered Kozel Černý: drier, "
    "properly roasted, with real coffee and dark bread rather than caramel syrup. Harder "
    "to find, and worth the walk.")

# ── Svijany ────────────────────────────────────────────────────────────────
L["svijansky-maz"] = (
    "The everyday Svijany, and the beer a Czech names when asked what they drink instead "
    "of the big three. Soft, malty, easy — brewed by a regional brewery small enough to "
    "feel local and large enough to be everywhere.")

L["svijansky-rytir"] = (
    "The 12° of the range and the closest regional answer to Pilsner Urquell: the same "
    "class of beer, a touch maltier and less sharp. If you liked the Urquell but wanted "
    "it a little gentler, this is the one.")

L["svijanska-knezna"] = (
    "A 13° special — fuller, sweeter and noticeably stronger than the everyday lagers, "
    "and still recognisably the same brewery. Order it late rather than first.")

L["svijany-450"] = (
    "The unfiltered Svijany, named for the brewery's anniversary. Hazier and softer than "
    "the Máz, with more of the yeast left in. Comes and goes from taps — ask rather than "
    "assume.")

# ── Radegast ───────────────────────────────────────────────────────────────
L["radegast-original"] = (
    "From Nošovice in Moravian Silesia, and the driest of the mainstream Czech lagers. "
    "Marketed on bitterness in a country that markets everything else on smoothness.")

L["radegast-ryze-horka-12"] = (
    "The most bitter beer you will find on an ordinary Czech tap — deliberately so. If "
    "Pilsner Urquell felt too soft to you, this is the correction; if it felt too bitter, "
    "walk past.")

# ── Budvar ─────────────────────────────────────────────────────────────────
L["budweiser-budvar-original"] = (
    "From České Budějovice — Budweis in German — and still state-owned. Rounder, sweeter "
    "and slower than Pilsner Urquell, with a long malty finish rather than a sharp one.")
N["budweiser-budvar-original"] = [
    ("Why it is not called Budweiser everywhere",
     "The brewery has been in a trademark dispute with the American Anheuser-Busch brand "
     "for over a century. In much of Europe the Czech beer is Budweiser; in the United "
     "States it is sold as Czechvar. They have nothing in common but the name."),
]

L["budvar-tmavy-lezak"] = (
    "The dark counterpart to the Original: caramel and dark bread with a genuine roasted "
    "edge, and drier than most Czech dark lagers. A good first dark beer for someone who "
    "found Kozel Černý too sweet.")

# ── Krušovice ──────────────────────────────────────────────────────────────
L["krusovice-svetle"] = (
    "A royal brewery by charter, a mass-market lager in practice. Soft, sweetish and "
    "undemanding — you will see it in tourist-facing places in the centre more often "
    "than in neighbourhood pubs.")

L["krusovice-cerne"] = (
    "Sweet, dark and low in alcohol, in the same family as Kozel Černý and with the same "
    "caveat: it is a dessert-leaning lager, not a stout.")

# ── прочие региональные ────────────────────────────────────────────────────
L["breznak-svetly-lezak"] = (
    "A North Bohemian lager with a firm, dry bitterness and a working-town reputation "
    "the brewery has never tried to shake. Straightforward and well made.")

L["klaster-lezak"] = (
    "A monastery brewery in Klášter Hradiště nad Jizerou, brewing a soft, malt-forward "
    "lager that goes down without argument. Common in pubs that want something other "
    "than the big four.")

L["konrad-12"] = (
    "From Vratislavice near Liberec — a balanced 12° that leans neither sweet nor "
    "aggressively bitter. The kind of beer a pub keeps because regulars never complain "
    "about it.")

L["branik-svetle-vycepni"] = (
    "Once Prague's own Braník brewery on the right bank; the brand survived the closure "
    "of the site. A light, cheap 10° with local sentiment attached to it.")

L["rychtar-fojt"] = (
    "From Hlinsko in the Bohemian-Moravian highlands. A clean, mid-weight 12° that "
    "appears in Prague pubs looking for a regional name rather than a corporate one.")

L["cvikov-sklar"] = (
    "A small North Bohemian brewery near the glassworks its beer is named after. Dry, "
    "firmly hopped, and a good example of what a regional 11° should taste like.")

L["hubertus-premium"] = (
    "From Kácov on the Sázava. Soft and malty with restrained bitterness — an easy pour "
    "for a long evening rather than a beer to study.")

L["cerna-hora-lezak"] = (
    "One of the older Moravian breweries, and a dependable middle-of-the-road 11°: enough "
    "malt to be interesting, enough hop to stay dry. Widely poured south of Brno and "
    "increasingly in Prague.")

# ── крафт ──────────────────────────────────────────────────────────────────
L["matuska-raptor"] = (
    "The beer that showed Czech drinkers what American hops do. Grapefruit and pine over "
    "a firm bitter spine, and still the reference IPA in a country that had none twenty "
    "years ago.")
N["matuska-raptor"] = [
    ("If you have been drinking lager all week",
     "This will taste enormous. That is the point, but it is not a session beer: at 6.3 % "
     "and with that much hop aroma, one is an event and three are a mistake."),
]

L["matuska-zlata-raketa"] = (
    "A pale ale rather than an IPA — the same New World hop character as the Raptor, "
    "turned down enough to drink more than one. A good bridge from Czech lager to Czech "
    "craft.")

# ── международные якоря ────────────────────────────────────────────────────
L["guinness-draught"] = (
    "Here only as a reference point. Dry, roasted, thin-bodied and poured with nitrogen — "
    "the opposite of what a Czech dark lager does, which is why ordering Kozel Černý "
    "expecting this ends badly.")

L["stella-artois"] = (
    "A reference point for a clean, mild European lager. Useful mainly as a marker of "
    "how much more bitter and malty a Czech 12° is.")

L["corona-extra"] = (
    "The lightest anchor in the atlas: barely bitter, barely bodied. If this is your idea "
    "of beer, start with a Czech 10° rather than a 12°.")

L["heineken"] = (
    "The international lager most visitors have a calibrated memory of. Everything Czech "
    "on this site is maltier and, above the 10° mark, considerably more bitter.")

L["brewdog-punk-ipa"] = (
    "The reference modern IPA: citrus and resin, high bitterness, dry finish. The "
    "yardstick for the Czech craft entries here.")

L["hoegaarden"] = (
    "A Belgian wheat beer — coriander, orange peel, no bitterness. There is nothing on a "
    "standard Czech tap like it, which is worth knowing before you go looking.")

L["weihenstephaner-hefeweissbier"] = (
    "A Bavarian wheat beer: banana and clove from the yeast, full and soft. Czech "
    "breweries do brew <em>pšeničné</em>, but it is a guest style here, not a native one.")
