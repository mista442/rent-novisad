from pathlib import Path

from rent_novisad import blacklist, filters, links, messages
from rent_novisad.config import load
from rent_novisad.parsing import extract_phones, extract_price_eur
from rent_novisad.sources import telegram_public

CFG = load()
HTML = (Path(__file__).parent / "fixtures" / "tg_sample.html").read_text(encoding="utf-8")


def test_telegram_parse():
    a, b = telegram_public.parse(HTML, "novisad_stan")
    assert a.phones == ["381641234567"] and a.usernames == ["stan_owner"]
    assert a.price_eur == 350 and a.rooms == 1.0 and a.area_m2 == 38
    assert b.phones == ["38163111222"]


def test_filters():
    a, b = telegram_public.parse(HTML, "novisad_stan")
    assert filters.apply(a, CFG)[0]
    ok, why = filters.apply(b, CFG)
    assert not ok and any("Futog" in w or "agency_fee" in w for w in why)


def test_price_rsd():
    assert extract_price_eur("40.000 din", 100) == 400
    assert extract_price_eur("1.200 EUR") == 1200


def test_phones():
    assert extract_phones("zovite 06 4123 4567 ili 0641234567") == ["381641234567"]


def test_blacklist():
    a, _ = telegram_public.parse(HTML, "novisad_stan")
    assert blacklist.is_blacklisted(a, {"381641234567"}, set())
    assert blacklist.is_blacklisted(a, set(), {"stan_owner"})
    assert not blacklist.is_blacklisted(a, set(), set())


def test_messages_all_variants_langs():
    for v in messages.VARIANTS:
        for lang in messages.LANGS:
            t = messages.render(v, lang, CFG, " (350 €)")
            assert "{" not in t and CFG["applicant"]["name"] in t


def test_links():
    assert links.whatsapp("381641234567", "a b").endswith("?text=a%20b")
