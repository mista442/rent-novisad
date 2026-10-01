# rent-novisad

Помощник по поиску долгосрочной аренды в Нови-Саде. Собирает объявления, отсеивает по вашим критериям и чёрному списку, переводит на русский и присылает в Telegram-бот **карточку с готовыми кнопками** «написать в WhatsApp/Telegram» — сообщение на сербском или английском уже вписано, вам остаётся нажать «Отправить» (полуавтомат, без риска бана номера).

## Что в карточке бота
1. Цена, комнаты, площадь, ссылка на объявление, пометки «уточнить: интернет…».
2. **Оригинал** объявления и **перевод на русский**.
3. Русский перевод сопроводительного сообщения, которое будет отправлено.
4. Кнопки: WhatsApp SR / EN, Telegram (по номеру или @нику), «отправить SR/EN» через выбор чата.

## Настройка (один раз)
1. Отредактируйте `config.yaml`: имя, бюджет, комнаты, районы, удобства, стоп-факторы. Описание критериев: [docs/CRITERIA.md](docs/CRITERIA.md).
2. Выберите вариант письма (`formal | friendly | short | detailed`) в `cover_letter.default_variant`. Все тексты sr/en/ru: [docs/COVER_LETTERS.md](docs/COVER_LETTERS.md). После правок `config.yaml` выполните `python -m rent_novisad docs`.
3. Создайте бота у @BotFather, напишите ему `/start`; chat id узнайте у @userinfobot.
4. Ключ Anthropic нужен только для перевода объявлений (без него придёт оригинал).
5. В GitHub: Settings → Secrets and variables → Actions → добавьте `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `ANTHROPIC_API_KEY`. Workflow `search` запускается каждые 3 часа и вручную (Actions → search → Run workflow).

## На любом устройстве
```bash
git clone https://github.com/mista442/rent-novisad && cd rent-novisad
pip install -e ".[dev]"
cp .env.example .env        # впишите токены
python -m rent_novisad run --dry-run   # проверка без записи в таблицу
pytest
```

## Таблица и статусы
`data/listings.csv` (статусы `new / contacted / replied / rejected / blacklisted / filtered`). Сменить статус: `python -m rent_novisad status <id> contacted`.

## Чёрный список
Проверяются телефон и @ник по `t.me/I_Black_list_Chat` (если у чата есть публичное превью) и по `data/blacklist.txt` (вставляйте туда номера/ники вручную). Совпадение — объявление не отправляется, в таблице статус `blacklisted`.

## Ограничения (честно)
- Парсинг Telegram-каналов написан по структуре `t.me/s/<канал>` и покрыт тестами на образце, **но не запускался на живых данных** — при первом запуске проверьте результат `--dry-run`.
- Сайты (halooglasi, 4zida, nekretnine, cityexpert) пока не реализованы: нужен их актуальный HTML. Пока вставляйте объявления с сайтов и из Facebook-групп в `data/manual_listings.yaml`.
- Если у чата чёрного списка нет публичного превью, пользуйтесь `data/blacklist.txt`.
- Ответы арендодателей приходят вам в WhatsApp/Telegram напрямую; статус в таблице меняйте командой выше.
