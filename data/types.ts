/**
 * Пивной атлас Праги — модель данных v0
 *
 * Два принципа, на которых держится всё остальное:
 *
 * 1. Провенанс на каждом значимом поле. Любая цифра несёт источник, метод
 *    получения и дату. Значения, выведенные моделью, помечены и видны как
 *    таковые — и в интерфейсе тоже. Без этого база превращается в правдоподобно
 *    выглядящую выдумку, и первый же гид это заметит.
 *
 * 2. Связь идёт через пивоварню, а не через SKU. Заведение в Чехии привязано к
 *    бренду (Svijanská hospoda, Kozlovna, сертифицированные заведения PU) —
 *    эта связь живёт годами. Наличие конкретной позиции живёт три дня.
 */

// ─── Языки ────────────────────────────────────────────────────────────────

/**
 * Текст всегда по языкам, даже пока язык один.
 * Чешская версия — не перевод английской, а отдельный продукт для другой
 * аудитории (опрос о варке, бары, пивоварни). Но поле должно быть готово
 * заранее: сейчас это ключ в объекте, через год — миграция всего каталога.
 */
export type Locale = "en" | "cs";
export type Text = { en: string } & Partial<Record<Locale, string>>;

// ─── Провенанс ────────────────────────────────────────────────────────────

export type Method =
  | "official"      // сайт пивоварни, этикетка, официальный список заведений
  | "measured"      // замерено или увидено лично
  | "phone"         // спросили по телефону
  | "inferred"      // выведено моделью из стиля и описания — САМЫЙ СЛАБЫЙ УРОВЕНЬ
  | "unverified";   // заполнено по памяти, требует проверки

export interface Sourced<T> {
  value: T;
  method: Method;
  source?: string;  // URL или имя человека
  checkedAt?: string; // ISO-дата
}

// ─── Вкусовой профиль ─────────────────────────────────────────────────────

/**
 * Девять осей, 0–10. Заполняются НЕ как абсолютные оценки, а как позиция
 * относительно центроида стиля — иначе у всех hazy IPA получится один вектор,
 * потому что маркетинговые описания у них одинаковые.
 *
 * hopProfile — специально для чешского контекста: главная ось здесь не
 * «сколько хмеля», а «какой». 0 = классический жатецкий травяно-пряный,
 * 10 = новосветский цитрусово-тропический.
 */
export interface Flavour {
  bitterness: number;
  maltSweetness: number;
  body: number;
  dryness: number;      // сухость финиша, степень сбраживания
  roast: number;
  fruitEster: number;
  sourness: number;
  hopAroma: number;     // интенсивность аромата
  hopProfile: number;   // 0 = Saaz, 10 = New World
}

export const FLAVOUR_AXES: (keyof Flavour)[] = [
  "bitterness", "maltSweetness", "body", "dryness", "roast",
  "fruitEster", "sourness", "hopAroma", "hopProfile",
];

/** Подписи для интерфейса: [низкий полюс, высокий полюс] */
export const AXIS_LABELS: Record<keyof Flavour, [string, string]> = {
  bitterness:    ["мягкое", "горькое"],
  maltSweetness: ["сухое солодовое", "сладкое солодовое"],
  body:          ["лёгкое", "плотное"],
  dryness:       ["округлый финиш", "сухой финиш"],
  roast:         ["без жжёности", "жжёное"],
  fruitEster:    ["чистое", "фруктовое"],
  sourness:      ["без кислинки", "кислое"],
  hopAroma:      ["сдержанный аромат", "яркий аромат"],
  hopProfile:    ["жатецкий, травяной", "цитрус, тропики"],
};

// ─── Сущности ─────────────────────────────────────────────────────────────

export type BreweryKind = "industrial" | "regional" | "craft" | "brewpub";

export interface Brewery {
  id: string;
  name: string;
  city: string;
  founded?: number;
  kind: BreweryKind;
  /** Официальный список партнёрских заведений — источник бутстрапа графа */
  venueListUrl?: string;
  site?: string;
  /** Краткая справка — материал для гида и тело страницы пивоварни */
  story?: Text;
}

export interface Beer {
  id: string;
  breweryId: string;
  name: string;
  /** Как это называется в чешском меню — то, что турист видит глазами */
  menuNameCs: string;
  style: string;

  plato?: Sourced<number>;   // °P, экстрактивность — НЕ крепость
  abv?: Sourced<number>;     // %
  ibu?: Sourced<number>;     // ориентир, плохо предсказывает воспринимаемую горечь
  ebc?: Sourced<number>;     // цвет

  flavour: Sourced<Flavour>;

  /** Международные якоря: «похоже на Guinness, но легче» */
  tastesLike?: string[];

  /** Первый абзац страницы сорта. Авторский текст, не извлечённый факт. */
  lead?: Text;
  /** Разделы ниже сравнения: заголовок и абзац. Только там, где есть что сказать. */
  notes?: { heading: Text; body: Text }[];

  /** Международный якорь: существует как точка отсчёта, правилу публикации не подчиняется */
  isAnchor?: boolean;

  availability: "core" | "seasonal" | "oneoff";
  filtered?: boolean;
  pasteurised?: boolean;
}

export type VenueKind =
  | "tankovna"    // танковое непастеризованное
  | "taproom"     // тапрум пивоварни
  | "multitap"    // ротация, крафт
  | "brewpub"
  | "pub";        // классическая хоспода

export interface Venue {
  id: string;
  name: string;
  district: string;         // Praha 1, Žižkov, Vinohrady…
  lat: number;
  lng: number;
  kind: VenueKind;

  /** Ось схемы: какие пивоварни здесь наливают постоянно */
  breweryIds: string[];
  /** Конкретные позиции — только если действительно подтверждены и с датой */
  beerIds?: string[];

  tankBeer?: Sourced<boolean>;
  price05?: Sourced<number>;     // CZK за 0,5 л, главный индикатор ловушки
  englishMenu?: Sourced<boolean>;
  cards?: Sourced<boolean>;

  /** Данные сентябрьского обзвона — то, чего нет ни у кого */
  groups?: Sourced<{
    maxWithoutBooking: number | null;  // null = не берут без брони
    bookingRequiredFrom: number | null;
    backRoom: boolean;
    answersPhone: boolean;
  }>;

  /** Честный флаг: цена и практики центра */
  touristTrap?: Sourced<boolean>;
  notes?: Text;
}

export interface Dataset {
  breweries: Brewery[];
  beers: Beer[];
  venues: Venue[];
}
