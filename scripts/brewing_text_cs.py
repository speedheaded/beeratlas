"""Česká verze technologie. Klíče stejné jako v brewing_text.py."""

PROCESS = [
    ("Ze sladu a vody vzniká mladina",
     "Šrotovaný slad se smíchá s horkou vodou, aby vlastní enzymy zrna rozštěpily jeho "
     "škrob na zkvasitelný cukr. České pivovary to dělají <b>dekokcí</b> — rmutováním: "
     "část rmutu se odebere, zvlášť povaří a vrátí zpátky, čímž se celá várka posune na "
     "další teplotní stupeň. Dva nebo tři rmuty jsou tu běžné tam, kde zbytek světa "
     "používá jedinou infuzi. Je to pomalejší, stojí to víc energie, a dává to sladový "
     "chlebový, lehce medový charakter, podle kterého se český ležák pozná."),
    ("Zrno se oddělí",
     "Sladká tekutina — <b>mladina</b> — se scedí od mláta, které jde dobytku. V pánvi "
     "zůstane cukr, bílkoviny a minerální látky, a žádné pivo."),
    ("Chmelovar",
     "Mladina se vaří a přidává se chmel, obvykle na několik dávek. Časný chmel dává "
     "hořkost, pozdní aroma. Český světlý ležák stojí na <b>žateckém chmelu</b> — "
     "žateckém poloraném červeňáku — aromatické odrůdě s nízkým obsahem alfa kyselin a "
     "bylinným, lehce kořenitým charakterem. Právě ten nízký obsah alfa kyselin je "
     "důvod, proč česká dvanáctka chutná pevně hořce, aniž by kdy chutnala pryskyřičně "
     "jako moderní IPA."),
    ("Studené kvašení se spodními kvasnicemi",
     "Mladina se zchladí zhruba na 6 °C, provzdušní a zakvasí spodními kvasnicemi, které "
     "pracují u dna a při teplotách, jaké by svrchní kvasnice odmítly. Hlavní kvašení "
     "trvá šest až deset dní zhruba při 8–12 °C. Pomalu a ve studeném vzniká čistý "
     "profil: žádné banánové a hřebíčkové estery, jaké hodí teplé svrchní kvašení. "
     "Některé české pivovary dodnes používají <b>otevřenou spilku</b> — hranaté "
     "otevřené kádě ve studeném sklepě, tak, jak se to dělalo před tlakovým tankem."),
    ("Ležení — část, po které se pivo jmenuje",
     "<em>Lagern</em> je německy „skladovat“. Mladé pivo jde do ležáckých tanků při "
     "zhruba 2 °C a leží tam týdny: tři až čtyři u každodenní desítky, šest až dvanáct u "
     "pořádné dvanáctky, a proslulých zhruba devadesát dnů u Budvaru. Za tu dobu se "
     "vyčeří, změkne, přirozeně se nasytí oxidem uhličitým a ztratí ostré tóny mladého "
     "piva. Tenhle dlouhý studený odpočinek je největší rozdíl mezi tradičním českým "
     "ležákem a průmyslově zrychleným."),
    ("Filtrované, nefiltrované, pasterizované, nepasterizované",
     "Jsou to dvě různé otázky a pořád se pletou. <b>Filtrace</b> odebírá kvasnice a "
     "zákal — křemelinová filtrace, někdy následovaná mikrofiltrací. <b>Pasterizace</b> "
     "zahřívá hotové pivo, aby zabila, co přežilo, a mění čerstvost za trvanlivost. "
     "Pivo může být filtrované a přitom nepasterizované, a přesně to na české etiketě "
     "„nepasterizované“ obvykle znamená: bylo vyčeřeno, ale nikdy zahřáto. Tankové pivo "
     "v hospodě bývá obojí — nepasterizované a dovezené během pár dnů."),
    ("Proč číslo na jídelním lístku není alkohol",
     "Ten stupeň je <b>stupeň Plato</b>: hmotnostní procento rozpuštěného cukru v "
     "mladině před kvašením. Kvasnice zhruba polovinu promění v alkohol, takže výsledná "
     "síla vyjde okolo třetiny toho čísla — jedenáctka skončí kolem 4,6 %. Pivovar může "
     "tu rovnováhu i posunout: trocha cukru do varny zvedne alkohol, aniž přidá plnost, "
     "a právě proto některé jedenáctky zůstávají v ústech nezvykle lehké."),
]

STAGE_WHAT = {
    "mash":    ("Rmutování", "Ze škrobu vzniká cukr",
                "Šrotovaný slad se potká s horkou vodou a vlastní enzymy zrna rozštěpí "
                "jeho škrob na zkvasitelný cukr. Výsledkem je <b>mladina</b>: sladká, "
                "bez chmele, ještě ne pivo."),
    "boil":    ("Chmelovar", "Přichází hořkost a aroma",
                "Mladina se vaří a přidává se chmel. Časné dávky dají hořkost, pozdní "
                "aroma. Nic jiného v procesu ani jedno nepřidá."),
    "ferment": ("Hlavní kvašení", "Z cukru vzniká alkohol",
                "Zchlazeno zhruba na 6 °C a zakvašeno spodními kvasnicemi. Cukr se mění "
                "na alkohol a oxid uhličitý; chlad a pomalost drží profil čistý."),
    "lager":   ("Ležení", "Zbytek udělá čas",
                "Mladé pivo odpočívá ve studených ležáckých tancích. Čeří se, měkne, "
                "přirozeně se nasycuje a ztrácí ostrost mladého piva. Tenhle krok "
                "průmyslové vaření zkracuje jako první."),
    "finish":  ("Dokončení", "Čeření a stáčení",
                "Filtrace odebere kvasnice a zákal. Pasterizace — zahřátí hotového piva "
                "— je samostatné rozhodnutí, a spousta českého piva se jí vyhýbá."),
}

LABELS = [
    ("water", "Voda"), ("malt", "Slad"), ("adjuncts", "Přídavky"), ("hops", "Chmel"),
    ("mash", "Rmutování"), ("ferment", "Kvašení"),
    ("lagerTemp", "Teplota ležení"), ("lagerDays", "Doba ležení"),
    ("filtration", "Filtrace"),
]

PASTEUR_NO = "Nepasterizované — filtrované, ale nikdy zahřáté."

# ── podle piv ──────────────────────────────────────────────────────────────
P = {}

P["pilsner-urquell"] = dict(
    water="Měkká plzeňská voda s velmi nízkým obsahem minerálních solí — díky ní dosedá "
          "chmelová hořkost čistě, ne drsně.",
    malt="Moravský humnový ječný slad.",
    hops="Žatecký chmel (žatecký poloraný červeňák), hlávkový.",
    mash="Třírmutová dekokce — tři oddělené části rmutu se povaří a vrátí. Ve velkém to "
         "už skoro nikdo nedělá.",
    ferment="Historicky otevřené kádě v pískovcových sklepích; malá souběžná várka se tam "
            "dodnes zakvašuje a leží v dřevěných sudech pro srovnání.",
    lagerDays="týdny, v ležáckých tancích",
    filtration="Filtrované pro láhev a plech; tankové se dodává nepasterizované.",
    note="Srovnávací várka ve sklepě je důvod, proč pivovar dokáže říct, jak to má "
         "chutnat. Kdo jede na exkurzi do Plzně, jde tam kvůli nefiltrovanému "
         "nepasterizovanému pivu přímo ze sklepního sudu.",
)
P["pilsner-urquell-nefiltrovana"] = dict(
    malt="Stejná sladová sypanina jako u filtrované verze.", hops="Žatecký chmel.",
    mash="Třírmutová dekokce.",
    filtration="Nefiltrované — kvasnice zůstávají, odtud zákal i měkčí ústa.",
    note="Nefiltrované a nepasterizované jsou dvě různé věci a tohle pivo je obojí. "
         "Čekejte kulatější plnost a jemný kvasnicový chlebový tón.",
)
P["svijansky-maz"] = dict(
    water="Z vlastních vrtů pivovaru.",
    malt="Humnový ječný slad kupovaný od malých nezávislých sladoven v Čechách a na "
         "Moravě. Humnové sladování je pomalá tradiční metoda a je zdrojem chlebového, "
         "lehce medového základu.",
    adjuncts="Trocha cukru do varny. Ne kvůli sladkosti — kvasnice ho téměř celý sežerou, "
             "takže zvedá alkohol a přitom drží plnost nízko. Proto mladina o 11 % "
             "skončí na 4,8 % a pivo se pořád pije snadno.",
    hops="Žatecký chmel z vlastních chmelnic pivovaru v Polepských blatech, plus chmelový "
         "extrakt pro přesné řízení hořkosti.",
    mash="Dvourmutová dekokce.",
    ferment="Otevřená spilka, zhruba do 12 °C, šest až osm dní.",
    lagerTemp="≈ 2 °C", lagerDays="30–60 dní podle piva",
    filtration="Křemelinová filtrace následovaná mikrofiltrací.",
    note="Nepasterizované tu neznamená živé kvasnice v láhvi — pivo je pořádně "
         "filtrované, jen nikdy nezahřáté.",
)
P["svijansky-rytir"] = dict(
    water="Vlastní vrty pivovaru.", malt="Humnový ječný slad.",
    hops="Žatecký chmel z vlastních chmelnic.", mash="Dvourmutová dekokce.",
    ferment="Otevřená spilka, zhruba do 12 °C.",
    lagerTemp="≈ 2 °C", lagerDays="30–60 dní",
    filtration="Křemelina a mikrofiltrace.",
)
P["svijanska-knezna"] = dict(mash="Dvourmutová dekokce.", ferment="Otevřená spilka.",
                             lagerTemp="≈ 2 °C", lagerDays="déle než běžná řada",
                             hops="Žatecký chmel.")
P["svijany-450"] = dict(mash="Dvourmutová dekokce.", ferment="Otevřená spilka.",
                        filtration="Nefiltrované.", hops="Žatecký chmel.",
                        note="Nefiltrované i nepasterizované — tak blízko kvasnému sklepu, "
                             "jak se pivo tohohle pivovaru v láhvi dostane.")
P["budweiser-budvar-original"] = dict(
    water="Z vlastních artéských studní pivovaru, z hluboké zvodně pod Českými Budějovicemi.",
    malt="Moravský ječný slad.", hops="Žatecký chmel.",
    lagerTemp="≈ 2 °C", lagerDays="zhruba 90 dní — asi trojnásobek běžného zvyku",
    note="Devadesátidenní ležení je hlavní tvrzení pivovaru a nejpravděpodobnější "
         "vysvětlení kulatosti piva: v dlouhém chladu odchází ostrost a přirozeně "
         "přichází nasycení.",
)
P["uneticka-12"] = dict(
    malt="Humnový český ječný slad.", hops="Žatecký chmel.", mash="Dekokce.",
    ferment="Otevřená spilka.", filtration="Nefiltrované.",
    note="Pivovar prodává pivo nefiltrované a nepasterizované a nerozváží ho daleko. Je "
         "to záměrná výměna: čerstvost za dosah.",
)
P["uneticka-10"] = dict(ferment="Otevřená spilka.", filtration="Nefiltrované.",
                        hops="Žatecký chmel.", mash="Dekokce.")
P["uneticka-tmava-12"] = dict(ferment="Otevřená spilka.", filtration="Nefiltrované.",
                              mash="Dekokce.",
                              malt="Světlý ječný slad s praženými a karamelovými slady pro "
                                   "barvu a kávový tón.")
P["kozel-cerny"] = dict(
    malt="Světlý slad s karamelovými a praženými slady. Většinu práce dělá karamelový "
         "slad: přináší barvu a sladkost, ale skoro nic ze suché praženosti, kterou "
         "stout dostává z praženého ječmene.",
    hops="Žatecký chmel, držený zkrátka.",
    note="Tohle je technický důvod, proč lidi zklame, když čekají Guinness. Suchý stout "
         "má charakter z nesladovaného praženého ječmene a dusíkového čepování; tohle ho "
         "má z karamelového sladu a běžného oxidu uhličitého.",
)
P["matuska-raptor"] = dict(
    malt="Základ ze světlého ale sladu, držený lehce, aby měl chmel prostor.",
    hops="Americké odrůdy s velkou pozdní dávkou a studeným chmelením — chmel přidaný po "
         "kvašení, který přispívá aromatem, ale žádnou hořkostí.",
    ferment="Svrchní kvasnice, teplo — opak všeho ostatního na tomhle webu.",
    note="Studené chmelení je rozdíl mezi IPA a silně chmeleným ležákem: hořkost přichází "
         "z varny, ale ta grapefruitová a borovicová vůně z chmele, který kotel nikdy neviděl.",
)
P["matuska-zlata-raketa"] = dict(hops="Americké odrůdy, studeně chmeleno.",
                                 ferment="Svrchní kvasnice, teplé kvašení.")
P["radegast-ryze-horka-12"] = dict(
    hops="Chmeleno znatelně silněji než česká norma — celé postavení piva stojí na hořkosti.",
    note="Prodává se na hořkosti na trhu, který prodává jemnost. Pokud vám kdy český ležák "
         "přišel příliš měkký, tohle je pivo postavené přesně na tu výtku.",
)

_SKUPINA = ("Součást skupiny Plzeňský Prazdroj a vaří se jejím postupem: český slad, "
            "žatecký chmel, rmutování a studené ležení.")
for _id in ("gambrinus-original-10", "gambrinus-original-11"):
    P[_id] = dict(hops="Žatecký chmel.", mash="Dekokce.",
                  note=_SKUPINA + " Vaří se ve stejné plzeňské varně jako Prazdroj a je "
                       "záměrně stavěný měkčeji.")
for _id in ("kozel-svetly", "kozel-11"):
    P[_id] = dict(hops="Žatecký chmel.", mash="Dekokce.", note=_SKUPINA)
P["radegast-original"] = dict(hops="Žatecký chmel, používaný důrazněji než česká norma.",
                              mash="Dekokce.", note=_SKUPINA)
for _id in ("staropramen-svetly", "staropramen-lezak", "staropramen-granat"):
    P[_id] = dict(hops="České aromatické chmely.", mash="Dekokce.",
                  note="Vaří se na Smíchově, uvnitř Prahy, což je nejkratší cesta z varny "
                       "na pípu ve městě.")
P["staropramen-granat"]["malt"] = ("Světlý a karamelový slad. Karamelový podíl je to, co ho "
                                   "staví mezi světlé a tmavé, místo do jednoho z nich.")
P["krusovice-svetle"] = dict(hops="Žatecký chmel.", mash="Dekokce.")
P["krusovice-cerne"] = dict(hops="Žatecký chmel, držený zkrátka.", mash="Dekokce.",
                            malt="Světlý slad s karamelovým a praženým sladem.")
P["budvar-tmavy-lezak"] = dict(hops="Žatecký chmel.",
                               malt="Světlý slad s praženými a karamelovými slady.",
                               lagerTemp="≈ 2 °C", lagerDays="dlouho, jako v celé řadě",
                               note="Budvar leží své pivo podstatně déle, než je v oboru "
                                    "zvykem, a tmavé není výjimkou.")

# ── typické pro styl ───────────────────────────────────────────────────────
STYLE = {
    "Czech pale lager": dict(
        malt="Český ječný slad, obvykle samotný světlý plzeňský.",
        hops="Žatecký nebo jiný český aromatický chmel.",
        mash="Dekokce — typicky dvourmutová — místo jediné infuze.",
        ferment="Spodní kvasnice, zhruba 8–12 °C, šest až deset dní.",
        lagerTemp="≈ 2 °C", lagerDays="tři týdny u desítky, šest a víc u dvanáctky",
        filtration="Obvykle filtrované."),
    "Czech pale lager, unfiltered": dict(
        malt="Český světlý ječný slad.", hops="Žatecký chmel.",
        mash="Dekokce.", ferment="Spodní kvasnice, 8–12 °C.",
        lagerTemp="≈ 2 °C", lagerDays="několik týdnů",
        filtration="Nefiltrované — zákal a měkčí plnost jsou kvasnice zůstávající v pivu."),
    "Czech dark lager": dict(
        malt="Světlý slad s karamelovými a praženými slady pro barvu a sladkost.",
        hops="Žatecký chmel, držený vzadu, aby vedl slad.",
        mash="Dekokce.", ferment="Spodní kvasnice, 8–12 °C.",
        lagerTemp="≈ 2 °C", lagerDays="několik týdnů"),
    "Czech amber lager": dict(
        malt="Světlý a karamelový slad — na půl cesty mezi světlým a tmavým.",
        hops="Žatecký chmel.", mash="Dekokce.", ferment="Spodní kvasnice, 8–12 °C.",
        lagerTemp="≈ 2 °C", lagerDays="několik týdnů"),
    "Czech pale special": dict(
        malt="Těžší sypanina než u každodenního ležáku — víc sladu dovnitř, víc alkoholu ven.",
        hops="Žatecký chmel.", mash="Dekokce.", ferment="Spodní kvasnice, 8–12 °C.",
        lagerTemp="≈ 2 °C", lagerDays="déle než běžná řada"),
    "American IPA": dict(
        malt="Lehký základ ze světlého sladu.",
        hops="Novosvětské odrůdy, silně pozdně a studeně chmeleno.",
        ferment="Svrchní kvasnice, teplo.", filtration="Často nefiltrované."),
    "American pale ale": dict(
        malt="Základ ze světlého sladu.", hops="Novosvětské odrůdy, studeně chmeleno.",
        ferment="Svrchní kvasnice, teplo."),
}
