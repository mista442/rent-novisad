"""Отправка карточки в Telegram-бот: оригинал + перевод + готовые ссылки на отправку."""
from __future__ import annotations

import html

import requests

from . import links
from .config import env
from .messages import render
from .models import Listing

LIMIT = 3900


def build(l: Listing, cfg: dict, variant: str) -> tuple[str, list[list[dict]]]:
    price = f"{l.price_eur:g} €" if l.price_eur else "цена ?"
    ref = f" ({price})" if l.price_eur else ""
    lang = "sr"
    msg_sr = render(variant, "sr", cfg, ref)
    msg_en = render(variant, "en", cfg, ref)
    msg_ru = render(variant, "ru", cfg, ref)

    head = f"🏠 <b>{html.escape(price)}</b> · комнат: {l.rooms or '?'} · {l.area_m2 or '?'} м² · id <code>{l.id}</code>\n{html.escape(l.url)}"
    if l.notes:
        head += "\n⚠️ " + html.escape("; ".join(l.notes))
    body = f"\n\n<b>Оригинал:</b>\n{html.escape(l.text)}"
    if l.translation_ru:
        body += f"\n\n<b>Перевод:</b>\n{html.escape(l.translation_ru)}"
    body += f"\n\n<b>Сообщение (вариант {variant}), RU-перевод:</b>\n{html.escape(msg_ru)}"
    text = (head + body)[:LIMIT]

    rows: list[list[dict]] = []
    for ph in l.phones[:1]:
        rows.append([{"text": "WhatsApp SR", "url": links.whatsapp(ph, msg_sr)}, {"text": "WhatsApp EN", "url": links.whatsapp(ph, msg_en)}])
        rows.append([{"text": "Telegram (по номеру)", "url": links.telegram_phone(ph)}])
    for u in l.usernames[:1]:
        rows.append([{"text": f"Telegram @{u}", "url": links.telegram_user(u)}])
    rows.append([{"text": "Telegram: отправить SR", "url": links.telegram_share(msg_sr)}, {"text": "EN", "url": links.telegram_share(msg_en)}])
    return text, rows


def send(l: Listing, cfg: dict, variant: str) -> bool:
    token, chat = env("TELEGRAM_BOT_TOKEN"), env("TELEGRAM_CHAT_ID")
    text, rows = build(l, cfg, variant)
    if not token or not chat:
        print(text)
        return False
    r = requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": chat, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True, "reply_markup": {"inline_keyboard": rows}},
        timeout=30,
    )
    if not r.ok:
        print(f"[notify] {r.status_code}: {r.text[:200]}")
    return r.ok
