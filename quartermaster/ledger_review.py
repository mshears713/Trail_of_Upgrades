"""Review the quartermaster ledger in chronological order."""

from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).with_name("wagon.db")


def review_ledger() -> None:
    """Print each ledger entry with calm, clerical pride."""
    print("Quartermaster: Ledger review commencing.")
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute(
            """
            SELECT id, timestamp, action, item, quantity_change, description
            FROM ledger
            ORDER BY timestamp, id
            """
        )
        rows = cursor.fetchall()
        if not rows:
            print("Quartermaster: Ledger is currently empty.")
        else:
            print(
                "Quartermaster: ID | Timestamp | Action | Item | Qty Change | Description"
            )
            for entry in rows:
                ident, timestamp, action, item, quantity_change, description = entry
                print(
                    "Quartermaster: "
                    f"{ident} | {timestamp} | {action} | {item} | {quantity_change:+d} | {description}"
                )
    print("Quartermaster: Ledger review complete. Records stand tall.")


if __name__ == "__main__":
    review_ledger()
