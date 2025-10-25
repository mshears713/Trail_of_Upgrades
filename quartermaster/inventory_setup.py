"""Initialize the wagon inventory database with required tables."""

from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).with_name("wagon.db")


def initialize_database() -> None:
    """Ensure the wagon database has both items and ledger tables."""
    if DB_PATH.exists():
        print("Quartermaster: Existing wagon database found. No reinitialization needed.")
        return

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS items (
                item TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                description TEXT NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                action TEXT,
                item TEXT,
                quantity_change INTEGER,
                description TEXT
            )
            """
        )
        connection.commit()
    print("Quartermaster: Wagon database initialized from scratch.")


if __name__ == "__main__":
    initialize_database()
