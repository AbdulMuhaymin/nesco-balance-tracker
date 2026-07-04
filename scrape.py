from playwright.sync_api import sync_playwright
from pathlib import Path
from datetime import datetime, timezone
import csv

URL = "https://customer.nesco.gov.bd/pre/panel"
CONSUMER = "36003567"


def get_balance():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(URL, wait_until="networkidle")

        page.fill("#cust_no", CONSUMER)
        page.click("#recharge_hist_button")

        balance_label = page.locator(
            "label",
            has_text="অবশিষ্ট ব্যালেন্স"
        )

        timestamp = (
            balance_label
            .locator("span")
            .inner_text()
            .strip()
        )

        balance = (
            balance_label
            .locator(
                "xpath=following-sibling::div[1]//input"
            )
            .input_value()
            .strip()
        )

        browser.close()

    return timestamp, balance


timestamp, balance = get_balance()

checked_at = datetime.now(timezone.utc).isoformat()

csv_file = Path("balance.csv")

new_row = [
    checked_at,
    timestamp,
    balance,
]

last_row = None

if csv_file.exists():
    with csv_file.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as f:
        rows = list(csv.reader(f))

        if len(rows) > 1:
            last_row = rows[-1]

# Compare only timestamp + balance
if last_row and last_row[1:] == new_row[1:]:
    print("No change detected.")
else:
    new_file = not csv_file.exists()

    with csv_file.open(
        "a",
        newline="",
        encoding="utf-8",
    ) as f:

        writer = csv.writer(f)

        if new_file:
            writer.writerow([
                "Checked At (UTC)",
                "NESCO Timestamp",
                "Balance (Tk)",
            ])

        writer.writerow(new_row)

    print("New balance saved.")