"""Simple Quartermaster script that reads inventory and prints a report."""

import json
from pathlib import Path


def load_inventory(manifest_path: Path) -> list[dict]:
    """Return every item from the manifest file."""
    print("Quartermaster: Reading manifest...")
    with manifest_path.open("r", encoding="utf-8") as manifest_file:
        return json.load(manifest_file)


def print_report(items: list[dict]) -> None:
    """Show each item and finish with a simple summary."""
    for item in items:
        print(
            f"Quartermaster: Item: {item['item']} | Quantity: {item['quantity']} | Description: {item['description']}"
        )
    print(f"Quartermaster Report: {len(items)} items successfully cataloged.")


def main() -> None:
    """Run the full report for the inventory manifest."""
    manifest_path = Path(__file__).with_name("inventory.json")
    items = load_inventory(manifest_path)
    print_report(items)


if __name__ == "__main__":
    main()
