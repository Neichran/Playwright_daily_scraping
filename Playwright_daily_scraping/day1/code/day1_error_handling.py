# -------------------------------
# Day 1 - Part 2
# Goal: Test error handling in dynamic pages
#   1. Using a correct selector
#   2. Using a wrong selector
#   3. Using very short timeout
# -------------------------------

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

def main():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Open test site (JavaScript version)
        page.goto("https://quotes.toscrape.com/js/")

        # Case 1: correct selector
        try:
            page.wait_for_selector("div.quote", timeout=5000)
            print("OK: correct selector found (quotes).")
        except Exception as e:
            print("Error in case 1:", e)

        # Case 2: wrong selector
        try:
            page.wait_for_selector("div.quotesss", timeout=5000)
            print("Unexpected: wrong selector found.")
        except PlaywrightTimeoutError:
            print("Timeout: wrong selector not found.")
        except Exception as e:
            print("Other error in case 2:", e)

        # Case 3: very short timeout
        try:
            page.wait_for_selector("div.quote", timeout=1000)  # 1 second
            print("OK: quotes found in 1s.")
        except PlaywrightTimeoutError:
            print("Timeout: element did not load in 1s.")
        except Exception as e:
            print("Other error in case 3:", e)

        browser.close()

if __name__ == "__main__":
    main()
