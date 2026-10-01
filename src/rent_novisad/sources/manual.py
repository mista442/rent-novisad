"""Объявления, вставленные вручную (Facebook, сайты): data/manual_listings.yaml.

Формат:
- url: https://...
  text: |
    полный текст объявления
"""
from __future__ import annotations

from pathlib import Path

import yaml

from ..config import ROOT
from ..models import Listing
from ..parsing import extract_area, extract_phones, extract_price_eur, extract_rooms, extract_usernames


def fetch(path: str, eur_to_rsd: float = 117) -> list[Listing]:
    p = ROOT / path
    if not p.exists():
        return []
    items = yaml.safe_load(p.read_text(encoding="utf-8")) or []
    return [
        Listing(
            source="manual", url=i.get("url", ""), text=i["text"], posted_at=str(i.get("date", "")),
            phones=extract_phones(i["text"]) + [x for x in i.get("phones", [])],
            usernames=extract_usernames(i["text"]),
            price_eur=extract_price_eur(i["text"], eur_to_rsd), rooms=extract_rooms(i["text"]), area_m2=extract_area(i["text"]),
        )
        for i in items
    ]
