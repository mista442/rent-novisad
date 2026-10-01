"""Публичное веб-превью каналов: https://t.me/s/<канал> (без логина)."""
from __future__ import annotations

import requests
from bs4 import BeautifulSoup

from ..models import Listing
from ..parsing import extract_area, extract_phones, extract_price_eur, extract_rooms, extract_usernames

UA = {"User-Agent": "Mozilla/5.0 (rent-novisad personal search)"}


def parse(html: str, channel: str, eur_to_rsd: float = 117) -> list[Listing]:
    soup = BeautifulSoup(html, "html.parser")
    out: list[Listing] = []
    for wrap in soup.select(".tgme_widget_message_wrap"):
        body = wrap.select_one(".tgme_widget_message_text")
        if not body:
            continue
        for br in body.find_all("br"):
            br.replace_with("\n")
        text = body.get_text().strip()
        link = wrap.select_one("a.tgme_widget_message_date")
        time = wrap.select_one("time")
        # tel:/mailto: ссылки и @ники внутри текста
        text_with_links = text + " " + " ".join(a.get("href", "") for a in body.select("a[href^='tel:']"))
        out.append(
            Listing(
                source=f"telegram:{channel}",
                url=link["href"] if link and link.get("href") else f"https://t.me/{channel}",
                text=text,
                posted_at=time["datetime"] if time and time.get("datetime") else "",
                phones=extract_phones(text_with_links),
                usernames=extract_usernames(text),
                price_eur=extract_price_eur(text, eur_to_rsd),
                rooms=extract_rooms(text),
                area_m2=extract_area(text),
            )
        )
    return out


def fetch(channel: str, eur_to_rsd: float = 117) -> list[Listing]:
    r = requests.get(f"https://t.me/s/{channel}", headers=UA, timeout=30)
    r.raise_for_status()
    return parse(r.text, channel, eur_to_rsd)
