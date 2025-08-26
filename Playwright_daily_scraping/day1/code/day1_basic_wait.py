from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print(" Opening dynamic page...")
        page.goto("https://quotes.toscrape.com/js/")

        
        print("\n without waiting ... ")
        try:
            quotes = page.locator("div.quote").all_text_contents()
            print(f"Found {len(quotes)} quotes immediately.")
        except Exception as e:
            print("Error:", e)

        
        print("\n with waiting ... ")
        try:
            page.wait_for_selector("div.quote", timeout=10000)  
            quotes = page.locator("div.quote").all_text_contents()
            print(f"Found {len(quotes)} quotes after waiting.")
        except Exception as e:
            print("Timeout or error:", e)

        browser.close()

if __name__ == "__main__":
    main()
