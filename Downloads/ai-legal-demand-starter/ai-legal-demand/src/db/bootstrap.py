from pathlib import Path
import sqlite3

SQLITE_PATH = Path("./data/db/legal_case_management.sqlite")
INIT_SQL = Path("./data/db/initial_sql.sql")

def bootstrap_db():
    SQLITE_PATH.parent.mkdir(parents=True, exist_ok=True)
    if SQLITE_PATH.exists():
        SQLITE_PATH.unlink()
    conn = sqlite3.connect(SQLITE_PATH)
    try:
        conn.executescript(INIT_SQL.read_text(encoding="utf-8"))
        conn.commit()
        print("✅ Database bootstrapped at", SQLITE_PATH)
    finally:
        conn.close()

if __name__ == "__main__":
    bootstrap_db()
