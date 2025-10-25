"""Initialize the wagon inventory database with a simple items table."""

from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).with_name("wagon.db")


def initialize_database() -> None:
    """Ensure the wagon database and items table exist."""
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
        connection.commit()
    print("Quartermaster: Wagon database initialized.")


if __name__ == "__main__":
    initialize_database()
