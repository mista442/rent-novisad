from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field


@dataclass
class Listing:
    source: str                      # "telegram:novisad_stan", "manual", ...
    url: str
    text: str                        # оригинал объявления
    posted_at: str = ""              # ISO-дата
    phones: list[str] = field(default_factory=list)
    usernames: list[str] = field(default_factory=list)   # Telegram-ники
    price_eur: float | None = None
    rooms: float | None = None
    area_m2: float | None = None
    translation_ru: str = ""
    notes: list[str] = field(default_factory=list)       # «уточнить: интернет» и т.п.
    status: str = "new"

    @property
    def id(self) -> str:
        key = "|".join(sorted(self.phones)) or self.url
        body = re.sub(r"\W+", "", self.text.lower())[:80]
        key += f"|{self.price_eur}|{body}"
        return hashlib.sha1(key.encode()).hexdigest()[:10]
