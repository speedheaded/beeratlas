"""
Технология: как это сварено.

Два уровня достоверности, и они не смешиваются:

    level="brewery"  — известно про эту конкретную пивоварню
    level="style"    — так обычно делают пиво этого стиля; для этого сорта
                       не подтверждено

Второй уровень честнее пустоты и честнее выдумки: читатель узнаёт, как
устроен чешский лагер вообще, и видит, что про его кружку конкретно мы этого
не проверяли. Всё вместе остаётся `unverified`, пока не сверено с пивоварней.

PROCESS — общий разбор цепочки, один на весь сайт: он одинаков для всех
чешских лагеров, и повторять его на тридцати страницах было бы и скучно, и
вредно для поиска.
"""

# ── общий разбор процесса (страница #/brewing) ─────────────────────────────

PROCESS = [
    ("Malt and water become wort",
     "Crushed malt is mixed with hot water so the grain's own enzymes can break its starch "
     "into fermentable sugar. Czech breweries do this by <b>decoction</b>: part of the mash is "
     "drawn off, boiled separately, and returned to raise the whole batch to the next "
     "temperature step. Two or three decoctions are normal here where most of the world uses a "
     "single infusion — it is slower, costs more energy, and gives the bready, faintly honeyed "
     "malt character that Czech lager is recognised by."),
    ("The grain is separated out",
     "The sweet liquid — <b>wort</b> — is drained off the spent grain, which goes to cattle. "
     "What is left in the kettle is sugar, protein and minerals, and no beer yet."),
    ("Boiling with hops",
     "The wort is boiled and hops go in, usually in several additions. Early hops give "
     "bitterness, late hops give aroma. Czech pale lager leans on <b>Saaz</b> — Žatecký "
     "poloraný červeňák — a low-alpha aroma hop with a herbal, faintly spicy character. Its "
     "low alpha content is why a Czech 12° can taste firmly bitter without ever tasting "
     "resinous the way a modern IPA does."),
    ("Cold fermentation with bottom yeast",
     "The wort is cooled to around 6 °C, aerated and pitched with lager yeast, which works at "
     "the bottom of the vessel and at temperatures an ale yeast would refuse. Primary "
     "fermentation runs six to ten days at roughly 8–12 °C. Slow and cold produces a clean "
     "profile: none of the banana and clove esters a warm ale ferment throws. Some Czech "
     "breweries still use <b>open fermentation vessels</b> — square open-topped tanks in a cold "
     "cellar, which is how it was done before the pressure tank."),
    ("Lagering — the part the beer is named after",
     "<em>Lagern</em> is German for &ldquo;to store&rdquo;. The green beer goes into horizontal "
     "tanks at about 2 °C and sits there for weeks: three to four for an everyday 10°, six to "
     "twelve for a serious 12°, and famously around ninety days at Budvar. During that time it "
     "clears, softens, carbonates naturally from residual fermentation, and loses the harsh "
     "notes of young beer. This long cold rest is the single biggest difference between "
     "traditional Czech lager and industrially accelerated lager."),
    ("Filtered, unfiltered, pasteurised, unpasteurised",
     "These are two separate questions and they are constantly confused. <b>Filtration</b> "
     "removes yeast and haze — kieselguhr filtration, sometimes followed by microfiltration. "
     "<b>Pasteurisation</b> heats the finished beer to kill what survives, trading some "
     "freshness for shelf life. A beer can be filtered but unpasteurised, which is what most "
     "&ldquo;nepasterizované&rdquo; on a Czech label means: it has been cleared, but never "
     "heated. Tank beer in a pub is normally both unpasteurised and delivered within days."),
    ("Why the number on the menu is not alcohol",
     "The degree is <b>degrees Plato</b>: the percentage by weight of dissolved sugar in the "
     "wort before fermentation. Yeast converts roughly half of it to alcohol, so the finished "
     "strength lands near a third of the number — an 11° comes out around 4.6 %. Breweries can "
     "also push the balance: adding a little sugar to the boil raises the alcohol without "
     "adding body, which is how some 11° beers stay unusually light on the palate."),
]

# ── по сортам ──────────────────────────────────────────────────────────────
# ключи: water malt adjuncts hops mash ferment primary lagerTemp lagerDays
#        filtration pasteurised note level

P = {}

P["pilsner-urquell"] = dict(
    level="brewery",
    water="Soft Plzeň water, very low in mineral salts — the reason the hop bitterness lands "
          "clean rather than harsh.",
    malt="Moravian floor-malted barley.",
    hops="Saaz (Žatecký poloraný červeňák), whole cone.",
    mash="Triple decoction — three separate portions of mash boiled and returned. Almost "
         "nobody does this at scale any more.",
    ferment="Historically open vessels in the sandstone cellars; a small parallel batch is "
            "still fermented and lagered there in wooden barrels for comparison.",
    lagerDays="weeks, in horizontal tanks",
    filtration="Filtered for bottle and can; tank beer is delivered unfiltered of character "
               "and unpasteurised.",
    note="The cellar comparison batch is the reason the brewery can tell you what it is "
         "supposed to taste like. If you take the brewery tour in Plzeň, the unfiltered, "
         "unpasteurised beer straight from a cellar barrel is the whole point of going.",
)

P["pilsner-urquell-nefiltrovana"] = dict(
    level="brewery",
    malt="Same grist as the filtered version.",
    hops="Saaz.",
    mash="Triple decoction.",
    filtration="Unfiltered — the yeast stays in, which is where the haze and the softer mouthfeel come from.",
    pasteurised=False,
    note="Unfiltered and unpasteurised are different things, and this beer is both. Expect a "
         "rounder body and a faint bready yeast note the filtered version does not have.",
)

P["svijansky-maz"] = dict(
    level="brewery",
    water="From the brewery's own wells.",
    malt="Floor-malted barley — <em>humnový slad</em> — bought from small independent maltings "
         "in Bohemia and Moravia. Floor malting is the slow traditional method, and it is where "
         "the bready, faintly honeyed base comes from.",
    adjuncts="A small amount of sugar in the boil. Not for sweetness — the yeast eats it "
             "almost entirely, so it raises alcohol while keeping the body light. It is why an "
             "11° wort finishes at 4.8 % and still drinks easily.",
    hops="Saaz from the brewery's own hop gardens in the Polepské blaty, plus hop extract for "
         "precise control of bitterness.",
    mash="Double decoction.",
    ferment="Open fermentation vessels, up to about 12 °C, six to eight days.",
    lagerTemp="≈ 2 °C",
    lagerDays="30–60 days depending on the beer",
    filtration="Kieselguhr filtration followed by microfiltration.",
    pasteurised=False,
    note="Unpasteurised does not mean live yeast in the bottle here — the beer is filtered "
         "thoroughly, just never heated.",
)

P["svijansky-rytir"] = dict(
    level="brewery",
    water="Brewery's own wells.", malt="Floor-malted barley.",
    hops="Saaz from the brewery's own gardens.",
    mash="Double decoction.",
    ferment="Open vessels, up to about 12 °C.",
    lagerTemp="≈ 2 °C", lagerDays="30–60 days",
    filtration="Kieselguhr and microfiltration.", pasteurised=False,
)

P["svijanska-knezna"] = dict(level="brewery", mash="Double decoction.", ferment="Open vessels.",
                             lagerTemp="≈ 2 °C", lagerDays="longer than the everyday range",
                             pasteurised=False, hops="Saaz.")
P["svijany-450"] = dict(level="brewery", mash="Double decoction.", ferment="Open vessels.",
                        filtration="Unfiltered.", pasteurised=False, hops="Saaz.",
                        note="Unfiltered and unpasteurised both — as close to the fermenting "
                             "cellar as this brewery's beer gets in a bottle.")

P["budweiser-budvar-original"] = dict(
    level="brewery",
    water="From the brewery's own artesian wells, drawn from a deep aquifer under České "
          "Budějovice.",
    malt="Moravian barley malt.",
    hops="Saaz.",
    lagerTemp="≈ 2 °C",
    lagerDays="around 90 days — roughly three times the industry norm",
    note="The ninety-day lagering is the brewery's central claim and the most plausible "
         "explanation for the beer's roundness: the long cold rest is where harshness goes and "
         "carbonation arrives naturally.",
)

P["uneticka-12"] = dict(
    level="brewery",
    malt="Floor-malted Czech barley.",
    hops="Saaz.",
    mash="Decoction.",
    ferment="Open fermentation vessels.",
    filtration="Unfiltered.",
    pasteurised=False,
    note="The brewery sells its beer unfiltered and unpasteurised and does not distribute far, "
         "which is a deliberate trade: freshness in exchange for range.",
)
P["uneticka-10"] = dict(level="brewery", ferment="Open vessels.", filtration="Unfiltered.",
                        pasteurised=False, hops="Saaz.", mash="Decoction.")
P["uneticka-tmava-12"] = dict(level="brewery", ferment="Open vessels.", filtration="Unfiltered.",
                              pasteurised=False, mash="Decoction.",
                              malt="Pale barley malt with roasted and caramel malts for colour "
                                   "and the coffee note.")

P["kozel-cerny"] = dict(
    level="brewery",
    malt="Pale malt with caramel and roasted malts. The caramel malt is doing most of the work: "
         "it brings colour and sweetness but very little of the dry roast a stout gets from "
         "roasted barley.",
    hops="Saaz, restrained.",
    note="This is the technical reason it disappoints people expecting Guinness. A dry stout "
         "gets its character from unmalted roasted barley and a nitrogen pour; this gets its "
         "character from caramel malt and normal CO₂.",
)

P["matuska-raptor"] = dict(
    level="brewery",
    malt="Pale ale malt base, kept light so the hops have room.",
    hops="American varieties, with a large late and dry-hop charge — hops added after "
         "fermentation, which contributes aroma but no bitterness.",
    ferment="Ale yeast, warm — the opposite of everything else on this site.",
    note="Dry hopping is the difference between an IPA and a strongly hopped lager: bitterness "
         "comes from the boil, but that grapefruit and pine smell comes from hops that never "
         "saw a kettle.",
)
P["matuska-zlata-raketa"] = dict(level="brewery", hops="American varieties, dry hopped.",
                                 ferment="Ale yeast, warm fermentation.")

P["radegast-ryze-horka-12"] = dict(
    level="brewery",
    hops="Hopped noticeably harder than the mainstream Czech norm — the entire positioning of "
         "the beer is bitterness.",
    note="Marketed on bitterness in a market that sells smoothness. If a Czech lager has ever "
         "tasted too soft to you, this is the one built for that complaint.",
)

# ── типовое для стиля ──────────────────────────────────────────────────────

STYLE = {
    "Czech pale lager": dict(
        level="style",
        malt="Czech barley malt, usually pale Pilsner malt alone.",
        hops="Saaz or another Czech aroma hop.",
        mash="Decoction — typically double — rather than a single infusion.",
        ferment="Bottom-fermenting lager yeast, roughly 8–12 °C, six to ten days.",
        lagerTemp="≈ 2 °C",
        lagerDays="three weeks for a 10°, six or more for a 12°",
        filtration="Normally filtered.",
    ),
    "Czech pale lager, unfiltered": dict(
        level="style",
        malt="Czech pale barley malt.", hops="Saaz.",
        mash="Decoction.", ferment="Lager yeast, 8–12 °C.",
        lagerTemp="≈ 2 °C", lagerDays="several weeks",
        filtration="Unfiltered — the haze and the softer body are the yeast still in suspension.",
    ),
    "Czech dark lager": dict(
        level="style",
        malt="Pale malt with caramel and roasted malts for colour and sweetness.",
        hops="Saaz, held back so the malt leads.",
        mash="Decoction.", ferment="Lager yeast, 8–12 °C.",
        lagerTemp="≈ 2 °C", lagerDays="several weeks",
    ),
    "Czech amber lager": dict(
        level="style",
        malt="Pale and caramel malt — halfway between the pale and the dark.",
        hops="Saaz.", mash="Decoction.", ferment="Lager yeast, 8–12 °C.",
        lagerTemp="≈ 2 °C", lagerDays="several weeks",
    ),
    "Czech pale special": dict(
        level="style",
        malt="A heavier grist than an everyday lager — more malt in, more alcohol out.",
        hops="Saaz.", mash="Decoction.", ferment="Lager yeast, 8–12 °C.",
        lagerTemp="≈ 2 °C", lagerDays="longer than the everyday range",
    ),
    "American IPA": dict(
        level="style",
        malt="Light pale malt base.",
        hops="New World varieties, heavily late-hopped and dry hopped.",
        ferment="Ale yeast, warm.", filtration="Often unfiltered.",
    ),
    "American pale ale": dict(
        level="style", malt="Pale malt base.", hops="New World varieties, dry hopped.",
        ferment="Ale yeast, warm.",
    ),
}

LABELS = [
    ("water", "Water"), ("malt", "Malt"), ("adjuncts", "Adjuncts"), ("hops", "Hops"),
    ("mash", "Mashing"), ("ferment", "Fermentation"),
    ("lagerTemp", "Lagering temperature"), ("lagerDays", "Lagering time"),
    ("filtration", "Filtration"),
]


# ── что известно про остальные пивоварни ───────────────────────────────────
# Немного, но это правда, и это лучше, чем правдоподобная выдумка.

_PRAZDROJ_GROUP = ("Part of the Plzeňský Prazdroj group and brewed to its process: "
                   "Czech malt, Saaz hops, decoction mashing and cold lagering.")

for _id in ("gambrinus-original-10", "gambrinus-original-11"):
    P[_id] = dict(level="brewery", hops="Saaz.", mash="Decoction.",
                  note=_PRAZDROJ_GROUP + " Brewed in the same Plzeň brewhouse as Pilsner "
                       "Urquell and deliberately built softer.")
for _id in ("kozel-svetly", "kozel-11"):
    P[_id] = dict(level="brewery", hops="Saaz.", mash="Decoction.", note=_PRAZDROJ_GROUP)
P["radegast-original"] = dict(level="brewery", hops="Saaz, used more assertively than the "
                              "Czech norm.", mash="Decoction.", note=_PRAZDROJ_GROUP)

for _id in ("staropramen-svetly", "staropramen-lezak", "staropramen-granat"):
    P[_id] = dict(level="brewery", hops="Czech aroma hops.", mash="Decoction.",
                  note="Brewed in Smíchov, inside Prague, which makes it the shortest journey "
                       "from brewhouse to tap in the city.")
P["staropramen-granat"]["malt"] = ("Pale and caramel malt. The caramel fraction is what puts "
                                   "it between the pale and the dark rather than in either.")

P["krusovice-svetle"] = dict(level="brewery", hops="Saaz.", mash="Decoction.")
P["krusovice-cerne"] = dict(level="brewery", hops="Saaz, restrained.", mash="Decoction.",
                            malt="Pale malt with caramel and roasted malt.")
P["budvar-tmavy-lezak"] = dict(level="brewery", hops="Saaz.",
                               malt="Pale malt with roasted and caramel malts.",
                               lagerTemp="≈ 2 °C", lagerDays="long, as across the range",
                               note="Budvar lagers its beers considerably longer than the "
                                    "industry norm, and the dark one is no exception.")


# ── длительности в днях, для шкалы времени ─────────────────────────────────
# Время — самое наглядное в чешском лагере: неделя брожения против полутора
# месяцев лежания. Числа те же, что в текстовых полях, только машиночитаемо.

DAYS = {
    "svijansky-maz":    dict(ferment=(6, 8), lager=(30, 60)),
    "svijansky-rytir":  dict(ferment=(6, 8), lager=(30, 60)),
    "svijanska-knezna": dict(ferment=(6, 8), lager=(45, 60)),
    "svijany-450":      dict(ferment=(6, 8), lager=(30, 60)),
    "budweiser-budvar-original": dict(ferment=(7, 10), lager=(90, 90)),
    "budvar-tmavy-lezak":        dict(ferment=(7, 10), lager=(60, 90)),
}

# типовое для стиля — от плотности: чем крепче сусло, тем дольше лежит
STYLE_DAYS = {
    "Czech pale lager":             dict(ferment=(6, 10), lager=(21, 45)),
    "Czech pale lager, unfiltered": dict(ferment=(6, 10), lager=(21, 45)),
    "Czech dark lager":             dict(ferment=(6, 10), lager=(21, 45)),
    "Czech amber lager":            dict(ferment=(6, 10), lager=(21, 45)),
    "Czech pale special":           dict(ferment=(7, 10), lager=(45, 70)),
    "American IPA":                 dict(ferment=(4, 7),  lager=(7, 14)),
    "American pale ale":            dict(ferment=(4, 7),  lager=(7, 14)),
    "Irish dry stout":              dict(ferment=(4, 6),  lager=(7, 14)),
    "Euro pale lager":              dict(ferment=(6, 10), lager=(14, 28)),
    "Pale lager":                   dict(ferment=(6, 10), lager=(14, 28)),
    "Witbier":                      dict(ferment=(4, 7),  lager=(7, 14)),
    "German wheat beer":            dict(ferment=(4, 7),  lager=(7, 14)),
}

# Что происходит на каждом шаге — общий текст, привязанный к этапу.
STAGE_WHAT = {
    "mash":    ("Mashing", "Starch becomes sugar",
                "Crushed malt meets hot water and the grain's own enzymes cut its starch into "
                "fermentable sugar. The result is <b>wort</b>: sweet, hopless, not yet beer."),
    "boil":    ("Boil and hops", "Bitterness and aroma arrive",
                "The wort is boiled and hops go in. Early additions give bitterness, late ones "
                "give aroma. Nothing else in the process adds either."),
    "ferment": ("Fermentation", "Sugar becomes alcohol",
                "Cooled to about 6 °C and pitched with bottom-fermenting yeast. Sugar turns into "
                "alcohol and CO₂; cold and slow keeps the profile clean."),
    "lager":   ("Lagering", "Time does the rest",
                "The green beer rests cold in horizontal tanks. It clears, softens, carbonates "
                "naturally and loses the harshness of young beer. This is the step industrial "
                "brewing cuts first."),
    "finish":  ("Finishing", "Clearing and packaging",
                "Filtration removes yeast and haze. Pasteurisation — heating the finished beer — "
                "is a separate decision, and plenty of Czech beer skips it."),
}
