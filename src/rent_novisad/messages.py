"""Сопроводительные сообщения арендодателю: 4 варианта × sr/en, плюс русский перевод для вас.

Отправляется только sr или en; ru — чтобы вы понимали, что именно отправляете.
"""
from __future__ import annotations

LANGS = ("sr", "en", "ru")

# --- Вопросы (ключ -> текст на каждом языке) ---
Q = {
    "free": {
        "sr": "Da li je stan još uvek slobodan i od kog datuma bi mogao da se useli ({date})?",
        "en": "Is the apartment still available, and from what date could I move in ({date})?",
        "ru": "Квартира ещё свободна, и с какой даты можно заехать ({date})?",
    },
    "lease": {
        "sr": "Da li se izdaje na duži rok (najmanje {months} meseci) i kolika je mesečna kirija?",
        "en": "Is it available for a long-term lease (at least {months} months), and what is the monthly rent?",
        "ru": "Сдаётся ли на длительный срок (минимум {months} мес.) и какая арендная плата в месяц?",
    },
    "utilities": {
        "sr": "Da li su komunalni troškovi (struja, grejanje, voda, infostan) uključeni u cenu ili se plaćaju posebno? Koliko to otprilike iznosi zimi?",
        "en": "Are utilities (electricity, heating, water, building fees) included in the rent or paid separately? Roughly how much are they in winter?",
        "ru": "Коммунальные платежи (свет, отопление, вода, взносы за дом) включены в цену или платятся отдельно? Сколько это примерно зимой?",
    },
    "deposit": {
        "sr": "Da li se traži depozit i u kom iznosu? Da li ugovor ide preko overe (potpisi kod javnog beležnika)?",
        "en": "Is a deposit required, and how much? Will the lease be a formal written contract?",
        "ru": "Нужен ли залог и в каком размере? Будет ли официальный письменный договор?",
    },
    "furnished": {
        "sr": "Da li je stan opremljen (nameštaj, šporet, frižider, veš mašina)? Da li sve radi ispravno?",
        "en": "Is the apartment furnished (furniture, stove, fridge, washing machine)? Is everything in working order?",
        "ru": "Квартира меблирована (мебель, плита, холодильник, стиральная машина)? Всё ли исправно работает?",
    },
    "internet": {
        "sr": "Da li postoji internet (optika/kabl) i klima uređaj?",
        "en": "Is there internet (fibre/cable) and air conditioning?",
        "ru": "Есть ли интернет (оптика/кабель) и кондиционер?",
    },
    "heating": {
        "sr": "Kakvo je grejanje (daljinsko, etažno, na struju)?",
        "en": "What kind of heating is there (district, individual gas, electric)?",
        "ru": "Какое отопление (центральное, индивидуальное газовое, электрическое)?",
    },
    "registration": {
        "sr": "Da li je moguća prijava boravka na toj adresi? (potrebno mi je za boravišnu dozvolu)",
        "en": "Is it possible to register my residence at this address? (I need it for my residence permit)",
        "ru": "Возможна ли регистрация проживания по этому адресу? (она нужна мне для вида на жительство)",
    },
    "pensioner": {
        "sr": "Da li izdajete penzionerima? Ja sam penzioner, miran stanar.",
        "en": "Do you rent to retirees? I am a retiree and a quiet tenant.",
        "ru": "Сдаёте ли вы пенсионерам? Я пенсионер, спокойный жилец.",
    },
    "viewing": {
        "sr": "Kada bih mogao da razgledam stan?",
        "en": "When could I view the apartment?",
        "ru": "Когда можно приехать посмотреть квартиру?",
    },
    "pets_floor": {
        "sr": "Na kom je spratu stan i da li zgrada ima lift?",
        "en": "What floor is it on, and does the building have a lift?",
        "ru": "На каком этаже квартира и есть ли в доме лифт?",
    },
}

# --- Варианты: приветствие, набор вопросов, завершение ---
VARIANTS = {
    "formal": {
        "title_ru": "Официальный",
        "hello": {"sr": "Poštovani,", "en": "Dear Sir or Madam,", "ru": "Здравствуйте,"},
        "intro": {
            "sr": "Zovem se {name} i zanima me Vaš oglas za izdavanje stana{ref}. Tražim stan za dugoročan najam u Novom Sadu.",
            "en": "My name is {name} and I am interested in your advertisement for the apartment{ref}. I am looking for a long-term rental in Novi Sad.",
            "ru": "Меня зовут {name}, меня заинтересовало ваше объявление об аренде квартиры{ref}. Я ищу жильё в Нови-Саде на длительный срок.",
        },
        "lead": {"sr": "Bio bih Vam zahvalan na odgovorima na sledeća pitanja:", "en": "I would be grateful if you could answer the following questions:", "ru": "Буду признателен за ответы на следующие вопросы:"},
        "questions": ["free", "lease", "utilities", "deposit", "furnished", "internet", "registration", "pensioner", "viewing"],
        "bye": {"sr": "Unapred hvala na odgovoru.\nSrdačan pozdrav,\n{name}", "en": "Thank you in advance for your reply.\nKind regards,\n{name}", "ru": "Заранее благодарю за ответ.\nС уважением,\n{name}"},
    },
    "friendly": {
        "title_ru": "Дружелюбный",
        "hello": {"sr": "Zdravo!", "en": "Hello!", "ru": "Здравствуйте!"},
        "intro": {
            "sr": "Ja sam {name}. Video sam Vaš oglas za stan{ref} i veoma me zanima. Dolazim u Novi Sad i tražim stan za duži boravak.",
            "en": "I'm {name}. I saw your listing for the apartment{ref} and I'm very interested. I'm moving to Novi Sad and looking for a place to stay long-term.",
            "ru": "Я {name}. Увидел ваше объявление о квартире{ref}, оно мне очень интересно. Я переезжаю в Нови-Сад и ищу жильё надолго.",
        },
        "lead": {"sr": "Može li nekoliko pitanja:", "en": "A few quick questions:", "ru": "Несколько быстрых вопросов:"},
        "questions": ["free", "lease", "utilities", "furnished", "internet", "registration", "pensioner", "viewing"],
        "bye": {"sr": "Hvala Vam puno i unapred se izvinjavam na pitanjima!\n{name}", "en": "Thank you very much, and sorry for all the questions!\n{name}", "ru": "Большое спасибо и извините за столько вопросов!\n{name}"},
    },
    "short": {
        "title_ru": "Короткий",
        "hello": {"sr": "Dobar dan,", "en": "Hello,", "ru": "Добрый день,"},
        "intro": {
            "sr": "interesuje me stan iz oglasa{ref}, za dugoročan najam od {date}.",
            "en": "I'm interested in the apartment from your listing{ref}, for a long-term rental from {date}.",
            "ru": "меня интересует квартира из объявления{ref}, долгосрочная аренда с {date}.",
        },
        "lead": {"sr": "Molim kratak odgovor:", "en": "Could you briefly tell me:", "ru": "Подскажите, пожалуйста:"},
        "questions": ["free", "lease", "utilities", "internet", "pensioner"],
        "bye": {"sr": "Hvala, {name}", "en": "Thanks, {name}", "ru": "Спасибо, {name}"},
    },
    "detailed": {
        "title_ru": "Подробный",
        "hello": {"sr": "Dobar dan,", "en": "Good day,", "ru": "Добрый день,"},
        "intro": {
            "sr": "Zovem se {name}. Zainteresovan sam za stan iz Vašeg oglasa{ref}. {about} Tražim stan za dugoročan najam u Novom Sadu, useljenje od {date}.",
            "en": "My name is {name}. I'm interested in the apartment from your listing{ref}. {about} I'm looking for a long-term rental in Novi Sad, moving in from {date}.",
            "ru": "Меня зовут {name}. Меня интересует квартира из вашего объявления{ref}. {about} Ищу долгосрочную аренду в Нови-Саде, заезд с {date}.",
        },
        "lead": {"sr": "Molim Vas da mi odgovorite na sledeće:", "en": "Could you please let me know:", "ru": "Пожалуйста, сообщите:"},
        "questions": ["free", "lease", "utilities", "deposit", "furnished", "internet", "heating", "pets_floor", "registration", "pensioner", "viewing"],
        "bye": {"sr": "Slobodno me kontaktirajte putem ove poruke. Hvala na vremenu!\nSrdačan pozdrav,\n{name}", "en": "Feel free to reply to this message. Thank you for your time!\nKind regards,\n{name}", "ru": "Можно ответить прямо на это сообщение. Спасибо за уделённое время!\nС уважением,\n{name}"},
    },
}


def render(variant: str, lang: str, cfg: dict, ref: str = "") -> str:
    """Собирает сообщение. ref — например ' (Grbavica, 350 €)'; пусто, если неизвестно."""
    v = VARIANTS[variant]
    a = cfg["applicant"]
    fmt = {
        "name": a["name"],
        "ref": ref,
        "date": a["move_in_from"],
        "months": a["lease_months"],
        "about": a.get(f"about_{lang}", "") if a.get("is_pensioner") else "",
    }
    qs = [k for k in v["questions"] if k != "pensioner" or a.get("is_pensioner")]
    lines = [f"{i}. {Q[k][lang].format(**fmt)}" for i, k in enumerate(qs, 1)]
    parts = [v["hello"][lang], v["intro"][lang].format(**fmt).replace("  ", " ").strip(), "", v["lead"][lang], *lines, "", v["bye"][lang].format(**fmt)]
    return "\n".join(parts)
