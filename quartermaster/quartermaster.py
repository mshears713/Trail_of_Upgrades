"""Quartermaster script that records and reports wagon inventory using SQLite."""

import json
from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).with_name("wagon.db")
INVENTORY_PATH = Path(__file__).with_name("inventory.json")


def load_inventory() -> list[tuple[str, int, str]]:
    """Fetch the latest manifest from the JSON ledger."""
    print("Quartermaster: Consulting inventory.json for today's manifest.")
    with INVENTORY_PATH.open("r", encoding="utf-8") as manifest:
        items = json.load(manifest)
    return [
        (entry["item"], int(entry["quantity"]), entry["description"])
        for entry in items
    ]


def record_items(connection: sqlite3.Connection, items: list[tuple[str, int, str]]) -> None:
    """Clear previous entries and store the latest manifest."""
    print("Quartermaster: Tidying previous records for accuracy.")
    with connection:
        connection.execute("DELETE FROM items")
        for item, quantity, description in items:
            print(f"Quartermaster: Adding item '{item}'...")
            connection.execute(
                "INSERT INTO items (item, quantity, description) VALUES (?, ?, ?)",
                (item, quantity, description),
            )


def report_items(connection: sqlite3.Connection) -> None:
    """Display every item now stored in the wagon ledger."""
    print("Quartermaster: Current inventory:")
    cursor = connection.execute(
        "SELECT item, quantity, description FROM items ORDER BY ROWID"
    )
    for item, quantity, description in cursor.fetchall():
        print(f"Quartermaster: {item} | {quantity} | {description}")
    print("Quartermaster: Report complete. Ever ready to assist.")


def main() -> None:
    """Run the full inventory cycle."""
    print("Quartermaster: Opening the wagon ledger.")
    items = load_inventory()
    with sqlite3.connect(DB_PATH) as connection:
        record_items(connection, items)
        report_items(connection)


if __name__ == "__main__":
    main()
