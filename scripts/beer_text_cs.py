"""
Česká verze textů piv. Struktura je stejná jako v beer_text.py:
    L — úvodní odstavec stránky
    N — oddíly pod srovnáním, jen tam, kde je co říct
"""

L = {}
N = {}

# ── Plzeňský Prazdroj ──────────────────────────────────────────────────────
L["pilsner-urquell"] = (
    "Pivo, jehož kopií je každý světlý ležák na světě. V roce 1842 měli plzeňští "
    "měšťané dost nepitelného piva, najali bavorského sládka, vyhloubili sklepy do "
    "pískovce a uvařili první zlatavé spodně kvašené pivo, jaké kdo viděl.")
N["pilsner-urquell"] = [
    ("Proč chutná hořčeji, než čekáte",
     "Žatecký chmel dává bylinnou, skoro travnatou hořkost, která doznívá, a slad "
     "pod ní zůstává suchý. Vedle mezinárodního ležáku to první dva doušky působí "
     "přísně — a pak už nikdy."),
    ("Tank a láhev nejsou totéž",
     "Nepasterizované tankové pivo je měkčí, plnější a znatelně čerstvější. Hospody, "
     "které ho čepují, to dávají na dveře, protože je stojí víc. Pro návštěvníka je "
     "to největší dostupný rozdíl a obvykle nestojí nic navíc."),
]

L["pilsner-urquell-nefiltrovana"] = (
    "Totéž pivo bez filtrace: zakalenější, kulatější, s měkkým kvasnicovým tónem, "
    "o který filtrovaná verze přichází. Čepuje ho zlomek hospod, které mají tu "
    "běžnou, a stojí za to za ním zajít.")

# ── Velké Popovice ─────────────────────────────────────────────────────────
L["kozel-svetly"] = (
    "Levné každodenní pivo. Lehké, měkké a stavěné spíš na to, aby se ho dalo vypít "
    "několik, než aby se o něm přemýšlelo. Když má hospoda jednu pípu pro místní a "
    "jednu pro turisty, tahle bývá ta místní.")

L["kozel-11"] = (
    "O stupeň plnější a sladší než desítka, a právě tuhle verzi většina lidí myslí, "
    "když řekne, že pije Kozla. Měkčí a sladovější než Prazdroj, s výrazně menším "
    "chmelovým skusem.")

L["kozel-cerny"] = (
    "Tmavé pivo, na které narazíte skoro v každé pražské hospodě, a to, které si "
    "nejvíc návštěvníků objedná v očekávání stoutu. Stout to není — je sladké, "
    "slabé a v závěru spíš čisté než suché.")
N["kozel-cerny"] = [
    ("Je to jako Guinness?",
     "Ne, a tohle je nejčastější zklamání v Praze. Guinness je suchý, tenký a čepuje "
     "se dusíkem; Kozel Černý je sladký ležák s karamelovým sladem a běžným "
     "nasycením. Kdo přišel pro stout, najde na běžných českých pípách nejblíž "
     "<em>tmavý speciál</em> okolo třinácti stupňů — a obvykle bude muset opustit "
     "turistické centrum."),
]

# ── Gambrinus ──────────────────────────────────────────────────────────────
L["gambrinus-original-10"] = (
    "Objemem pivo, které Češi opravdu pijí. Nemoderní, levné a všude — to, co "
    "dostanete, když vejdete do obyčejné hospody a řeknete jen <em>pivo</em>.")

L["gambrinus-original-11"] = (
    "Prostřední Gambrinus: o něco plnější a kulatější než desítka, pořád ale pivo "
    "na každý den. Vaří se v Plzni vedle Prazdroje a je záměrně měkčí.")

# ── Staropramen ────────────────────────────────────────────────────────────
L["staropramen-svetly"] = (
    "Vlastní velký pražský pivovar, na břehu Vltavy na Smíchově od roku 1869. "
    "Desítka je lehká každodenní verze — nekonfliktní, všude dostupná a vypitá "
    "většinou aniž by si toho někdo všiml.")

L["staropramen-lezak"] = (
    "Dvanáctka, a ta z dvojice stojí za objednání, pokud hospoda čepuje obě. "
    "Plnější a chmelenější než desítka, pořád ale jemnější než plzeňský ležák.")

L["staropramen-granat"] = (
    "Polotmavý ležák na půl cesty mezi světlým a tmavým: karamelová sladkost, "
    "trocha praženosti, hořkost skoro žádná. Dobrá odpověď, když tmavé zní moc "
    "těžce a světlé moc obyčejně.")

# ── Únětický pivovar ───────────────────────────────────────────────────────
L["uneticka-10"] = (
    "Z vesnice kousek za Prahou, nefiltrovaná a mezi místními tiše kultovní. "
    "Desítka je lehčí, než jak chutná — plné, chlebové pivo pod čtyři procenta.")

L["uneticka-12"] = (
    "Tvarem Prazdroj, jenže nefiltrovaný a kulatější: stejná pevná žatecká hořkost "
    "s větší plností pod ní a kvasnicovou měkkostí, kterou by filtrace odebrala. "
    "Jedno z nejzajímavějších piv dvacet minut od města.")

L["uneticka-tmava-12"] = (
    "Tmavé pivo, ve které většina návštěvníků doufala, když si objednala Kozla "
    "Černého: sušší, pořádně pražené, s opravdovou kávou a tmavým chlebem místo "
    "karamelového sirupu. Hůř k sehnání a stojí to za tu procházku.")

# ── Svijany ────────────────────────────────────────────────────────────────
L["svijansky-maz"] = (
    "Každodenní Svijany, a pivo, které Čech jmenuje, když se ho zeptáte, co pije "
    "místo velké trojky. Měkké, sladové, snadné — z pivovaru dost malého na to, "
    "aby působil místně, a dost velkého na to, aby byl všude.")

L["svijansky-rytir"] = (
    "Dvanáctka z řady a nejbližší regionální odpověď na Prazdroj: stejná třída "
    "piva, o kousek sladovější a méně ostrá. Komu Prazdroj chutnal, ale chtěl by ho "
    "jemnější, hledá tohle.")

L["svijanska-knezna"] = (
    "Třináctistupňový speciál — plnější, sladší a znatelně silnější než každodenní "
    "ležáky, a pořád rozpoznatelně ze stejného pivovaru. Objednávejte spíš pozdě "
    "než jako první.")

L["svijany-450"] = (
    "Nefiltrované Svijany, pojmenované po výročí pivovaru. Zakalenější a měkčí než "
    "Máz, s větším podílem kvasnic. Na pípách se objevuje a mizí — ptejte se, "
    "nepředpokládejte.")

# ── Radegast ───────────────────────────────────────────────────────────────
L["radegast-original"] = (
    "Z Nošovic ve Slezsku, a nejsušší z běžných českých ležáků. Prodává se na "
    "hořkosti v zemi, kde se všechno ostatní prodává na jemnosti.")

L["radegast-ryze-horka-12"] = (
    "Nejhořčejší pivo, jaké najdete na běžné české pípě — a je to záměr. Pokud vám "
    "Prazdroj přišel příliš měkký, tohle je oprava; pokud příliš hořký, jděte dál.")

# ── Budvar ─────────────────────────────────────────────────────────────────
L["budweiser-budvar-original"] = (
    "Z Českých Budějovic, německy Budweis, a pořád ve státních rukou. Kulatější, "
    "sladší a pomalejší než Prazdroj, s dlouhým sladovým závěrem místo ostrého.")
N["budweiser-budvar-original"] = [
    ("Proč se všude nejmenuje Budweiser",
     "Pivovar vede spor o ochrannou známku s americkou značkou Anheuser-Busch přes "
     "sto let. Ve velké části Evropy je Budweiser české pivo, ve Spojených státech "
     "se prodává jako Czechvar. Kromě jména nemají společného nic."),
]

L["budvar-tmavy-lezak"] = (
    "Tmavý protějšek Originalu: karamel a tmavý chléb s opravdovou praženou hranou, "
    "sušší než většina českých tmavých ležáků. Dobré první tmavé pivo pro toho, "
    "komu byl Kozel Černý příliš sladký.")

# ── Krušovice ──────────────────────────────────────────────────────────────
L["krusovice-svetle"] = (
    "Královský pivovar podle listiny, masový ležák v praxi. Měkké, nasládlé a "
    "nenáročné — v turistických podnicích v centru ho uvidíte častěji než v "
    "hospodách na sídlišti.")

L["krusovice-cerne"] = (
    "Sladké, tmavé a slabé, ze stejné rodiny jako Kozel Černý a se stejnou výhradou: "
    "je to ležák tíhnoucí k dezertu, ne stout.")

# ── další regionální ───────────────────────────────────────────────────────
L["breznak-svetly-lezak"] = (
    "Severočeský ležák s pevnou suchou hořkostí a pověstí dělnického města, které "
    "se pivovar nikdy nesnažil zbavit. Přímočaré a dobře udělané.")

L["klaster-lezak"] = (
    "Klášterní pivovar v Klášteře Hradišti nad Jizerou, založený cisterciáky a "
    "vařící v nějaké podobě od šestnáctého století. Měkké sladové pivo, které "
    "projde bez námitek.")

L["konrad-12"] = (
    "Z Vratislavic u Liberce — vyvážená dvanáctka, která netíhne ani ke sladkosti, "
    "ani k agresivní hořkosti. Pivo, které si hospoda drží, protože si na něj štamgasti "
    "nikdy nestěžují.")

L["branik-svetle-vycepni"] = (
    "Kdysi vlastní pražský pivovar na pravém břehu Vltavy; značka provoz přežila. "
    "Lehká levná desítka, ke které se váže víc místního sentimentu, než si samo pivo "
    "zaslouží.")

L["rychtar-fojt"] = (
    "Z Hlinska na Vysočině. Regionální jméno, které pražské hospody dávají na pípu, "
    "když chtějí něco rozpoznatelně nekorporátního.")

L["cvikov-sklar"] = (
    "Malý severočeský pivovar u sklárny, po níž se pivo jmenuje. Suché, pevně "
    "chmelené, a dobrý příklad toho, jak má regionální jedenáctka chutnat.")

L["hubertus-premium"] = (
    "Z Kácova na Sázavě. Měkké a sladové s drženou hořkostí — pivo na dlouhý večer, "
    "ne ke studiu.")

L["cerna-hora-lezak"] = (
    "Jeden ze starších moravských pivovarů, doložený od šestnáctého století, ve vsi "
    "severně od Brna. Spolehlivé ležáky středního proudu, čím dál častěji i v Praze.")

# ── řemeslné ───────────────────────────────────────────────────────────────
L["matuska-raptor"] = (
    "Pivo, které českým pijákům ukázalo, co dělá americký chmel. Grapefruit a "
    "borovice nad pevnou hořkou páteří, a pořád referenční IPA v zemi, která před "
    "dvaceti lety žádnou neměla.")
N["matuska-raptor"] = [
    ("Pokud jste celý týden pili ležák",
     "Tohle bude chutnat obrovsky. To je záměr, ale není to pivo na sezení: při 6,3 % "
     "a takovém chmelovém aroma je jedno zážitek a tři chyba."),
]

L["matuska-zlata-raketa"] = (
    "Spíš pale ale než IPA — stejný novosvětský chmelový charakter, ztlumený natolik, "
    "aby se dalo vypít víc než jedno. Dobrý most z českého ležáku do českého řemesla.")

# ── mezinárodní kotvy ──────────────────────────────────────────────────────
L["guinness-draught"] = (
    "Tady jen jako bod srovnání. Suchý, pražený, tenký a čepovaný dusíkem — pravý "
    "opak toho, co dělá český tmavý ležák, a proto objednat Kozla Černého v očekávání "
    "tohohle dopadá špatně.")

L["stella-artois"] = (
    "Bod srovnání pro čistý, mírný evropský ležák. Užitečný hlavně jako měřítko toho, "
    "o kolik je česká dvanáctka hořčejší a sladovější.")

L["corona-extra"] = (
    "Nejlehčí kotva v atlasu: sotva hořká, sotva plná. Pokud tohle je vaše představa "
    "piva, začněte českou desítkou, ne dvanáctkou.")

L["heineken"] = (
    "Mezinárodní ležák, na který má většina návštěvníků zkalibrovanou paměť. Všechno "
    "české na tomhle webu je sladovější a nad desítkou i podstatně hořčejší.")

L["brewdog-punk-ipa"] = (
    "Referenční moderní IPA: citrusy a pryskyřice, vysoká hořkost, suchý závěr. "
    "Měřítko pro české řemeslné položky zde.")

L["hoegaarden"] = (
    "Belgické pšeničné pivo — koriandr, pomerančová kůra, žádná hořkost. Na běžné "
    "české pípě není nic podobného, což je dobré vědět, než se po tom vydáte.")

L["weihenstephaner-hefeweissbier"] = (
    "Bavorské pšeničné: banán a hřebíček z kvasnic, plné a měkké. České pivovary "
    "pšeničné vaří, ale je to tu styl hostující, ne domácí.")
