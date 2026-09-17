"""
Very simple version: open the Streamlit app, wait for it to load/compute,
take one full-page screenshot, and send it to Telegram.

Env vars required (set as GitHub Actions secrets):
  TELEGRAM_BOT_TOKEN
  TELEGRAM_CHAT_ID
"""

import os
import time
import requests
from playwright.sync_api import sync_playwright

APP_URL = "https://yfinextrememove-2ylefqmq9wk3h3rqrrbfoe.streamlit.app/"
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# How long to wait after the page loads for Streamlit to finish computing
# and rendering everything, before taking the screenshot. Increase this if
# your app takes longer to fully render.
WAIT_AFTER_LOAD_SECONDS = 45


def send_photo(image_bytes, caption):
    resp = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
        data={"chat_id": CHAT_ID, "caption": caption},
        files={"photo": ("screenshot.png", image_bytes, "image/png")},
        timeout=60,
    )
    if resp.status_code != 200:
        print(f"Telegram send failed: {resp.status_code} {resp.text}")
    else:
        print("Screenshot sent to Telegram.")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1600, "height": 1200})

        print(f"Opening {APP_URL} ...")
        page.goto(APP_URL, wait_until="domcontentloaded", timeout=60000)

        # Streamlit Community Cloud apps sometimes go to sleep and show a
        # "wake up" prompt if no one has visited in a while.
        try:
            wake_btn = page.get_by_text("get this app back up", exact=False)
            if wake_btn.count() > 0 and wake_btn.first.is_visible():
                print("App was asleep -- clicking wake-up button.")
                wake_btn.first.click()
        except Exception:
            pass

        print(f"Waiting {WAIT_AFTER_LOAD_SECONDS}s for the app to finish rendering...")
        time.sleep(WAIT_AFTER_LOAD_SECONDS)

        img_bytes = page.screenshot(full_page=True)
        browser.close()

    send_photo(img_bytes, "Daily screenshot")


if __name__ == "__main__":
    main()
