from __future__ import annotations

import argparse

from . import blacklist, docs_gen, filters, notify, store, translate
from .config import load
from .sources import manual, telegram_public


def collect(cfg: dict) -> list:
    rate = cfg["search"]["eur_to_rsd"]
    out = []
    for ch in cfg["sources"]["telegram_channels"]:
        try:
            out += telegram_public.fetch(ch, rate)
        except Exception as e:
            print(f"[source:{ch}] ошибка: {e}")
    out += manual.fetch(cfg["sources"]["manual_file"], rate)
    return out


def run(dry: bool) -> None:
    cfg = load()
    seen = store.load_ids()
    bl_phones, bl_users = blacklist.load(cfg["sources"]["blacklist_chat"])
    fresh, sent = [], 0
    for l in collect(cfg):
        if l.id in seen or any(f.id == l.id for f in fresh):
            continue
        if blacklist.is_blacklisted(l, bl_phones, bl_users):
            l.status = "blacklisted"
        else:
            ok, why = filters.apply(l, cfg)
            if not ok:
                l.status, l.notes = "filtered", why
            elif not (l.phones or l.usernames):
                l.notes.append("нет контакта — писать через ссылку объявления")
        if l.status == "new":
            l.translation_ru = translate.to_russian(l.text, cfg)
            if notify.send(l, cfg, cfg["cover_letter"]["default_variant"]) or dry:
                sent += 1
        fresh.append(l)
    if not dry:
        store.append(fresh)
    print(f"Новых: {len(fresh)}, на отправку вам: {sent}")


def cli() -> None:
    ap = argparse.ArgumentParser(prog="rent_novisad")
    sub = ap.add_subparsers(dest="cmd")
    r = sub.add_parser("run")
    r.add_argument("--dry-run", action="store_true", help="печатать, не писать в таблицу")
    sub.add_parser("docs", help="перегенерировать docs/COVER_LETTERS.md и CRITERIA.md")
    s = sub.add_parser("status", help="сменить статус: status <id> contacted|replied|rejected")
    s.add_argument("id")
    s.add_argument("value")
    a = ap.parse_args()
    if a.cmd == "docs":
        docs_gen.write()
    elif a.cmd == "status":
        print("ok" if store.set_status(a.id, a.value) else "не найдено/неверный статус")
    else:
        run(getattr(a, "dry_run", False))
