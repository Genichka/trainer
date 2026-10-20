"""Читання й запис словника WordHunter (data/*.js).

Кожен файл даних — рядки виду «const NAME = <JSON>;» (NOUNS — «const NOUNS=new Set([...]);»).
Приклад:
    from wh_data import load, save
    d = load()                 # {'LEVELS': [...], 'SENT': {...}, 'IPA': {...}, 'NOUNS': set(...), ...}
    d['SENT']['pump'] = 'The {} is running.'
    save(d)
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = ["data/words.js", "data/texts.js", "data/topics.js", "data/voice.js"]
LINE = re.compile(r"^const (\w+)\s*=\s*(new Set\()?(.*?)\)?;\s*$", re.S)


def _parse(path):
    out = {}
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        for line in f:
            m = LINE.match(line.rstrip("\n"))
            if not m:
                continue
            name, is_set, body = m.groups()
            val = json.loads(body)
            out[name] = (set(val) if is_set else val, path, bool(is_set))
    return out


def load():
    """Усі константи з усіх файлів даних: {NAME: value}."""
    d = {}
    for p in FILES:
        for k, (v, _, _) in _parse(p).items():
            d[k] = v
    return d


def save(d):
    """Записує змінені значення назад у ті самі файли й рядки."""
    for p in FILES:
        full = os.path.join(ROOT, p)
        with open(full, encoding="utf-8") as f:
            lines = f.read().split("\n")
        for i, line in enumerate(lines):
            m = LINE.match(line)
            if not m or m.group(1) not in d:
                continue
            name, is_set = m.group(1), bool(m.group(2))
            v = d[name]
            if is_set:
                lines[i] = "const %s=new Set(%s);" % (name, json.dumps(sorted(v), ensure_ascii=False))
            else:
                lines[i] = "const %s = %s;" % (name, json.dumps(v, ensure_ascii=False, separators=(",", ":")))
        with open(full, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))


def delete_words(d, words):
    """Прибирає слова з рівнів, речень, транскрипцій та іменників."""
    words = set(words)
    for lv in d["LEVELS"]:
        lv["words"] = [w for w in lv["words"] if w[0] not in words]
    for k in ("SENT", "IPA"):
        for w in words:
            d[k].pop(w, None)
    d["NOUNS"] -= words
