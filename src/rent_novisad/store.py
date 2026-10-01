from __future__ import annotations

import csv
from dataclasses import asdict

from .config import ROOT
from .models import Listing

FIELDS = ["id", "status", "source", "url", "posted_at", "price_eur", "rooms", "area_m2", "phones", "usernames", "notes", "text", "translation_ru"]
PATH = ROOT / "data" / "listings.csv"
STATUSES = ("new", "contacted", "replied", "rejected", "blacklisted", "filtered")


def load_ids() -> dict[str, str]:
    if not PATH.exists():
        return {}
    with open(PATH, encoding="utf-8", newline="") as f:
        return {r["id"]: r["status"] for r in csv.DictReader(f)}


def append(listings: list[Listing]) -> None:
    PATH.parent.mkdir(exist_ok=True)
    new_file = not PATH.exists()
    with open(PATH, "a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, FIELDS)
        if new_file:
            w.writeheader()
        for l in listings:
            d = asdict(l)
            d.update(id=l.id, phones=";".join(l.phones), usernames=";".join(l.usernames), notes="; ".join(l.notes))
            w.writerow({k: d[k] for k in FIELDS})


def set_status(listing_id: str, status: str) -> bool:
    if status not in STATUSES or not PATH.exists():
        return False
    with open(PATH, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    hit = False
    for r in rows:
        if r["id"] == listing_id:
            r["status"], hit = status, True
    if hit:
        with open(PATH, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, FIELDS)
            w.writeheader()
            w.writerows(rows)
    return hit
