from playwright.sync_api import sync_playwright
import csv
from pathlib import Path

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
            "label", has_text="অবশিষ্ট ব্যালেন্স"
        )

        timestamp = (
            balance_label
            .locator("span")
            .inner_text()
            .strip()
        )

        balance = (
            balance_label
            .locator("xpath=following-sibling::div[1]//input")
            .input_value()
            .strip()
        )

        browser.close()

        return timestamp, balance


timestamp, balance = get_balance()

print(timestamp)
print(balance)

csv_file = Path("balance.csv")

new_file = not csv_file.exists()

with csv_file.open("a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    if new_file:
        writer.writerow(["Timestamp", "Balance"])

    writer.writerow([timestamp, balance])

print("Saved to balance.csv")