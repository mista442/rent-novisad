"""Извлечение телефонов, цены, комнат, площади и удобств из текста объявления (sr/ru/en)."""
from __future__ import annotations

import re

PHONE_RE = re.compile(r"(?:\+|00)?381[\s\-/]?\(?0?\)?6\d[\s\-/]?\d{3}[\s\-/]?\d{3,4}|\b06\d[\s\-/]?\d{3}[\s\-/]?\d{3,4}\b")
USERNAME_RE = re.compile(r"(?<![\w/])@([A-Za-z][\w]{4,31})")


def normalize_phone(raw: str) -> str:
    digits = re.sub(r"\D", "", raw)
    if digits.startswith("00"):
        digits = digits[2:]
    if digits.startswith("0"):
        digits = "381" + digits[1:]
    return digits


def extract_phones(text: str) -> list[str]:
    seen: list[str] = []
    for m in PHONE_RE.finditer(text):
        p = normalize_phone(m.group())
        if p not in seen:
            seen.append(p)
    return seen


def extract_usernames(text: str) -> list[str]:
    return list(dict.fromkeys(USERNAME_RE.findall(text)))


NUM = r"(?<![\w.,])(\d{1,3}(?:[.,\s]\d{3})+|\d+(?:[.,]\d{1,2})?)"


def extract_price_eur(text: str, eur_to_rsd: float = 117) -> float | None:
    t = text.lower().replace(" ", " ")
    m = re.search(NUM + r"\s*(?:€|eur|evra|евро|euro)", t) or re.search(r"(?:€|eur)\s*" + NUM, t)
    if m:
        return _num(m.group(1))
    m = re.search(NUM + r"\s*(?:din|rsd|дин)", t)
    if m:
        v = _num(m.group(1))
        return round(v / eur_to_rsd) if v else None
    return None


def _num(s: str) -> float | None:
    s = s.strip().replace(" ", "")
    if re.fullmatch(r"\d{1,3}([.,]\d{3})+", s):
        s = re.sub(r"[.,]", "", s)
    else:
        s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


ROOM_WORDS = [
    (r"garsonjer|studio|гарсоњер|студи", 1.0),
    (r"jednoiposoban|1\.5|1,5|полтор", 1.5),
    (r"jednosoban|1[- ]?sob|однокомнат|1 комнат|one[- ]bedroom|1[- ]room", 1.0),
    (r"dvoiposoban|2\.5|2,5", 2.5),
    (r"dvosoban|2[- ]?sob|двухкомнат|2 комнат|two[- ]bedroom|2[- ]room", 2.0),
    (r"trosoban|3[- ]?sob|трёхкомнат|трехкомнат|3 комнат", 3.0),
]


def extract_rooms(text: str) -> float | None:
    t = text.lower()
    for pat, val in ROOM_WORDS:
        if re.search(pat, t):
            return val
    return None


def extract_area(text: str) -> float | None:
    m = re.search(r"(\d{2,3})\s*(?:m2|m²|kvm|кв\.?\s?м|sqm)", text.lower())
    return float(m.group(1)) if m else None


# Ключевые слова (sr латиница/кириллица, ru, en)
AMENITIES = {
    "internet": r"internet|wi-?fi|optik|kabl|интернет|вай-?фай",
    "stove": r"šporet|sporet|rerna|плита|шпорет|stove|cooker|kuhinja opremljena",
    "fridge": r"frižider|frizider|fri[zž]|холодильник|fridge|refrigerator",
    "washing_machine": r"veš ?ma[sš]ina|ves ?masina|стиральн|washing machine|washer",
    "air_conditioning": r"klima|кондиционер|air.?condition|\bac\b",
    "balcony": r"terasa|balkon|лоджи|балкон|terrace",
    "elevator": r"lift|лифт|elevator",
    "central_heating": r"centralno grejanje|daljinsko|toplana|центральн\w+ отоплен|central heating",
}
DEAL_BREAKERS = {
    "agency_fee": r"provizij|agencijsk|комисси|agency fee|commission",
    "no_registration": r"bez prijave|без регистрац|no registration|ne mo[zž]e prijava",
    "students_only": r"samo (?:za )?student|isključivo student|только студент|students only",
    "short_term_only": r"kratkoročn|dnevn|noćenj|посуточ|short.?term|airbnb",
}


def detect(text: str, table: dict[str, str]) -> set[str]:
    t = text.lower()
    return {k for k, pat in table.items() if re.search(pat, t)}
