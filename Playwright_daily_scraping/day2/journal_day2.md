# Journal — Day 2 (Playwright)

**Date:** August 28, 2025  
**Duration:** ~3 hours  
**Site used:** http://books.toscrape.com/

---

## Key Learnings

### 1. Assertions
- Used `expect(page).to_have_title("...")` and `expect(locator).to_have_count(20)` to check page correctness.
- Assertions are stronger than `wait_for_*` because they both **wait** and **validate**.
- Help catch site changes (e.g., if the number of products changes).

### 2. Screenshots on Error
- Learned `page.screenshot(path, full_page=True)` to capture page state.
- Learned `page.content()` to save raw HTML for debugging.
- Helpful when a selector fails or the site blocks scraping (shows you exactly what happened).

### 3. Pagination
- Practiced looping through multiple listing pages.
- Used `locator.count()`, `locator.nth(i)`, `.inner_text()`, and `.get_attribute()` to extract book titles and prices.
- Learned to click the `.next a` button until no longer available.

### 4. Anti-blocking Basics
- Rotated **User-Agents** (`user_agent` in `new_context`).
- Added `extra_http_headers` like `"Accept-Language"`.
- Added **random delays** (`time.sleep(random.uniform(...))`) to avoid robotic patterns.
- Used `--disable-blink-features=AutomationControlled` and masked `navigator.webdriver` to look less like a bot.
- Exported results to **CSV** using Python’s built-in `csv.DictWriter`.

---

## Errors & Fixes
- Wrong CSS selectors (`li.article.product_pod`) returned 0 elements → fixed with `article.product_pod`.
- Realized `expect(...).to_have_title()` only accepts **string/regex**, not lambdas.
- Assertion failures raise `AssertionError`, not `TimeoutError` → handled separately in error-catching logic.

---

## Outputs
- **Scripts:**  
  - `day2_assertions_books_simple.py`  
  - `day2_screenshot_on_error.py`  
  - `day2_pagination.py`  
  - `day2_anti_blocking_basics.py`  

- **Artifacts:**  
  - Screenshots + HTML dumps when errors triggered  
  - `books_day2.csv` containing scraped titles and prices  

---

## Reflection
- Assertions make scrapers safer and easier to debug.  
- Screenshots/HTML dumps are essential for diagnosing unexpected page behavior.  
- Pagination is straightforward with Playwright’s `locator` API.  
- Anti-blocking measures are simple hygiene steps — good enough for small-scale scraping, but real-world sites may require proxies, stealth plugins, or APIs.  

---

## Next Steps (Day 3 Plan)
- Export data to **JSON/CSV** more systematically.  
- Introduce **pytest-playwright** for quick testing.  
- Try capturing **traces** (`context.tracing.start/stop`) for debugging.  
- Explore **proxy usage** for scaling.
