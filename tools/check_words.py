"""Перевірка словника WordHunter. Запуск: python3 tools/check_words.py

Помилки (код виходу 1):
  - слово повторюється в кількох рівнях;
  - немає речення, або в реченні не рівно один пропуск {};
  - немає транскрипції;
  - порожній переклад або емодзі;
  - у перекладі англійські слова поза дужками.
Попередження (переглянути вручну): однаковий переклад у словах одного рівня (часто це синоніми —
гра їх враховує), однина/множина (glass / glasses), дефіс/пробіл (take off / take-off).
"""
import collections
import re
import sys

from wh_data import load


def main():
    d = load()
    L, SENT, IPA = d["LEVELS"], d["SENT"], d["IPA"]
    err, warn = [], []
    where = collections.defaultdict(list)
    for lv in L:
        for w in lv["words"]:
            where[w[0]].append(lv["id"])
    for en, ls in where.items():
        if len(ls) > 1:
            err.append("дубль у рівнях %s: %s" % (",".join(ls), en))

    norm = collections.defaultdict(list)
    for en in where:
        k = en.lower().replace("-", " ")
        norm[k].append(en)
        for suf, base in (("ies", "y"), ("es", ""), ("s", "")):
            if k.endswith(suf) and len(k) > 4 and (k[: -len(suf)] + base) in {x.lower().replace("-", " ") for x in where}:
                warn.append("однина/множина: %s / %s" % (k[: -len(suf)] + base, en))
                break
    for k, v in norm.items():
        if len(v) > 1:
            warn.append("варіанти написання: %s" % " / ".join(v))

    for lv in L:
        by_ua = collections.defaultdict(list)
        for en, ua, em in lv["words"]:
            tag = "%s:%s" % (lv["id"], en)
            s = SENT.get(en)
            if not s:
                err.append("немає речення: " + tag)
            elif s.count("{}") != 1:
                err.append("у реченні не один пропуск: %s — %s" % (tag, s))
            if not IPA.get(en):
                err.append("немає транскрипції: " + tag)
            if not ua.strip():
                err.append("порожній переклад: " + tag)
            if not em.strip():
                err.append("немає емодзі: " + tag)
            if re.search(r"[A-Za-z]{3,}", re.sub(r"\([^)]*\)", "", ua)):
                err.append("англійська в перекладі: %s — %s" % (tag, ua))
            by_ua[ua.strip().lower()].append(en)
        for ua, ens in by_ua.items():
            if len(ens) > 1:
                warn.append("однаковий переклад у %s: %s → %s" % (lv["id"], ", ".join(ens), ua))

    for m in err:
        print("ПОМИЛКА  " + m)
    for m in warn:
        print("увага    " + m)
    total = sum(len(lv["words"]) for lv in L)
    print("\nслів: %d · помилок: %d · попереджень: %d" % (total, len(err), len(warn)))
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main())
