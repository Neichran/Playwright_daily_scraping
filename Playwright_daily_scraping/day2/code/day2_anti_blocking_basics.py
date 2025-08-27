# day2_anti_blocking_basics.py
# ------------------------------------------------------------
# Goal: Show simple anti-blocking hygiene for Playwright scraping
#       AND save the collected data to a CSV file.
# Site: http://books.toscrape.com/
# ------------------------------------------------------------

import random
import time
import csv
from typing import List, Dict

from playwright.sync_api import sync_playwright, expect, Page

USER_AGENTS: List[str] = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
]

def human_delay(a: float = 1.2, b: float = 2.8) -> None:
    """Random short sleep to look less robotic."""
    time.sleep(random.uniform(a, b))

def save_debug(page: Page, prefix: str = "debug") -> None:
    """Capture screenshot + HTML to understand what the site served."""
    ts = time.strftime("%Y%m%d_%H%M%S")
    page.screenshot(path=f"{prefix}_screenshot_{ts}.png", full_page=True)
    with open(f"{prefix}_dump_{ts}.html", "w", encoding="utf-8") as f:
        f.write(page.content())
    print(f"[i] Saved debug artifacts with prefix '{prefix}'.")

def scrape_listing_page(page: Page) -> List[Dict[str, str]]:
    """Collect (title, price) items from the current listing page."""
    items = page.locator("article.product_pod")
    expect(items).to_have_count(20)
    results: List[Dict[str, str]] = []
    for i in range(items.count()):
        card = items.nth(i)
        title = card.locator("h3 a").get_attribute("title") or ""
        price = card.locator(".price_color").inner_text()
        results.append({"title": title, "price": price})
    return results

def save_to_csv(data: List[Dict[str, str]], filename: str = "books.csv") -> None:
    """Save a list of dicts to a simple CSV file."""
    if not data:
        print("[i] No data to save.")
        return
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "price"])
        writer.writeheader()
        writer.writerows(data)
    print(f"[✓] Saved {len(data)} rows to {filename}")

def main() -> None:
    ua = random.choice(USER_AGENTS)
    print(f"[i] Using UA: {ua}")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )

        context = browser.new_context(
            user_agent=ua,
            viewport={"width": 1280, "height": 800},
            locale="en-US",
            java_script_enabled=True,
            extra_http_headers={"Accept-Language": "en-US,en;q=0.9"},
        )

        context.add_init_script(
            """Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"""
        )

        page = context.new_page()
        try:
            page.goto("http://books.toscrape.com/", timeout=15000)
            expect(page).to_have_title("All products | Books to Scrape - Sandbox")
            human_delay()

            all_books: List[Dict[str, str]] = []
            max_pages = 3
            current = 1

            while current <= max_pages:
                print(f"[i] Scraping page {current}...")
                all_books.extend(scrape_listing_page(page))
                human_delay()

                next_link = page.locator(".next a")
                if next_link.count() > 0:
                    next_link.click()
                    human_delay(1.0, 2.0)
                    current += 1
                else:
                    break

            print(f"\n[✓] Collected {len(all_books)} books from {current} page(s).")
            for b in all_books[:5]:
                print(f" - {b['title']} | {b['price']}")

            # Save results to CSV
            save_to_csv(all_books, "books_day2.csv")

        except Exception as e:
            print(f"[!] Error: {e}")
            save_debug(page, prefix="anti_blocking")
        finally:
            context.close()
            browser.close()

if __name__ == "__main__":
    main()
