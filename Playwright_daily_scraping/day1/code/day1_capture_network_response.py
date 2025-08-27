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
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        target = "https://quotes.toscrape.com/js/"
        print("Opening quotes site...")

        try:
            print("Waiting for network response (status=200)...")
            # Correct: use expect_response as a context manager
            with page.expect_response(lambda r: r.url == target and r.status == 200, timeout=5000) as resp_info:
                page.goto(target)

            response = resp_info.value  # this is a real Response
            print("✅ Response received:")
            print("   URL:", response.url)
            print("   Status:", response.status)

            try:
                body_preview = response.text()[:300]
                print("   Body preview (first 300 chars):")
                print("   " + "-"*40)
                print(body_preview)
                print("   " + "-"*40)
            except Exception as e:
                print("⚠️ Could not read response body:", e)

        except PlaywrightTimeoutError:
            print("⏳ Timeout: No matching response received in time.")
        except Exception as e:
            print("⚠️ Error while waiting for response:", e)
        finally:
            browser.close()

if __name__ == "__main__":
    main()
