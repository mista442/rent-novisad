"""Перевод объявления на русский через Claude API. Без ключа возвращает пустую строку."""
from __future__ import annotations

from .config import env

PROMPT = (
    "Переведи это объявление об аренде квартиры (сербский/английский) на русский язык. "
    "Сохрани все числа, адреса, телефоны и условия точно. Названия районов и улиц оставь латиницей "
    "с русской транскрипцией в скобках при первом упоминании. Верни только перевод, без комментариев.\n\n"
)


def to_russian(text: str, cfg: dict) -> str:
    tcfg = cfg.get("translate", {})
    key = env("ANTHROPIC_API_KEY")
    if not tcfg.get("enabled") or not key:
        return ""
    try:
        import anthropic

        client = anthropic.Anthropic(api_key=key)
        msg = client.messages.create(
            model=tcfg.get("model", "claude-haiku-4-5-20251001"),
            max_tokens=1500,
            messages=[{"role": "user", "content": PROMPT + text}],
        )
        return "".join(b.text for b in msg.content if b.type == "text").strip()
    except Exception as e:  # перевод не должен ронять весь запуск
        print(f"[translate] ошибка: {e}")
        return ""
