from __future__ import annotations

from urllib.parse import quote


def whatsapp(phone: str, text: str) -> str:
    return f"https://wa.me/{phone}?text={quote(text)}"


def telegram_user(username: str) -> str:
    return f"https://t.me/{username}"


def telegram_phone(phone: str) -> str:
    return f"https://t.me/+{phone}"


def telegram_share(text: str) -> str:
    """Открывает выбор получателя с готовым текстом (запасной вариант без ника)."""
    return f"https://t.me/share/url?url=&text={quote(text)}"
