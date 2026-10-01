"""Генерирует docs/COVER_LETTERS.md и docs/CRITERIA.md из кода и config.yaml."""
from __future__ import annotations

from pathlib import Path

from .config import ROOT, load
from .messages import VARIANTS, render


def cover_letters(cfg: dict) -> str:
    out = ["# Сопроводительные сообщения\n", "Отправляется **sr** или **en**; **ru** — перевод для вас. Перегенерация: `python -m rent_novisad docs`.\n"]
    for key, v in VARIANTS.items():
        out.append(f"\n## {v['title_ru']} (`{key}`)\n")
        for lang, title in (("sr", "Srpski (латиница)"), ("en", "English"), ("ru", "Русский перевод")):
            out.append(f"### {title}\n\n```\n{render(key, lang, cfg, ' (Grbavica)' if lang != 'ru' else ' (Грбавица)')}\n```\n")
    return "\n".join(out)


def criteria(cfg: dict) -> str:
    s = cfg["search"]
    return f"""# Критерии поиска (из config.yaml)

| Параметр | Значение |
|---|---|
| Город | {s['city']} |
| Цена | {s.get('min_price_eur', 0)}–{s['max_price_eur']} € в месяц (курс {s['eur_to_rsd']} RSD/€) |
| Комнат | {s['min_rooms']:g}–{s['max_rooms']:g} (1 = garsonjera) |
| Площадь | от {s['min_area_m2']} м² |
| Желаемые районы | {', '.join(s['districts_prefer'])} |
| Исключить районы | {', '.join(s['districts_avoid'])} |
| Нужно (иначе пометка «уточнить») | {', '.join(s['required_amenities'])} |
| Приятно иметь | {', '.join(s['nice_to_have'])} |
| Стоп-факторы (отсев) | {', '.join(s['deal_breakers'])} |
| Свежесть | не старше {s['max_age_days']} дней |

Объявление из чёрного списка `t.me/{cfg['sources']['blacklist_chat']}` отбрасывается всегда.
Если в объявлении нет цены/комнат/площади — оно **не** отсеивается, а получает пометку для уточнения.
"""


def write() -> None:
    cfg = load()
    d = ROOT / "docs"
    d.mkdir(exist_ok=True)
    (d / "COVER_LETTERS.md").write_text(cover_letters(cfg), encoding="utf-8")
    (d / "CRITERIA.md").write_text(criteria(cfg), encoding="utf-8")
