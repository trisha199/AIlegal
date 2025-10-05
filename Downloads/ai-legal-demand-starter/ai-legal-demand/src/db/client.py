from contextlib import contextmanager
import sqlite3
from typing import Any, Iterable

DB_PATH = "./data/db/legal_case_management.sqlite"

@contextmanager
def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def fetch_one(q: str, params: Iterable[Any] = ()):
    with db() as c:
        return c.execute(q, params).fetchone()

def fetch_all(q: str, params: Iterable[Any] = ()):
    with db() as c:
        return c.execute(q, params).fetchall()

def get_case_details(case_id: str):
    return fetch_one("SELECT * FROM cases WHERE case_id=?", (case_id,))

def get_parties(case_id: str, party_type: str | None = None):
    q, args = "SELECT * FROM parties WHERE case_id=?", [case_id]
    if party_type:
        q += " AND party_type=?"
        args.append(party_type)
    return fetch_all(q, args)

def get_financial_rollup(case_id: str):
    q = '''SELECT event_type, SUM(amount) AS total_amount, COUNT(*) AS event_count
           FROM case_events WHERE case_id=? AND amount IS NOT NULL
           GROUP BY event_type ORDER BY total_amount DESC'''
    return fetch_all(q, (case_id,))

def get_medical_total(case_id: str):
    q = '''SELECT SUM(amount) AS total_medical_expenses FROM case_events
           WHERE case_id=? AND event_type IN ('medical_treatment','expense')
           AND (description LIKE '%medical%' OR description LIKE '%therapy%' OR description LIKE '%prescription%')'''
    row = fetch_one(q, (case_id,))
    return row["total_medical_expenses"] or 0.0
