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

# Max time (seconds) to wait for a sleeping app to wake back up after
# clicking the wake-up button, before giving up and proceeding anyway.
WAKE_UP_TIMEOUT_SECONDS = 90

# Max time (seconds) to wait for actual Streamlit app content to appear
# on the page before falling back to the fixed WAIT_AFTER_LOAD_SECONDS wait.
CONTENT_READY_TIMEOUT_SECONDS = 60


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


def wait_for_wake_up(page, timeout_seconds=WAKE_UP_TIMEOUT_SECONDS):
    """
    If the Streamlit Community Cloud "Zzzz / app has gone to sleep" screen
    is showing, click the wake-up button and poll until that screen is gone
    (it's replaced by the real app, usually after a reload).
    """
    try:
        wake_btn = page.get_by_role("button", name="get this app back up", exact=False)
        try:
            wake_btn.first.wait_for(state="visible", timeout=8000)
        except Exception:
            return  # button never showed up -- not asleep, nothing to do

        print("App was asleep -- clicking wake-up button.")
        wake_btn.first.click()

        deadline = time.time() + timeout_seconds
        while time.time() < deadline:
            still_asleep = page.get_by_text("This app has gone to sleep", exact=False)
            if still_asleep.count() == 0:
                print("App woke up.")
                return
            time.sleep(2)

        print("Timed out waiting for wake-up; proceeding anyway.")
    except Exception as e:
        print(f"Wake-up check skipped due to: {e}")


def wait_for_content_ready(page, timeout_seconds=CONTENT_READY_TIMEOUT_SECONDS):
    """
    Wait for the actual Streamlit app container to be present and for the
    "Running..." status indicator (shown while the script is executing) to
    disappear, so the screenshot captures a fully rendered page.
    """
    try:
        page.wait_for_selector(
            '[data-testid="stAppViewContainer"]', timeout=timeout_seconds * 1000
        )
    except Exception as e:
        print(f"Content container not detected within timeout: {e}")
        return

    try:
        deadline = time.time() + timeout_seconds
        while time.time() < deadline:
            running = page.get_by_text("Running", exact=False)
            if running.count() == 0:
                return
            time.sleep(2)
        print("Timed out waiting for 'Running' indicator to clear.")
    except Exception as e:
        print(f"Running-indicator check skipped due to: {e}")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1600, "height": 1200})

        print(f"Opening {APP_URL} ...")
        page.goto(APP_URL, wait_until="domcontentloaded", timeout=60000)

        # Streamlit Community Cloud apps sometimes go to sleep and show a
        # "wake up" prompt if no one has visited in a while.
        wait_for_wake_up(page)

        print("Waiting for app content to be ready...")
        wait_for_content_ready(page)

        print(f"Waiting {WAIT_AFTER_LOAD_SECONDS}s for the app to finish rendering...")
        time.sleep(WAIT_AFTER_LOAD_SECONDS)

        img_bytes = page.screenshot(full_page=True)
        browser.close()

    send_photo(img_bytes, "Daily screenshot")


if __name__ == "__main__":
    main()
