# -*- coding: utf-8 -*-
"""
Разбор снятых линеек: что нового, что расходится с каталогом, что проверить.

    python scripts/review_lineups.py            # сводка
    python scripts/review_lineups.py --new      # только сорта, которых нет в каталоге
    python scripts/review_lineups.py --conflict # только расхождения в числах

Ничего не пишет. Это лист сверки для человека: сырьё из data/lineups_raw.json
попадает в каталог только после подтверждения, потому что автоматический разбор
чужой вёрстки ошибается — и ошибается тихо.
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def key(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]+", "", s)


def main():
    raw_path = DATA / "lineups_raw.json"
    if not raw_path.exists():
        print("нет data/lineups_raw.json — сначала python scripts/fetch_lineups.py")
        return
    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    beers = json.loads((DATA / "beers.json").read_text(encoding="utf-8"))

    have = {}
    for b in beers:
        have.setdefault(b["breweryId"], {})[key(b["name"])] = b
        have[b["breweryId"]][key(b.get("menuNameCs"))] = b

    only_new = "--new" in sys.argv
    only_conf = "--conflict" in sys.argv

    n_new = n_conf = n_ok = n_review = 0
    for r in raw:
        rows = []
        for x in r["beers"]:
            if not x["name"]:
                continue
            cur = have.get(r["breweryId"], {}).get(key(x["name"]))
            if cur is None:
                n_new += 1
                if not only_conf:
                    rows.append(("НОВЫЙ   ", x, ""))
                continue
            diff = []
            cp = (cur.get("plato") or {}).get("value")
            ca = (cur.get("abv") or {}).get("value")
            if x["plato"] and cp is not None and abs(float(x["plato"]) - float(cp)) > 0.05:
                diff.append("° в каталоге %s, на сайте %s" % (cp, x["plato"]))
            if x["abv"] and ca is not None and abs(float(x["abv"]) - float(ca)) > 0.05:
                diff.append("%% в каталоге %s, на сайте %s" % (ca, x["abv"]))
            if diff:
                n_conf += 1
                if not only_new:
                    rows.append(("РАСХОЖД.", x, "; ".join(diff)))
            else:
                n_ok += 1
        if not rows:
            continue
        print("\n%s  (%s)" % (r["brewery"], r["site"]))
        for tag, x, note in rows:
            mark = " ПРОВЕРИТЬ" if x["needsReview"] else ""
            if x["needsReview"]:
                n_review += 1
            print("  %s %-34s °:%-5s %%:%-5s%s" %
                  (tag, x["name"][:34], x["plato"] or "-", x["abv"] or "-", mark))
            if note:
                print("           %s" % note)
            print("           %s" % x["url"])

    fetched = sum(1 for r in raw if not r.get("error"))
    empty = [r["brewery"] for r in raw if not r["beers"]]
    print("\n" + "─" * 68)
    print("пивоварен обойдено: %d   ничего не отдали: %d" % (fetched, len(empty)))
    if empty:
        print("   ", ", ".join(empty))
    print("совпало с каталогом: %d   новых: %d   расхождений: %d" % (n_ok, n_new, n_conf))
    print("помечено «проверить» (степень записана через %%): %d" % n_review)
    print("\nНичего не перенесено в каталог. Подтверждённое вносится руками")
    print("в scripts/beer_text.py и data/, с адресом источника и датой.")


if __name__ == "__main__":
    main()
