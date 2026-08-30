-- Чярки: голоса за сорта.
--
-- Ключевое решение: таблица append-only, по строке на голос. Счётчик вида
-- likes = likes + 1 навсегда закрывает срезы «за неделю» и «за месяц» —
-- переиграть это потом нельзя, поэтому пишем события с самого начала.
--
-- Персональных данных не храним. Устройство — случайный идентификатор,
-- сгенерированный в браузере; IP не пишется никуда, для ограничения частоты
-- берётся его хеш с солью, которая меняется ежедневно и нигде не сохраняется.

create table vote (
  id          bigserial primary key,
  beer_id     text        not null,
  kind        smallint    not null check (kind in (1, -1)),  -- 1 = čárka, -1 = not for me
  device      uuid        not null,        -- случайный, живёт в localStorage
  created_at  timestamptz not null default now()
);

-- одно мнение на устройство и сорт; повторный голос обновляет, а не плодит
create unique index vote_one_per_device on vote (beer_id, device);

create index vote_by_beer_time on vote (beer_id, created_at desc);
create index vote_recent on vote (created_at desc);

-- Ограничение частоты. Хранится только хеш и сутки, сам IP не пишется.
create table vote_throttle (
  ip_hash  bytea   not null,
  day      date    not null default current_date,
  n        integer not null default 1,
  primary key (ip_hash, day)
);

-- ── чтение ────────────────────────────────────────────────────────────────
-- «Not for me» в публичных числах не участвует: он кормит подбор и никогда
-- не показывается. Это продуктовое решение, а не техническое, и закреплено
-- прямо в представлении, чтобы его нельзя было случайно нарушить в запросе.

create view vote_public as
select beer_id,
       count(*) filter (where kind = 1)                                          as strokes_all,
       count(*) filter (where kind = 1 and created_at > now() - interval '7 days')  as strokes_week,
       count(*) filter (where kind = 1 and created_at > now() - interval '30 days') as strokes_month,
       count(*) filter (where kind = 1 and created_at > now() - interval '365 days') as strokes_year
from vote
group by beer_id;

-- ── запись ────────────────────────────────────────────────────────────────

create or replace function cast_vote(p_beer text, p_kind smallint, p_device uuid)
returns integer
language plpgsql
as $$
declare
  n integer;
begin
  insert into vote (beer_id, kind, device)
  values (p_beer, p_kind, p_device)
  on conflict (beer_id, device)
  do update set kind = excluded.kind, created_at = now();

  select strokes_all into n from vote_public where beer_id = p_beer;
  return coalesce(n, 0);
end;
$$;

-- ── что понадобится позже ─────────────────────────────────────────────────
-- Настоящая ценность чярок не в счётчике, а в рёбрах: кто поставил чярку
-- этому, поставил и тому. На этом вкусовые векторы перестают быть выводом
-- модели и становятся наблюдением. Порог осмысленности — порядка тысячи
-- голосов; до него запрос ниже возвращает шум.

create view co_liked as
select a.beer_id as beer_id, b.beer_id as also_id, count(*) as n
from vote a
join vote b on a.device = b.device and a.beer_id <> b.beer_id
where a.kind = 1 and b.kind = 1
group by 1, 2
having count(*) >= 5;
