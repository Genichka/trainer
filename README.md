<!-- шапка: бейджі (оновлює Claude) -->
<p align="center"><a href="https://genichka.github.io/trainer/"><img src="icon-192.png" width="96" alt="WordHunter"></a></p>

# WordHunter

<p align="center">

[![▶️ Грати](https://img.shields.io/badge/%D0%93%D1%80%D0%B0%D1%82%D0%B8-%D0%BE%D0%BD%D0%BB%D0%B0%D0%B9%D0%BD-3d71d9?style=for-the-badge)](https://genichka.github.io/trainer/) [![версія](https://img.shields.io/badge/dynamic/json?url=https://genichka.github.io/trainer/version.json&query=%24.version&label=%D0%B2%D0%B5%D1%80%D1%81%D1%96%D1%8F&color=73bf69&style=for-the-badge)](https://genichka.github.io/trainer/) [![оновлено](https://img.shields.io/github/last-commit/Genichka/trainer?label=%D0%BE%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%BE&style=for-the-badge&color=8e8e9e)](https://github.com/Genichka/trainer/commits/main) [![EnergyUA](https://img.shields.io/badge/YouTube-EnergyUA-f2495c?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@YevhenShchuka)

</p>

> Офлайн-тренажер англійських слів для української аудиторії: картки, кросворди, батли, голос.
>
> 💬 Ідеї, питання й помилки — у [Обговореннях](https://github.com/Genichka/trainer/discussions) або [Issues](https://github.com/Genichka/trainer/issues/new/choose).
<!-- /шапка -->

Мінімалістичний офлайн-тренажер англійської лексики для української аудиторії. Застосунок — `index.html` (інтерфейс і логіка) плюс словник у `data/*.js`: без бекенду, без збірки, без залежностей. Працює прямо в браузері й ставиться на телефон як PWA.

## Версія і оновлення

Так само, як у EnergyUA Junior. На головній під меню — `v3.0.0` і кнопка **«🔄 Оновити»**.

Нова версія ставиться лише з дозволу. Гра тихо перевіряє `version.json` поруч із собою (при запуску й раз на пів години).
Якщо там новіша — на головній зʼявляється вікно «🆕 Нова версія … · Що змінилось: • … · 🔄 Оновити / Пізніше»,
а кнопка під меню стає «🆕 Є версія …». Посеред тренування гра не питає — спитає, коли повернешся на головну.
Після оновлення — «✅ Оновлено: 3.0.0 → 3.0.1». Слова, прогрес і профілі зберігаються.

Як випустити нову версію:
1. В `index.html` змінити `const APP_VERSION="3.0.1"`.
2. У `version.json` вписати ту саму версію й коротко, що змінилось (до 8 пунктів):
   `{ "version": "3.0.1", "changes": ["…", "…"] }`
3. Залити обидва файли. `sw.js` між версіями **не міняти** — саме тому гра й не оновлюється сама.

## Словник

Дані лежать окремо від коду, по одній константі в рядку (`const NAME = <JSON>;`):

- `data/words.js` — рівні й слова (`LEVELS`), речення (`SENT`), транскрипції (`IPA`), іменники (`NOUNS`);
- `data/texts.js` — тексти рівнів, книги, словнички до них;
- `data/topics.js` — тематичні добірки (авторежим, батл);
- `data/voice.js` — схожі на слух варіанти для розпізнавання голосу.

Редагувати зручно через `tools/wh_data.py` (`load()` / `save()` / `delete_words()`).
Перед публікацією: `python3 tools/check_words.py` — має бути «помилок: 0»
(дублікати, речення без пропуску `{}`, відсутні транскрипції, англійська в перекладі).

Гра сама кладе `data/*.js` у кеш офлайн-оболонки, тому `sw.js` для цього міняти не треба.
