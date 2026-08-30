"""
Тексты страниц пивоварен и точечные исправления к данным Wikidata.

Страница пивоварни, по оценке брифа, вероятно самая сильная по трафику из всех
типов — а до сих пор на ней стояла служебная заглушка. Здесь исправлено.

FIXES — отдельный уровень достоверности: `curated`. Wikidata иногда отдаёт дату
регистрации нынешнего юрлица вместо года основания пивоварни (Staropramen: 2012
вместо 1869). Такие значения переопределяются вручную и помечаются как
курируемые, а не выдаются за официальные.
"""

# id -> (первый абзац, [(заголовок, текст), ...])
S = {}

S["plzensky-prazdroj"] = (
    "The brewery that invented pale lager. In 1842 the burghers of Plzeň, fed up with "
    "undrinkable beer, hired a Bavarian brewer, dug cellars into sandstone and produced "
    "the first golden bottom-fermented beer anyone had seen. Every lager on earth is "
    "descended from what came out of those cellars.",
    [("Why it still matters to a visitor",
      "Almost every Czech pale lager you will be offered defines itself against this one — "
      "softer than it, maltier than it, more bitter than it. Drink it early in the trip and "
      "the rest of the menu becomes readable."),
     ("Tank pubs are worth seeking out",
      "Unpasteurised tank beer is a different, fuller drink than the bottled version, and "
      "pubs that pour it say so on the door. It usually costs the same.")])

S["pivovar-velke-popovice"] = (
    "The goat brewery, twenty minutes south-east of Prague, brewing since 1874. Owned by "
    "the same group as Pilsner Urquell and deliberately positioned as its opposite: softer, "
    "sweeter, easier, with the bitterness turned down.",
    [("The dark one is the famous one",
      "Kozel Černý is the dark beer most visitors to Prague meet first, and the one most "
      "often mistaken for a stout. It is a sweet, low-alcohol lager — good on its own terms, "
      "and nothing like Guinness.")])

S["pivovar-gambrinus-plzen"] = (
    "Brewed alongside Pilsner Urquell in Plzeň and, by volume, the beer Czechs actually "
    "drink. Unfashionable and everywhere — the pour you get in an ordinary neighbourhood "
    "pub when you just ask for beer.",
    [])

S["pivovary-staropramen"] = (
    "Prague's own big brewery, on the Smíchov bank of the Vltava since 1869. The name means "
    "&ldquo;old spring&rdquo;. It is the beer of the city in the plainest sense: brewed here, "
    "drunk here, and rarely thought about by anyone who lives here.",
    [("What to order",
      "If a pub carries both the 10° and the 12°, take the 12° — the extra malt is where the "
      "beer becomes interesting. The amber Granát is the best answer to &ldquo;something "
      "darker but not heavy&rdquo;.")])

S["uneticky-pivovar"] = (
    "A village brewery eight kilometres outside Prague, closed under communism and restarted "
    "in 2011 by locals who wanted their beer back. Unfiltered, unpasteurised and quietly "
    "revered — the beer Prague beer people name when they want to sound unpretentious.",
    [("Worth the trip",
      "The brewery pub in Únětice is a bus ride from Dejvická and a genuinely local afternoon. "
      "In Prague itself the beer turns up in a handful of pubs that take beer seriously.")])

S["pivovar-svijany"] = (
    "A regional brewery in a village in the Liberec region, brewing on and off since 1564 and "
    "in its current form since the 1990s. It occupies the middle ground of Czech beer: never "
    "went industrial, never went craft, and built a tied network of pubs across Bohemia — a "
    "dozen of them in Prague.",
    [("Why Czechs are loyal to it",
      "Svijany is the beer a Czech names when asked what they drink instead of the big three. "
      "Cheap enough for an everyday pub, small enough to feel local, and it avoided the "
      "ownership churn Czechs hold against the industrial brands.")])

S["pivovar-radegast"] = (
    "From Nošovice in Moravian Silesia, named after a Slavic god and marketed on bitterness "
    "in a country that markets everything else on smoothness. The driest of the big Czech "
    "lagers, and the one to reach for if Pilsner Urquell felt too soft.",
    [])

S["budejovicky-budvar"] = (
    "From České Budějovice — Budweis in German — and one of the last large Czech breweries "
    "still owned by the state. Rounder and slower than a Plzeň lager, with a long malty "
    "finish rather than a sharp one.",
    [("The Budweiser name",
      "The brewery has been in a trademark fight with the American Anheuser-Busch brand for "
      "over a century. In much of Europe the Czech beer is Budweiser; in the United States it "
      "is sold as Czechvar. The two beers have nothing in common but the name.")])

S["kralovsky-pivovar-krusovice"] = (
    "A royal brewery by charter — Rudolf II bought it in 1583 — and a mass-market lager in "
    "practice. Soft and sweetish, and more common in tourist-facing places in the centre than "
    "in neighbourhood pubs.",
    [])

S["pivovar-klaster"] = (
    "A monastery brewery at Klášter Hradiště nad Jizerou, founded by Cistercians and brewing "
    "in one form or another since the sixteenth century. Soft, malt-forward beer that pubs "
    "keep when they want something other than the big four.",
    [])

S["pivovar-branik"] = (
    "Once Prague's own brewery on the right bank of the Vltava, opened in 1900 and closed as "
    "a working site in 2007. The brand survived and is still poured in the city, carrying "
    "more local sentiment than the beer itself strictly earns.",
    [])

S["pivovar-rychtar"] = (
    "From Hlinsko in the Bohemian-Moravian highlands. A regional name that Prague pubs put on "
    "the tap when they want something recognisably not corporate.",
    [])

S["pivovar-cvikov"] = (
    "A small North Bohemian brewery near the glassworks its beers are named after. Dry, firmly "
    "hopped, and a good example of what a regional 11° is supposed to taste like.",
    [])

S["pivovar-cerna-hora"] = (
    "One of the older Moravian breweries, documented from the sixteenth century, in a village "
    "north of Brno. Dependable middle-of-the-road lagers, increasingly poured in Prague.",
    [])

S["pivovar-zichovec"] = (
    "A revived village brewery in central Bohemia that became one of the loudest names in "
    "Czech craft — heavy on collaborations, sours and one-offs alongside a straight lager.",
    [("Nothing listed here yet",
      "We have not collected this brewery's range. Under the publishing rule the brewery gets "
      "a page and its beers do not, until each one has a source and somewhere in Prague to "
      "drink it.")])

S["vinohradsky-pivovar"] = (
    "A Prague brewpub in Vinohrady, brewing on site since 2014 in a neighbourhood that had "
    "lost its brewery a century earlier. The kind of place where the beer travels ten metres "
    "from tank to glass.",
    [])

S["pivovar-prokopak"] = (
    "A small Prague brewpub in Nové Butovice, brewing for its own tables. Local in the most "
    "literal sense — the beer exists mainly where it is made.",
    [])

S["restaurace-a-pivovar-beer-factory"] = (
    "A Prague brewpub brewing on the premises. Worth knowing that it exists rather than "
    "planning an evening around it.",
    [])

S["breznak"] = (
    "A North Bohemian brand from Velké Březno with a working-town reputation the brewery has "
    "never tried to shake. Firm, dry bitterness and no pretence.",
    [])

S["konrad"] = (
    "From Vratislavice nad Nisou near Liberec. Balanced lagers that lean neither sweet nor "
    "aggressively bitter — the sort a pub keeps because regulars never complain.",
    [])

S["hubertus"] = (
    "From Kácov on the Sázava, in a valley of weekend cottages. Soft, malty beer for a long "
    "evening rather than for study.",
    [])


# ── Отложенные марки ───────────────────────────────────────────────────
# Эти значения пришли из тега OSM `brewery=*` и не подтверждены ничем,
# кроме него: ни записи в Wikidata, ни линейки с сайта. Пивоварнями они
# больше не считаются (см. CURATED_BRANDS в scripts/ingest.py), поэтому
# текст лежит здесь, а не в S. Часть из них — реальные пивоварни (arpus,
# falkon, chroust, kout, bad-flash), часть — не пивоварни вовсе: `argus`
# это частная марка Lidl, `maisel-s-weisse` — название пива, AB InBev и
# Molson Coors — концерны, а `more` пришло из одного паба и, судя по
# всему, мусор. Верните запись в S, когда появится подтверждение.
PENDING = {}

PENDING["kout"] = (
    "Kout na Šumavě, near the Bavarian border — a brewery with genuine cult status among "
    "Czech drinkers and a reputation for dark beers that outclass anything on a mainstream "
    "tap. Hard to find in Prague, and the reason to walk further when you do.",
    [])

S["matuska"] = (
    "The brewery that started Czech craft. Founded in Broumy in 2009 by a father and son who "
    "had been brewing at home, and the first to show Czech drinkers what American hops do to "
    "a beer.",
    [("Where to start",
      "Raptor is the reference Czech IPA and hits hard after a week of lager. Zlatá raketa is "
      "the same hop character turned down enough to have two.")])

PENDING["postriziny"] = (
    "Nymburk, and the brewery of Bohumil Hrabal's novel <em>Postřižiny</em> — his stepfather "
    "managed it. The name on the tap is a literary reference before it is a beer.",
    [])

PENDING["slavkov"] = ("A small Moravian brewery from Slavkov u Brna — Austerlitz.", [])
PENDING["bad-flash"] = (
    "A Prague craft brewery known for hop-forward beers and a fast-changing line-up. Poured "
    "where the tap list turns over weekly.", [])
PENDING["arpus"] = ("A Czech craft brewery whose beers turn up on rotating Prague taps.", [])
PENDING["falkon"] = ("A Czech craft brewery from Žatec, in the hop country itself.", [])
PENDING["chroust"] = ("A Czech craft brewery poured on rotating Prague taps.", [])
PENDING["nozib"] = ("A Czech craft brewery poured on rotating Prague taps.", [])
PENDING["argus"] = ("A Czech beer brand poured in a Prague venue.", [])
PENDING["more"] = ("A Czech craft brewery poured on a rotating Prague tap.", [])

# Иностранные марки: честно сказать, что это не чешская пивоварня
S["guinness"] = (
    "Not a Czech brewery. Guinness appears here because a Prague venue pours it, and because "
    "it is the reference point almost every visitor uses when ordering a dark beer — usually "
    "to their disappointment, since Czech dark lager is a different drink entirely.", [])
S["stella-artois"] = (
    "Not a Czech brewery. Listed because a Prague venue pours it and because it is a useful "
    "yardstick: everything Czech here is maltier, and above the 10° mark considerably more "
    "bitter.", [])
PENDING["molson-coors"] = ("A multinational brewing group, not a Czech brewery. Listed because the tag appears on a Prague venue.", [])
PENDING["ab-inbev"] = ("A multinational brewing group, not a Czech brewery. Listed because the tag appears on a Prague venue.", [])
PENDING["maisel-s-weisse"] = ("A Bavarian wheat beer brand, not a Czech brewery. Listed because a Prague venue pours it.", [])

# Точечные исправления к Wikidata. Уровень достоверности — curated.
FIXES = {
    "pivovary-staropramen": {"founded": 1869},        # 2012 — дата нынешнего юрлица
    "pivovar-velke-popovice": {"founded": 1874},
    "pivovar-branik": {"city": "Praha"},
    "vinohradsky-pivovar": {"city": "Praha"},
    "pivovar-prokopak": {"city": "Praha"},
    "matuska": {"city": "Broumy"},
    "breznak": {"city": "Velké Březno"},
    "konrad": {"city": "Vratislavice nad Nisou"},
    "hubertus": {"city": "Kácov"},
    "kout": {"city": "Kout na Šumavě"},
    "postriziny": {"city": "Nymburk"},
    "falkon": {"city": "Žatec"},
    "slavkov": {"city": "Slavkov u Brna"},
}
