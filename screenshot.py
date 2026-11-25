"""
Very simple version: open the Streamlit app, wait for it to load/compute,
take one full-page screenshot, and send it to Telegram.

Env vars required (set as GitHub Actions secrets):
  TELEGRAM_BOT_TOKEN
  TELEGRAM_CHAT_ID
"""

import os
import sys
import time
import datetime
from zoneinfo import ZoneInfo
import requests
from playwright.sync_api import sync_playwright

APP_URL = "https://yfinextrememove-2ylefqmq9wk3h3rqrrbfoe.streamlit.app/"
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# Max time (seconds) to wait for the app to finish fetching and computing.
# The pre-/post-market scanners call several news APIs one after another, so a
# run with an empty cache can take a few minutes.
LOADING_TIMEOUT_SECONDS = 480

# The app must show no loading indicator for this long in a row before it counts
# as finished (there are short gaps between one spinner and the next).
QUIET_SECONDS = 15

# Max time (seconds) to wait for a sleeping app to wake up AND finish booting.
# A cold start on Streamlit Community Cloud ("Your app is in the oven") can
# take well over a minute, so this has to be generous.
APP_BOOT_TIMEOUT_SECONDS = 180

# Max time (seconds) to wait for actual Streamlit app content to appear once
# the app frame/container exists.
CONTENT_READY_TIMEOUT_SECONDS = 90

# Telegram send retries (network blips between the GitHub runner and
# api.telegram.org, e.g. "Connection reset by peer", are usually transient).
TELEGRAM_MAX_ATTEMPTS = 5

# On *.streamlit.app the real app is rendered inside this iframe, so
# selectors/text checks must look inside it, not on the outer page.
STREAMLIT_IFRAME = 'iframe[title="streamlitApp"]'
APP_CONTAINER = '[data-testid="stAppViewContainer"]'

# Anything visible here means the app is still working.
LOADING_SELECTORS = (
    '[data-testid="stStatusWidget"]',  # script is still running
    '[data-testid="stSpinner"]',       # st.spinner / cache_data spinners
    '[data-testid="stSkeleton"]',      # element placeholders
)
# Backup check: the app's own spinner messages. Use full phrases only -- single
# words like "Running" can appear in news headlines in the catalyst table.
LOADING_TEXTS = (
    "Scanning premarket movers",
    "Scanning post-market movers",
    "Fetching catalysts (",
    "Fetching post-market catalysts",
)

MARKET_TZ = ZoneInfo("America/New_York")


def log(msg):
    # flush=True keeps our prints in order with tracebacks in the Actions log
    print(msg, flush=True)


def _screenshot_caption():
    now_et = datetime.datetime.now(ZoneInfo("America/New_York"))
    start = now_et.replace(hour=8, minute=30, second=0, microsecond=0)
    end   = now_et.replace(hour=9, minute=30, second=0, microsecond=0)
    if now_et.weekday() < 5 and start <= now_et < end:
        return "pre-market"

    now_sg = datetime.datetime.now(ZoneInfo("Asia/Singapore"))
    start_sg = now_sg.replace(hour=6, minute=30, second=0, microsecond=0)
    end_sg   = now_sg.replace(hour=7, minute=30, second=0, microsecond=0)
    if 1 <= now_sg.weekday() <= 5 and start_sg <= now_sg < end_sg:
        return "post-market"
    return "Regular Trading Hour"


def is_market_open_now() -> bool:
    """True on NYSE trading hours (weekday 9:30am-4:00pm ET).
    Does NOT account for market holidays."""
    now_et = datetime.datetime.now(MARKET_TZ)
    if now_et.weekday() >= 5:
        return False
    open_t = now_et.replace(hour=9, minute=30, second=0, microsecond=0)
    close_t = now_et.replace(hour=16, minute=0, second=0, microsecond=0)
    return open_t <= now_et <= close_t


def send_photo(image_bytes, caption, max_attempts=TELEGRAM_MAX_ATTEMPTS) -> bool:
    """Send to Telegram with retry + backoff. Never raises; returns True on success."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    for attempt in range(1, max_attempts + 1):
        wait = min(5 * 2 ** (attempt - 1), 60)  # 5, 10, 20, 40, 60s
        try:
            resp = requests.post(
                url,
                data={"chat_id": CHAT_ID, "caption": caption},
                files={"photo": ("screenshot.png", image_bytes, "image/png")},
                timeout=(15, 60),  # (connect, read)
            )
            if resp.status_code == 200:
                log("Screenshot sent to Telegram.")
                return True
            if resp.status_code == 429:  # rate limited: honour retry_after
                try:
                    wait = int(resp.json()["parameters"]["retry_after"]) + 1
                except Exception:
                    pass
            elif 400 <= resp.status_code < 500:
                # Bad token / chat id / photo too big -- retrying won't help.
                log(f"Telegram rejected the request: {resp.status_code} {resp.text}")
                return False
            log(f"Attempt {attempt}/{max_attempts}: Telegram returned "
                f"{resp.status_code} {resp.text[:200]}")
        except requests.exceptions.RequestException as e:
            log(f"Attempt {attempt}/{max_attempts}: network error: {e}")

        if attempt < max_attempts:
            log(f"Retrying in {wait}s...")
            time.sleep(wait)

    log("Giving up sending to Telegram.")
    return False


def wait_for_app_scope(page, timeout_seconds=APP_BOOT_TIMEOUT_SECONDS):
    """Wake the app if it is asleep, then wait until the Streamlit app is
    actually mounted. Returns the scope to query (the iframe's frame_locator,
    or the page itself if the app is not wrapped in an iframe), or None if
    nothing showed up before the timeout.

    This is one polling loop on purpose. Previously the wake-up check returned
    as soon as the "gone to sleep" text vanished, but the app then spends a
    while booting ("Your app is in the oven") before the iframe exists. A
    short iframe wait followed by a silent fall-back to the top-level page
    meant we then looked for the app container on the outer page, where it
    never exists -- so we always timed out."""
    wake_btn = page.get_by_role("button", name="get this app back up", exact=False)
    deadline = time.time() + timeout_seconds
    last_click = 0.0
    last_state = None

    def note(state):
        nonlocal last_state
        if state != last_state:
            log(state)
            last_state = state

    while time.time() < deadline:
        try:
            if page.locator(STREAMLIT_IFRAME).count() > 0:
                note("Found Streamlit app iframe.")
                return page.frame_locator(STREAMLIT_IFRAME)
            if page.locator(APP_CONTAINER).count() > 0:
                note("Found Streamlit app container on the top-level page.")
                return page

            if wake_btn.count() > 0:
                # Re-click every 20s in case the first click didn't register.
                if time.time() - last_click > 20:
                    note("App is asleep -- clicking wake-up button.")
                    wake_btn.first.click()
                    last_click = time.time()
            else:
                note("Waiting for the app to boot...")
        except Exception as e:
            log(f"Boot check hiccup (will retry): {e}")
        time.sleep(2)

    log(f"App did not appear within {timeout_seconds}s.")
    return None


def wait_for_content_ready(scope, timeout_seconds=CONTENT_READY_TIMEOUT_SECONDS) -> bool:
    """Wait for the app container to appear."""
    try:
        scope.locator(APP_CONTAINER).first.wait_for(
            state="visible", timeout=timeout_seconds * 1000
        )
        return True
    except Exception as e:
        log(f"Content container not detected within timeout: {e}")
        return False


def find_loading_indicator(scope):
    """Describe the first visible sign that the app is still working, or None."""
    for selector in LOADING_SELECTORS:
        if scope.locator(selector).locator("visible=true").count() > 0:
            return selector
    for text in LOADING_TEXTS:
        if scope.get_by_text(text, exact=False).locator("visible=true").count() > 0:
            return f"text '{text}'"
    return None


def wait_until_loaded(scope, timeout_seconds=LOADING_TIMEOUT_SECONDS,
                      quiet_seconds=QUIET_SECONDS) -> bool:
    """Poll until nothing has been loading for `quiet_seconds` in a row.
    Returns False if that never happens within `timeout_seconds`."""
    start = time.time()
    quiet_since = None
    last_state = None

    while time.time() - start < timeout_seconds:
        try:
            busy = find_loading_indicator(scope)
        except Exception as e:
            busy = f"check failed, will retry ({e})"

        if busy is None:
            if quiet_since is None:
                quiet_since = time.time()
            if time.time() - quiet_since >= quiet_seconds:
                log(f"App finished loading after {time.time() - start:.0f}s.")
                return True
        else:
            quiet_since = None  # something started again -- restart the count
            if busy != last_state:
                log(f"[{time.time() - start:.0f}s] Still loading: {busy}")
        last_state = busy
        time.sleep(2)

    log(f"Still loading after {timeout_seconds}s (last seen: {last_state}).")
    return False


def save_debug(page, reason):
    """Keep a screenshot and a bit of page text so a failed run is diagnosable."""
    try:
        page.screenshot(path="debug_not_ready.png", full_page=True)
    except Exception as e:
        log(f"Could not save debug screenshot: {e}")
    try:
        text = page.inner_text("body")[:500].replace("\n", " | ")
        log(f"Page text at failure: {text}")
    except Exception:
        pass
    log(f"{reason} Saved debug_not_ready.png and exiting.")


def main():
    #if not is_market_open_now():
    #    log("Market closed right now (ET) — skipping.")
    #    return

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1600, "height": 1200})

        log(f"Opening {APP_URL} ...")
        page.goto(APP_URL, wait_until="domcontentloaded", timeout=60000)

        scope = wait_for_app_scope(page)
        if scope is None:
            save_debug(page, "App never finished booting.")
            browser.close()
            sys.exit(1)

        log("Waiting for app content to be ready...")
        if not wait_for_content_ready(scope):
            # App never rendered -- don't send a blank/loading screenshot.
            save_debug(page, "App content never appeared.")
            browser.close()
            sys.exit(1)

        log("Waiting for the app to finish fetching and rendering...")
        if not wait_until_loaded(scope):
            # Fail the job (red run) instead of skipping silently.
            save_debug(page, "App never finished loading.")
            browser.close()
            sys.exit(1)

        img_bytes = page.screenshot(full_page=True)
        with open("screenshot.png", "wb") as f:  # keep a copy for debugging
            f.write(img_bytes)
        browser.close()

    if not send_photo(img_bytes, _screenshot_caption()):
        sys.exit(1)  # fail the job only after all retries are exhausted


if __name__ == "__main__":
    main()
