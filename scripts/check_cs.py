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
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from ui_cs import UI  # noqa: E402

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
TEMPLATE = ROOT / "scripts" / "mockup_template.html"
MOCKUP = ROOT / "mockup" / "index.html"

ROUTES = ["#/cs/", "#/cs/find", "#/cs/beers", "#/cs/breweries",
          "#/cs/brewery/pivovar-svijany", "#/cs/beer/pilsner-urquell",
          "#/cs/beer/matuska-raptor", "#/cs/venues", "#/cs/brewing",
          "#/cs/ordering", "#/cs/correct"]

# слова, которых в чешском тексте быть не может
EN = (r"\b(the|and|with|from|days?|brewery|breweries|style|this|that|what|where|"
      r"which|beer|beers|are|is|was|were|for|not|you|your|our|we|its|how|made|"
      r"about|more|than|only|every|each|says?|known|confirmed|normally|gravity|"
      r"strength|figures|rows|marked|top|glass|grain|showing|venue|venues|"
      r"phone|hours|unknown|source|barcode|listed|described|alcohol)\b")

# имена собственные и машинные строки: английские слова в них законны
# без флага (?i) в тексте: он уезжает в JavaScript, где такого синтаксиса нет,
# скрипт молча падает на разборе и проба возвращает пусто — то есть «всё чисто»
ALLOW = re.compile(r"(prague beer atlas|open ?food ?facts|openstreetmap|wikidata|"
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


PROBE = """<body><iframe id="f" width="1100" height="900" style="border:0"></iframe>
<pre id="OUT">пусто</pre><script>
var R=%s, i=0, out=[], f=document.getElementById('f');
var EN=new RegExp(%s,'i'), OK=new RegExp(%s,'i');
var DATA_STR={}; %s.forEach(function(x){DATA_STR[x]=1;});
function step(){
  if(i>=R.length){document.getElementById('OUT').textContent=out.join("\\n");return;}
  var r=R[i++]; f.src="file:///%s"+r;
  setTimeout(function(){
    try{
      var d=f.contentDocument, seen={};
      var w=d.createTreeWalker(d.body,NodeFilter.SHOW_TEXT), n;
      while((n=w.nextNode())){
        var t=(n.nodeValue||"").trim();
        if(t.length<3||seen[t]) continue;
        if(!EN.test(t)) continue;
        if(OK.test(t)||DATA_STR[t]) continue;
        seen[t]=1; out.push(r+" | "+t.slice(0,110));
      }
    }catch(e){out.push("ОШИБКА "+r+" "+e.message);}
    step();
  },1200);
}
step();
</script>"""


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


def rendered():
    if not MOCKUP.exists():
        print("нет mockup/index.html — сначала python scripts/build_mockup.py")
        return 0
    page = PROBE % (json.dumps(ROUTES), json.dumps(EN), json.dumps(ALLOW.pattern),
                    json.dumps(sorted(data_strings())), str(MOCKUP).replace("\\", "/"))
    tmp = Path(tempfile.gettempdir()) / "beeratlas_check_cs.html"
    tmp.write_text(page, encoding="utf-8")
    try:
        out = subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu", "--allow-file-access-from-files",
             "--window-size=1200,900", "--virtual-time-budget=40000", "--dump-dom",
             "file:///" + str(tmp).replace("\\", "/")],
            capture_output=True, timeout=180).stdout.decode("utf-8", "replace")
    except Exception as e:
        print("браузер не отработал: %s" % e)
        return 0
    m = re.search(r'<pre id="OUT">(.*?)</pre>', out, re.S)
    if not m:
        print("проба не вернула результат — проверьте вручную")
        return 0
    import html as H
    rows = [r for r in H.unescape(m.group(1)).split("\n") if r.strip() and r.strip() != "пусто"]
    print("\nобойдено чешских маршрутов: %d" % len(ROUTES))
    if rows:
        print("АНГЛИЙСКИЙ В ЧЕШСКОМ РЕЖИМЕ, %d мест:" % len(rows))
        for r in rows:
            print("   %s" % r)
    return len(rows)


def main():
    bad = static()
    if "--static" not in sys.argv:
        bad += rendered()
    if bad:
        print("\nПАРИТЕТ НАРУШЕН: %d мест" % bad)
        return 1
    print("\nпаритет в порядке")
    return 0


if __name__ == "__main__":
    sys.exit(main())
