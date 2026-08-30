# -*- coding: utf-8 -*-
"""
Разведка: какие чешские пивные e-shopы отдают публичный XML-фид.

Отмечает невыполненный пункт чек-листа в DATA-SOURCES.md. Ничего не пишет
в data/ — только смотрит, что вообще доступно и какие там поля.

Вежливо: сначала robots.txt, запрещённые пути не трогаем, пауза между
запросами, честный User-Agent с контактом.
"""
import gzip
import io
import re
import sys
import functools
import time
import urllib.error
import urllib.request
import urllib.robotparser as rp

print = functools.partial(print, flush=True)  # иначе вывод копится до конца
UA = "BeerAtlasResearch/0.1 (+https://beeratlas.eu; contact via github.com/speedheaded/beeratlas)"

# Пути, по которым чешские платформы (Shoptet, Upgates, WooCommerce) обычно
# публикуют фиды для агрегаторов.
PATHS = [
    "/export/heureka.xml",
    "/heureka.xml",
    "/export/products.xml",
    "/export/googleMerchant.xml",
    "/google.xml",
    "/feed/heureka.xml",
    "/heureka/export.xml",
    "/export/heureka_cz.xml",
]

SHOPS = [
    "https://www.pivnidum.cz",
    "https://www.bevbox.cz",
    "https://www.pivo-pivo.cz",
    "https://www.pivnitrezor.cz",
    "https://www.beerland.cz",
    "https://www.naspivo.cz",
    "https://www.pivnisvet.cz",
    "https://www.zlatydzbanek.cz",
]


def get(url, timeout=25, limit=400_000):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept-Encoding": "gzip",
        "Accept": "application/xml,text/xml,*/*",
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read(limit)
        if r.headers.get("Content-Encoding") == "gzip":
            try:
                raw = gzip.decompress(raw)
            except Exception:
                pass
        return r.status, r.headers.get("Content-Type", ""), raw


def robots(base):
    p = rp.RobotFileParser()
    try:
        st, _, raw = get(base + "/robots.txt", timeout=15, limit=80_000)
        p.parse(raw.decode("utf-8", "replace").splitlines())
        return p
    except Exception:
        return None


ITEM = re.compile(r"(?is)<(SHOPITEM|item|entry)\b")
FIELD = re.compile(r"(?is)<([A-Za-z_][\w:.-]{1,40})>")


def probe(base):
    print("\n" + base)
    r = robots(base)
    for path in PATHS:
        url = base + path
        if r is not None and not r.can_fetch(UA, url):
            print("   %-28s robots.txt запрещает" % path)
            continue
        try:
            st, ct, raw = get(url)
        except urllib.error.HTTPError as e:
            if e.code not in (404, 403, 410):
                print("   %-28s HTTP %s" % (path, e.code))
            continue
        except Exception as e:
            print("   %-28s %s" % (path, str(e)[:44]))
            continue
        text = raw.decode("utf-8", "replace")
        if "<" not in text[:400]:
            continue
        items = len(ITEM.findall(text))
        fields = []
        for f in FIELD.findall(text[:60_000]):
            f = f.strip()
            if f not in fields and f.lower() not in ("shop",):
                fields.append(f)
        print("   %-28s HTTP %s  %-24s элементов в куске: %d" % (path, st, ct[:24], items))
        if fields:
            print("      поля: %s" % ", ".join(fields[:18]))
        return
    print("   публичного фида по типовым путям нет")


if __name__ == "__main__":
    only = sys.argv[1:] or SHOPS
    for s in only:
        try:
            probe(s)
        except Exception as e:
            print("\n%s\n   не отвечает: %s" % (s, str(e)[:60]))
        time.sleep(1.0)
