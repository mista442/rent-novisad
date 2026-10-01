from __future__ import annotations

from datetime import datetime, timedelta, timezone

from .models import Listing
from .parsing import AMENITIES, DEAL_BREAKERS, detect


def apply(listing: Listing, cfg: dict) -> tuple[bool, list[str]]:
    """Возвращает (подходит, причины отказа). Пустые причины + notes — подходит."""
    s = cfg["search"]
    why: list[str] = []
    text = listing.text.lower()

    if listing.price_eur is not None:
        if listing.price_eur > s["max_price_eur"]:
            why.append(f"цена {listing.price_eur:g}€ > {s['max_price_eur']}€")
        if listing.price_eur < s.get("min_price_eur", 0):
            why.append(f"цена {listing.price_eur:g}€ подозрительно низкая")
    else:
        listing.notes.append("цена не указана — уточнить")

    if listing.rooms is not None and not (s["min_rooms"] <= listing.rooms <= s["max_rooms"]):
        why.append(f"комнат {listing.rooms:g}")
    if listing.area_m2 is not None and listing.area_m2 < s["min_area_m2"]:
        why.append(f"площадь {listing.area_m2:g} м²")

    for d in s.get("districts_avoid", []):
        if d.lower() in text:
            why.append(f"район {d}")

    for bad in detect(listing.text, DEAL_BREAKERS) & set(s.get("deal_breakers", [])):
        why.append(f"стоп-фактор: {bad}")

    if listing.posted_at and s.get("max_age_days"):
        try:
            dt = datetime.fromisoformat(listing.posted_at.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            if datetime.now(timezone.utc) - dt > timedelta(days=s["max_age_days"]):
                why.append("старое объявление")
        except ValueError:
            pass

    have = detect(listing.text, AMENITIES)
    for need in s.get("required_amenities", []):
        if need not in have:
            listing.notes.append(f"уточнить: {need}")
    pref = [d for d in s.get("districts_prefer", []) if d.lower() in text]
    if pref:
        listing.notes.append("желаемый район: " + ", ".join(pref))
    return (not why, why)
