from playwright.sync_api import sync_playwright

URL = "https://customer.nesco.gov.bd/pre/panel"
CONSUMER = "36003567"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto(URL, wait_until="networkidle")

    # Fill consumer number
    page.fill("#cust_no", CONSUMER)

    # Click Recharge History
    page.click("#recharge_hist_button")

    # Wait until the balance box appears
    page.wait_for_selector('input[disabled][value]')

    # Find the label containing "অবশিষ্ট ব্যালেন্স"
    balance_label = page.locator("label", has_text="অবশিষ্ট ব্যালেন্স")

    # Timestamp inside that label
    timestamp = balance_label.locator("span").inner_text().strip()

    # The input immediately following the label
    balance = (
        balance_label
        .locator("xpath=following-sibling::div[1]//input")
        .input_value()
        .strip()
    )

    print("Timestamp:", timestamp)
    print("Balance:", balance)

    input("Press Enter to close...")
    browser.close()