"""Generate a reproducible synthetic transaction export for the Budget Tracker."""

from __future__ import annotations

import csv
import random
from calendar import monthrange
from datetime import date
from pathlib import Path


SEED = 20261104
ROW_COUNT = 812
OUTPUT = Path(__file__).with_name("fake_data.csv")
HEADER = ["Data", "Gavėjas", "Paaiškinimai", "Suma", "D/K", "Įrašo Nr."]

EXPENSE_TEMPLATES = [
    ("Housing", "VISI IRANKIAI", "Buitinės priemonės ir smulkus remontas", 12, 95),
    ("Food", "MAXIMA", "PIRKINYS maisto produktai", 4, 68),
    ("Food", "LIDL", "PIRKINYS maisto produktai", 3, 54),
    ("Food", "IKI", "PIRKINYS maisto produktai", 3, 48),
    ("Food", "JAMMI", "Pietūs ir užkandžiai", 5, 28),
    ("Food", "NORIUPICOS", "Pica ir vakarienė", 8, 39),
    ("Food", "CANDY POP", "Saldumynai", 2, 12),
    ("Transport", "VIADA", "Degalai", 6, 82),
    ("Transport", "SKULAS", "Viešojo transporto bilietas", 1.5, 9),
    ("Transport", "SNABB", "Automobilio plovimas", 8, 24),
    ("Transport", "ORLEN", "Degalai", 7, 76),
    ("Healthcare", "EUROVAISTINE", "Vaistai ir sveikatos prekės", 6, 74),
    ("Healthcare", "FIELMANN", "Optikos prekės", 18, 145),
    ("Healthcare", "BOD LENSES", "Kontaktiniai lęšiai", 15, 58),
    ("Healthcare", "GYM", "Sporto klubo paslauga", 15, 42),
    ("Subscriptions", "APPLE.COM/BILL", "Mėnesinė skaitmeninės paslaugos prenumerata", 4, 18),
    ("Entertainment", "FORUM CINEMAS", "Kino bilietai", 12, 42),
    ("Entertainment", "APOLLO KINAS", "Kino bilietai", 10, 38),
    ("Entertainment", "BILIARDO KLUBAS", "Laisvalaikis ir biliardas", 12, 35),
    ("Clothing", "VINTED", "Drabužiai ir avalynė", 12, 85),
    ("Shared Account", "REVOLUT", "Pervedimas į bendrą sąskaitą", 25, 180),
    ("Investments", "DANIEL PETKEVI", "Investicija į Taupykle", 25, 300),
]

UNSUPPORTED_EXPENSES = {
    3: ("Travel", "Baltic Dream Travel", "Kelionės rezervacijos avansas", 45, 420),
    6: ("Gifts", "Dovana Fiktyvi", "Dovana šeimos šventei", 15, 120),
    9: ("Other", "Miesto Paslaugos", "Įvairios buities išlaidos", 4, 75),
    12: ("Gifts & Refunds", "Refund Service", "Pirkimo grąžinimo korekcija", 5, 65),
}

INCOME_TEMPLATES = [
    ("Salary", "OMNIVA LT UAB", "Atlyginimas už praėjusį mėnesį", 1500, 2450),
    ("Freelance", "Freelance Studio", "Fiktyvus projektinis atlygis", 50, 600),
    ("Gifts & Refunds", "GENADIJ PETKEVI", "Dovana ir sąskaitos papildymas", 20, 180),
    ("Investment Withdrawals", "Invest Platform", "Investicijų išmokėjimas", 50, 400),
    ("Other Income", "REVOLUT", "Pervedimas iš asmeninės piniginės", 15, 250),
]


def amount(rng: random.Random, low: float, high: float) -> str:
    cents = rng.randint(round(low * 100), round(high * 100))
    return f"{cents / 100:.2f}"


def transaction_date(rng: random.Random, month: int) -> date:
    return date(2026, month, rng.randint(1, monthrange(2026, month)[1]))


def build_rows() -> list[list[str]]:
    rng = random.Random(SEED)
    rows: list[list[str]] = []
    sequence = 1
    counts = [67] * 8 + [66] * 4
    rng.shuffle(counts)

    for month, monthly_count in enumerate(counts, start=1):
        income_count = 8 if month <= 4 else 9
        expense_count = monthly_count - income_count
        if month == 1:
            income_count += 1
            expense_count -= 1

        for index in range(monthly_count):
            is_income = index < income_count
            if is_income:
                if index == 0:
                    category, merchant, description, low, high = INCOME_TEMPLATES[0]
                elif index == 1 and month in (1, 4, 7, 10):
                    category, merchant, description, low, high = INCOME_TEMPLATES[1]
                elif index == 1 and month in (2, 5, 8, 11):
                    category, merchant, description, low, high = INCOME_TEMPLATES[3]
                else:
                    category, merchant, description, low, high = rng.choice(
                        [INCOME_TEMPLATES[2], INCOME_TEMPLATES[4]]
                    )
                direction = "K"
            else:
                if month in UNSUPPORTED_EXPENSES and index == income_count:
                    category, merchant, description, low, high = UNSUPPORTED_EXPENSES[month]
                else:
                    category, merchant, description, low, high = rng.choice(EXPENSE_TEMPLATES)
                direction = "D"

            if category == "Salary":
                transaction_day = min(27, monthrange(2026, month)[1])
                transaction_date_value = date(2026, month, transaction_day)
            else:
                transaction_date_value = transaction_date(rng, month)

            if category == "Travel" and month not in (6, 7, 8, 12):
                low, high = 20, 110
            if category == "Subscriptions":
                description = f"{description} {month:02d}"
            if category == "Food" and transaction_date_value.weekday() >= 5:
                description += " savaitgalio pirkinys"
            description += f" ({transaction_date_value.isoformat()})"

            transaction_id = f"26{month:02d}{transaction_date_value.day:02d}{sequence:010d}"
            rows.append([
                transaction_date_value.isoformat(),
                merchant,
                description,
                amount(rng, low, high),
                direction,
                transaction_id,
            ])
            sequence += 1

    for month in range(1, 13):
        transaction_date_value = transaction_date(rng, month)
        rows.append([
            transaction_date_value.isoformat(),
            "Baltic Dream Travel",
            f"Mėnesio kelionės rezervacijos išlaidos ({transaction_date_value.isoformat()})",
            amount(rng, 100, 500),
            "D",
            f"26{month:02d}{transaction_date_value.day:02d}{sequence:010d}",
        ])
        sequence += 1

    for index in rng.sample(range(ROW_COUNT - 12), 8):
        row = rows[index]
        row[1] = f"Unknown Merchant {index + 1:03d}"
        row[2] = f"Neatpažinta bandomoji operacija ({row[0]})"

    rng.shuffle(rows)
    return rows


def main() -> None:
    rows = build_rows()
    if len(rows) != ROW_COUNT:
        raise RuntimeError(f"Expected {ROW_COUNT} rows, generated {len(rows)}")

    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, delimiter=";", quoting=csv.QUOTE_ALL, lineterminator="\n")
        writer.writerow(HEADER)
        writer.writerows(rows)

    print(f"Wrote {len(rows)} transactions to {OUTPUT.name}")


if __name__ == "__main__":
    main()
