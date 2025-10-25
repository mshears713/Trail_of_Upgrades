"""Quartermaster script that records, reconciles, and reports wagon inventory."""

from datetime import datetime
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


def current_inventory(connection: sqlite3.Connection) -> dict[str, tuple[int, str]]:
    """Read the existing inventory from the database."""
    cursor = connection.execute(
        "SELECT item, quantity, description FROM items"
    )
    return {item: (quantity, description) for item, quantity, description in cursor.fetchall()}


def log_ledger(
    connection: sqlite3.Connection,
    action: str,
    item: str,
    quantity_change: int,
    description: str,
) -> None:
    """Store a single ledger entry for the performed action."""
    timestamp = datetime.now().isoformat(timespec="seconds")
    connection.execute(
        """
        INSERT INTO ledger (timestamp, action, item, quantity_change, description)
        VALUES (?, ?, ?, ?, ?)
        """,
        (timestamp, action, item, quantity_change, description),
    )


def reconcile_inventory(
    connection: sqlite3.Connection, new_items: list[tuple[str, int, str]]
) -> None:
    """Apply additions, removals, and updates while logging each change."""
    print("Quartermaster: Reconciling records with the latest manifest.")
    existing = current_inventory(connection)
    latest = {item: (quantity, description) for item, quantity, description in new_items}

    with connection:
        for item, (quantity, description) in existing.items():
            if item not in latest:
                connection.execute("DELETE FROM items WHERE item = ?", (item,))
                log_ledger(connection, "remove", item, -quantity, "Removed from service.")
                print(
                    f"Quartermaster: Removed '{item}' (qty -{quantity}) — recorded in ledger."
                )

        for item, (quantity, description) in latest.items():
            if item not in existing:
                connection.execute(
                    "INSERT INTO items (item, quantity, description) VALUES (?, ?, ?)",
                    (item, quantity, description),
                )
                log_ledger(connection, "add", item, quantity, "New supply secured.")
                print(
                    f"Quartermaster: Added '{item}' (qty +{quantity}) — recorded in ledger."
                )
            else:
                old_quantity, old_description = existing[item]
                quantity_changed = quantity != old_quantity
                description_changed = description != old_description
                if quantity_changed or description_changed:
                    connection.execute(
                        "UPDATE items SET quantity = ?, description = ? WHERE item = ?",
                        (quantity, description, item),
                    )
                    change = quantity - old_quantity
                    details = []
                    if quantity_changed:
                        details.append(f"Quantity {old_quantity}->{quantity}")
                    if description_changed:
                        details.append("Description refreshed")
                    note = "; ".join(details) or "Details updated."
                    log_ledger(connection, "update", item, change, note)
                    print(
                        f"Quartermaster: Updated '{item}' (qty {change:+d}) — recorded in ledger."
                    )

    print("Quartermaster: Reconciliation complete.")


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
        reconcile_inventory(connection, items)
        report_items(connection)


if __name__ == "__main__":
    main()
