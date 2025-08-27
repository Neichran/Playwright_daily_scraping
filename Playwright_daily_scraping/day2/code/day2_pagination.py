# day2_pagination.py
# ------------------------------------------------------------
# Goal: Paginate through Books to Scrape listing pages and
#       collect (title, price) for each product.
# Keep it simple: open → loop pages → collect → print summary.
# ------------------------------------------------------------

from playwright.sync_api import sync_playwright, expect, Page

def scrape_listing_page(page: Page):
    """Return a list of dicts: [{'title': ..., 'price': ...}, ...] for the current page."""
    items = page.locator("article.product_pod")
    expect(items).to_have_count(20)  # Books to Scrape lists 20 items per page
    results = []

    count = items.count()
    for i in range(count):
        card = items.nth(i)
        # Title is in the <a> title attribute inside <h3>
        title = card.locator("h3 a").get_attribute("title")
        # Price is a visible text like "£51.77"
        price = card.locator(".price_color").inner_text()
        results.append({"title": title or "", "price": price})

    return results

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Go to page 1
        page.goto("http://books.toscrape.com/")
        expect(page).to_have_title("All products | Books to Scrape - Sandbox")

        all_books = []
        max_pages = 3  # keep the demo small; increase if you want
        current = 1

        while current <= max_pages:
            print(f"[i] Scraping page {current} ...")
            all_books += scrape_listing_page(page)

            # Find the "Next" link; if it exists, click it, else break
            next_link = page.locator(".next a")
            if next_link.count() > 0:
                next_link.click()
                current += 1
            else:
                break

        # Summary
        print(f"\n[✓] Collected {len(all_books)} books from {current} page(s).")
        for b in all_books[:5]:
            print(f" - {b['title']} | {b['price']}")

        browser.close()

if __name__ == "__main__":
    main()
