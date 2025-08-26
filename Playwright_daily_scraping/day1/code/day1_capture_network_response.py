# -------------------------------
# Day 1 - Part 4
# Goal: Test network response handling
#   1. Open site
#   2. Wait for response
#   3. Print response details
#   4. Handle errors & timeout
# -------------------------------

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

def main():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        try:
            with context.new_page() as page:
                print("Opening quotes site...")
                page.goto("https://quotes.toscrape.com/js/")

                try:
                    print("Waiting for network response...")
                    response = context.wait_for_response(
                        lambda r: r.url == "https://quotes.toscrape.com/js/" and r.status == 200,
                        timeout=5000  # 5s timeout
                    )

                    # Print response details
                    print("✅ Response received:")
                    print("   URL:", response.url)
                    print("   Status:", response.status)

                    body_preview = response.text()[:300]
                    print("   Body preview (first 300 chars):")
                    print("   " + "-"*40)
                    print(body_preview)
                    print("   " + "-"*40)

                except PlaywrightTimeoutError:
                    print("⏳ Timeout: No matching response received in time.")
                except Exception as e:
                    print("⚠️ Error while waiting for response:", e)

        finally:
            browser.close()

if __name__ == "__main__":
    main()

