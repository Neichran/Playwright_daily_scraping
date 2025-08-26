# -------------------------------
# Day 1 - Part 3
# Goal: Capture specific network response (XHR/Fetch)
# -------------------------------

from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("Opening quotes site...")

        # Expect a response that contains "js" in the URL
        with page.expect_response(lambda r: "js" in r.url) as response_info:
            page.goto("https://quotes.toscrape.com/js/")

        response = response_info.value
        print("Response URL:", response.url)
        print("Status:", response.status)

        try:
            body = response.text()
            print("Response body (first 300 chars):")
            print(body[:300])
        except Exception as e:
            print("Error while reading response:", e)

        browser.close()

if __name__ == "__main__":
    main()
