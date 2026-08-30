/**
 * Подбор по формуле «отклонение от знакомого якоря».
 *
 * Пользователь не отвечает на вопрос «сухость от 1 до 10» — он не умеет.
 * Он берёт пиво, вкус которого у него откалиброван во рту (Урквелл, Козел,
 * Guinness), и двигает его: «то же самое, но менее горькое и темнее».
 *
 * Тот же механизм работает в двух режимах:
 *   findMatches()  — найти существующее пиво и где оно налито
 *   describeSpec() — описать гипотетическое пиво для опроса о варке
 */

import {
  type Beer, type Flavour, type Venue,
  FLAVOUR_AXES, AXIS_LABELS,
} from "../data/types";

export type Deltas = Partial<Record<keyof Flavour, number>>;

const clamp = (n: number) => Math.max(0, Math.min(10, n));

/** Целевой профиль = якорь плюс сдвиги пользователя */
export function applyDeltas(anchor: Flavour, deltas: Deltas): Flavour {
  const out = { ...anchor };
  for (const axis of FLAVOUR_AXES) {
    out[axis] = clamp(anchor[axis] + (deltas[axis] ?? 0));
  }
  return out;
}

/**
 * Взвешенное расстояние. Оси, которые пользователь тронул, весят больше:
 * если человек специально убавил горечь, промах по горечи должен наказываться
 * сильнее, чем промах по оси, о которой он не думал.
 */
export function distance(target: Flavour, candidate: Flavour, deltas: Deltas): number {
  let sum = 0;
  for (const axis of FLAVOUR_AXES) {
    const moved = Math.abs(deltas[axis] ?? 0);
    const weight = 1 + moved * 0.6;
    const d = target[axis] - candidate[axis];
    sum += weight * d * d;
  }
  return Math.sqrt(sum);
}

export interface Match {
  beer: Beer;
  score: number;              // 0..1, выше — ближе
  venues: Venue[];
  /** Готовая фраза: «как Урквелл, но темнее и менее горькое» */
  explanation: string;
  /** true, если профиль выведен моделью, а не проверен — показывать в UI */
  soft: boolean;
}

export interface MatchOptions {
  /** Не показывать пиво, которое негде выпить. Правило из брифа. */
  requireVenue?: boolean;
  limit?: number;
}

export function findMatches(
  anchor: Beer,
  deltas: Deltas,
  beers: Beer[],
  venues: Venue[],
  opts: MatchOptions = {},
): Match[] {
  const { requireVenue = true, limit = 10 } = opts;
  const target = applyDeltas(anchor.flavour.value, deltas);

  const results: Match[] = [];

  for (const beer of beers) {
    if (beer.id === anchor.id) continue;

    const where = venuesFor(beer, venues);
    if (requireVenue && where.length === 0) continue;

    const d = distance(target, beer.flavour.value, deltas);
    results.push({
      beer,
      score: 1 / (1 + d / 4),
      venues: where,
      explanation: explain(anchor, beer),
      soft: beer.flavour.method === "inferred" || beer.flavour.method === "unverified",
    });
  }

  return results.sort((a, b) => b.score - a.score).slice(0, limit);
}

/**
 * Где налито. Привязка идёт через пивоварню — это стабильная связь.
 * Прямое совпадение по позиции сильнее, но встречается реже.
 */
export function venuesFor(beer: Beer, venues: Venue[]): Venue[] {
  const direct = venues.filter((v) => v.beerIds?.includes(beer.id));
  const byBrewery = venues.filter(
    (v) => v.breweryIds.includes(beer.breweryId) && !direct.includes(v),
  );
  return [...direct, ...byBrewery];
}

/**
 * Объяснение через два-три самых крупных отличия от якоря.
 * Это же — формат карточки в энциклопедии и бюллетеня в опросе.
 */
export function explain(anchor: Beer, candidate: Beer, maxAxes = 3): string {
  const a = anchor.flavour.value;
  const b = candidate.flavour.value;

  const diffs = FLAVOUR_AXES
    .map((axis) => ({ axis, d: b[axis] - a[axis] }))
    .filter((x) => Math.abs(x.d) >= 1.5)
    .sort((x, y) => Math.abs(y.d) - Math.abs(x.d))
    .slice(0, maxAxes);

  if (diffs.length === 0) return `очень близко к ${anchor.name}`;

  const parts = diffs.map(({ axis, d }) => {
    const [low, high] = AXIS_LABELS[axis];
    const strength = Math.abs(d) >= 4 ? "заметно " : "";
    return strength + (d > 0 ? high : low);
  });

  return `как ${anchor.name}, но ${parts.join(", ")}`;
}

/** Режим опроса: описать вариант варки, которого ещё не существует */
export function describeSpec(anchor: Beer, deltas: Deltas): string {
  const target = applyDeltas(anchor.flavour.value, deltas);
  const pseudo = { ...anchor, name: "", flavour: { ...anchor.flavour, value: target } };
  return explain(anchor, pseudo as Beer);
}
