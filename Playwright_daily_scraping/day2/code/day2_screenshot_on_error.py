# day2_screenshot_on_error.py
# ------------------------------------------------------------
# Goal: Save a screenshot and HTML dump when something goes wrong.
# Site: http://books.toscrape.com/
# Keep it simple: navigate → assert → intentionally fail → capture artifacts.
# ------------------------------------------------------------

from playwright.sync_api import sync_playwright, expect, Page, TimeoutError as PlaywrightTimeoutError

def save_debug(page: Page, prefix: str = "error"):
    """Save a full-page screenshot and the current HTML for debugging."""
    try:
        screenshot_path = f"{prefix}_screenshot.png"
        html_path = f"{prefix}_dump.html"
        page.screenshot(path=screenshot_path, full_page=True)
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(page.content())
        print(f"[i] Saved artifacts: {screenshot_path}, {html_path}")
    except Exception as e:
        print(f"[!] Failed to save debug artifacts: {e}")

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # 1) Go to the site
            page.goto("http://books.toscrape.com/")

            # 2) Basic assertions (should pass)
            expect(page).to_have_title("All products | Books to Scrape - Sandbox")
            items = page.locator("article.product_pod")
            expect(items).to_have_count(20)

            # 3) Intentional failure: look for a selector that does not exist
            #    (This triggers the error path so you can see screenshot/HTML dump.)
            print("[i] Intentionally checking a wrong selector to trigger the error path...")
            expect(page.locator(".this_selector_does_not_exist")).to_be_visible(timeout=3000)

            print("✅ All assertions passed (unexpected).")

        except PlaywrightTimeoutError as te:
            print(f"[!] TimeoutError: {te}")
            save_debug(page, prefix="timeout")
        except Exception as e:
            print(f"[!] Unexpected error: {e}")
            save_debug(page, prefix="unexpected")
        finally:
            browser.close()

if __name__ == "__main__":
    main()
