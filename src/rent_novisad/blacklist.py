"""Чёрный список арендодателей: публичное превью t.me/s/<чат> + локальный data/blacklist.txt."""
from __future__ import annotations

import re

import requests
from bs4 import BeautifulSoup

from .config import ROOT
from .models import Listing
from .parsing import extract_phones, extract_usernames

LOCAL = ROOT / "data" / "blacklist.txt"


def _tokens(text: str) -> tuple[set[str], set[str]]:
    return set(extract_phones(text)), {u.lower() for u in extract_usernames(text)}


def load(chat: str) -> tuple[set[str], set[str]]:
    phones: set[str] = set()
    users: set[str] = set()
    texts: list[str] = []
    try:
        r = requests.get(f"https://t.me/s/{chat}", timeout=30)
        if r.ok:
            soup = BeautifulSoup(r.text, "html.parser")
            texts += [m.get_text(" ") for m in soup.select(".tgme_widget_message_text")]
    except requests.RequestException as e:
        print(f"[blacklist] не удалось загрузить чат: {e}")
    if LOCAL.exists():
        texts.append(LOCAL.read_text(encoding="utf-8"))
    for t in texts:
        p, u = _tokens(t)
        phones |= p
        users |= u
    return phones, users


def is_blacklisted(l: Listing, phones: set[str], users: set[str]) -> bool:
    return bool(set(l.phones) & phones or {u.lower() for u in l.usernames} & users)
