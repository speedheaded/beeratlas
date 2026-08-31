# -*- coding: utf-8 -*-
"""
Проверка языкового паритета. Падает, если чешская версия недоделана.

    python scripts/check_cs.py           # обе проверки
    python scripts/check_cs.py --static  # только ключи, без браузера

Зачем. `T(s)` возвращает перевод, а если ключа нет — сам английский оригинал.
Пропущенная обёртка не падает и ничего не пишет в консоль, она молча печатает
английский. За 30 августа так набралось двенадцать мест, и нашлись они
руками. Второй раз искать их вручную не хочется.

Две разные болезни, и ловятся они по-разному:

  1. Строка обёрнута в T(), но ключа в словаре нет. Ловится статически:
     вытаскиваем все аргументы T("…") из шаблона и сверяем со словарём.
  2. Строку вообще не обернули. Статически это не поймать без разбора JS,
     поэтому рендерим чешские маршруты и ищем в тексте английские слова.
     Именно так нашлись «Grain to glass», «and 2 more» и «Showing 120 of».
"""
import io
import json
import re
import shutil
import subprocess
import sys
import time
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from ui_cs import UI  # noqa: E402

def find_chrome():
    r"""Скрипт гоняется и из Windows, и из WSL, и с линукса. Жёсткий путь
       C:\... в WSL не существует — а раньше это не роняло проверку, она
       печатала «браузер не отработал» и всё равно говорила «паритет в порядке».
       Молча проходящая проверка хуже отсутствующей."""
    for c in (r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
              "/mnt/c/Program Files/Google/Chrome/Application/chrome.exe",
              "/mnt/c/Program Files (x86)/Google/Chrome/Application/chrome.exe"):
        if Path(c).exists():
            return c
    for name in ("google-chrome", "chromium", "chromium-browser", "chrome"):
        found = shutil.which(name)
        if found:
            return found
    return None


CHROME = find_chrome()


def chrome_url(p):
    r"""Адрес файла для Chrome. Windows-Chrome, запущенный из WSL, не видит
       /home/... — путь переводится через wslpath и получается UNC вида
       \\wsl.localhost\Ubuntu\home\... Его нельзя клеить как "file:///"+path:
       выходит file://///wsl..., и Chrome отдаёт файл ПРОСТЫМ ТЕКСТОМ вместо
       HTML. Проба тогда читает исходник, содержимое всех маршрутов совпадает,
       обход не заканчивается — и раньше это выглядело как «паритет в порядке»."""
    p = str(p)
    if CHROME and CHROME.startswith("/mnt/"):
        try:
            p = subprocess.run(["wslpath", "-w", p], capture_output=True,
                               check=True).stdout.decode().strip()
        except Exception:
            pass
    p = p.replace("\\", "/")
    return "file:" + p if p.startswith("//") else "file:///" + p
TEMPLATE = ROOT / "scripts" / "mockup_template.html"
MOCKUP = ROOT / "index.html"

ROUTES = ["#/cs/", "#/cs/find", "#/cs/beers", "#/cs/breweries",
          "#/cs/brewery/pivovar-svijany", "#/cs/beer/pilsner-urquell",
          "#/cs/beer/matuska-raptor", "#/cs/venues", "#/cs/brewing",
          "#/cs/ordering", "#/cs/correct", "#/cs/scan"]

# слова, которых в чешском тексте быть не может
EN = (r"\b(the|and|with|from|days?|brewery|breweries|style|this|that|what|where|"
      r"which|beer|beers|are|is|was|were|for|not|you|your|our|we|its|how|made|"
      r"about|more|than|only|every|each|says?|known|confirmed|normally|gravity|"
      r"strength|figures|rows|marked|top|glass|grain|showing|venue|venues|"
      r"phone|hours|unknown|source|barcode|listed|described|alcohol)\b")

# имена собственные и машинные строки: английские слова в них законны
# без флага (?i) в тексте: он уезжает в JavaScript, где такого синтаксиса нет,
# скрипт молча падает на разборе и проба возвращает пусто — то есть «всё чисто»
ALLOW = re.compile(r"(beer atlas|open ?food ?facts|openstreetmap|wikidata|"
                   r"odbl|cc0|craft|beer factory|bar\b|pub\b|lidl|max laser|"
                   r"cash only|beer knír|beer spot|^mo-|^tu-|^we|^th|^fr|^sa|^su|"
                   r"punk ipa|brewdog|guinness|stella artois|corona|heineken|"
                   r"pilsner urquell|budweiser|lager|premium|original|black panda|"
                   r"london calling|summer krush|less sugars|pop & roll|seaman|yes!)")

T_CALL = re.compile(r'T\(\s*"((?:[^"\\]|\\.)*)"\s*\)')


def static(verbose=True):
    src = io.open(TEMPLATE, encoding="utf-8").read()
    keys = set()
    for raw in T_CALL.findall(src):
        # json разбирает те же escape-последовательности, что и JS, и не портит
        # UTF-8 — в отличие от unicode_escape, который читает байты как latin-1
        # и превращает тире в мусор
        try:
            keys.add(json.loads('"' + raw + '"'))
        except ValueError:
            keys.add(raw)
    missing = sorted(k for k in keys if k not in UI)
    if verbose:
        print("строк, обёрнутых в T(): %d   ключей в словаре: %d" % (len(keys), len(UI)))
    if missing:
        print("НЕТ ПЕРЕВОДА для %d строк — в чешском режиме они выйдут английскими:" % len(missing))
        for k in missing:
            print("   %s" % k[:96].replace("\n", " "))
    unused = sorted(k for k in UI if k not in keys)
    if unused and verbose:
        print("в словаре есть %d ключей, которых нет в шаблоне (не ошибка, но мусор):" % len(unused))
        for k in unused[:8]:
            print("   %s" % k[:80].replace("\n", " "))
    return len(missing)




def data_strings():
    """Значения из данных, а не текст интерфейса.

    Марка `more` из тега OSM или бар «Cash Only Bar» выглядят как английские
    слова, но переводить их нечего. Отличить по словарю нельзя, поэтому
    сверяем с тем, что лежит в самих данных.
    """
    out = set()
    src = io.open(MOCKUP, encoding="utf-8").read()
    m = re.search(r"const DATA = (\{.*?\});\n", src, re.S)
    if not m:
        return out
    d = json.loads(m.group(1))
    for v in d.get("venues", []):
        out.add(v.get("n", ""))
        out.update(v.get("bh", []))
    for b in d.get("breweries", []):
        out.update(filter(None, (b.get("name"), b.get("nameEn"), b.get("city"))))
    for b in d.get("beers", []) + d.get("listed", []):
        out.update(filter(None, (b.get("name"), b.get("cs"), b.get("style"))))
    for h in d.get("hints", []):
        out.add(h.get("brand", ""))
        out.update(h.get("venues", []))
    return {x.strip() for x in out if x and len(x.strip()) >= 3}


TAGS = re.compile(r"<(script|style)\b.*?</\1>", re.S | re.I)


def page_text(html):
    """Видимый текст страницы. Скрипты и стили выброшены: иначе в проверку
       едет сам исходник на 576 КБ, где английского сколько угодно."""
    import html as H
    return [H.unescape(t).strip()
            for t in re.split(r"<[^>]+>", TAGS.sub(" ", html))]


def rendered():
    """Раньше здесь была одна страница с iframe, который перебирал маршруты.
       Под --virtual-time-budget это не работает: таймеры внешней страницы
       промотываются раньше, чем iframe успевает загрузить 590 КБ, и обход
       вставал молча. Гоняем браузер по одному разу на маршрут — медленнее,
       зато каждый маршрут гарантированно отрисован."""
    if not MOCKUP.exists():
        print("нет index.html — сначала python scripts/build_mockup.py")
        return -1
    if not CHROME:
        print("Chrome не найден — проверка рендером не выполнена")
        return -1

    # ALLOW собран без (?i): раньше он уезжал в JavaScript, где такого
    # синтаксиса нет, а нечувствительность задавалась флагом new RegExp(...,'i').
    # Здесь сравнение идёт в Python, поэтому флаг нужно поставить явно —
    # иначе «Prague Beer Atlas» не совпадёт с шаблоном в нижнем регистре.
    base = chrome_url(MOCKUP)
    allow = re.compile(ALLOW.pattern, re.I)
    data = set(data_strings())
    en = re.compile(EN, re.I)
    rows, broken = [], 0

    for r in ROUTES:
        # запущенные вплотную копии Chrome делят профиль по умолчанию и мешают
        # друг другу: часть маршрутов отдаёт неотрисованную оболочку
        time.sleep(1.5)
        # headless отрисовывает не с первой попытки примерно в трети случаев:
        # страница на 590 КБ иногда не успевает за отведённое виртуальное время
        parts = None
        for attempt in range(5):
            try:
                out = subprocess.run(
                    [CHROME, "--headless=new", "--disable-gpu", "--no-first-run",
                     "--no-default-browser-check", "--disable-extensions",
                     "--allow-file-access-from-files", "--window-size=1200,900",
                     "--virtual-time-budget=%d" % (40000 + attempt * 15000),
                     "--dump-dom", base + r],
                    capture_output=True, timeout=180).stdout.decode("utf-8", "replace")
            except Exception as e:
                print("браузер не отработал на %s: %s" % (r, e))
                return -1
            got = page_text(out)
            if sum(len(t) for t in got) < 400 and attempt < 4:
                time.sleep(2.0)  # подряд запущенные копии Chrome мешают друг другу
            # статическая оболочка без отрисовки — около сотни знаков
            if sum(len(t) for t in got) >= 400:
                parts = got
                break
        if parts is None:
            print("НЕ ОТРИСОВАЛСЯ за пять попыток: %s" % r)
            broken += 1
            continue

        seen = set()
        for t in parts:
            if len(t) < 3 or t in seen:
                continue
            if not en.search(t) or allow.search(t) or t in data:
                continue
            seen.add(t)
            rows.append("%s | %s" % (r, t[:110]))

    print("\nобойдено чешских маршрутов: %d" % (len(ROUTES) - broken))
    if broken:
        print("не отрисовалось маршрутов: %d — паритет НЕ проверен" % broken)
        return -1
    if rows:
        print("АНГЛИЙСКИЙ В ЧЕШСКОМ РЕЖИМЕ, %d мест:" % len(rows))
        for x in rows:
            print("   %s" % x)
    return len(rows)


def main():
    bad = static()
    if "--static" not in sys.argv:
        r = rendered()
        if r < 0:
            print("\nПРОВЕРКА РЕНДЕРОМ НЕ ОТРАБОТАЛА — паритет НЕ подтверждён")
            return 2
        bad += r
    if bad:
        print("\nПАРИТЕТ НАРУШЕН: %d мест" % bad)
        return 1
    print("\nпаритет в порядке")
    return 0


if __name__ == "__main__":
    sys.exit(main())
