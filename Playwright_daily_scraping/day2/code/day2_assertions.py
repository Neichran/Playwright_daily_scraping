# day2_assertions_books_simple.py
# ---------------------------------------------
# Simple assertions on http://books.toscrape.com/.
# ---------------------------------------------

import re
from playwright.sync_api import sync_playwright, expect

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Go to the main listing page
        page.goto("http://books.toscrape.com/")

        # Basic page checks
        expect(page).to_have_title(re.compile(r"\bBooks to Scrape\b"))
        expect(page).to_have_url(re.compile(r"books\.toscrape\.com"))

        # ✅ Correct selector for product cards (article.product_pod)
        items = page.locator("article.product_pod")
        expect(items).to_have_count(20)  # 20 items per listing page

        # Sidebar categories exist (at least one visible)
        categories = page.locator("ul.nav-list li ul li")
        expect(categories.first).to_be_visible()

        # Check price format on the first few items (e.g., "£51.77")
        prices = page.locator("article.product_pod .price_color")
        for i in range(5):
            expect(prices.nth(i)).to_have_text(re.compile(r"^£\d+\.\d{2}$"))

        # Open the first product and assert details
        first_product = page.locator("article.product_pod h3 a").first
        first_product.click()

        expect(page.locator(".product_main h1")).to_be_visible()
        expect(page.locator(".product_main .price_color")).to_have_text(re.compile(r"^£\d+\.\d{2}$"))

        # Go back and paginate to page 2
        page.go_back()
        next_link = page.locator(".next a")
        expect(next_link).to_be_visible()
        next_link.click()

        # On page 2: still 20 items, and URL contains "page-2.html"
        expect(page).to_have_url(re.compile(r"page-2\.html"))
        expect(page.locator("article.product_pod")).to_have_count(20)

        print("✅ All assertions passed (books site).")
        browser.close()

if __name__ == "__main__":
    main()
