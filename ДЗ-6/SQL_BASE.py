import sqlite3
from contextlib import closing
from pathlib import Path


DB_PATH = Path(__file__).resolve().with_name("subscriptions.db")


def save_subscription(
    *, name, email, start, last_day, tariff_name, months, total, accepted_terms
):
    with closing(sqlite3.connect(DB_PATH)) as connection, connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                tariff TEXT NOT NULL,
                duration_months INTEGER NOT NULL,
                total_rubles INTEGER NOT NULL,
                accepted_terms INTEGER NOT NULL
            )
        """)

        connection.execute("""
            INSERT INTO subscriptions (
                name, email, start_date, end_date, tariff,
                duration_months, total_rubles, accepted_terms
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name, email, start.isoformat(), last_day.isoformat(),
            tariff_name, months, total, int(accepted_terms)
        ))
