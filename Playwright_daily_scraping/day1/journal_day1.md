# Journal — Day 1 (Playwright)

**Date:** August 26, 2025  
**Duration:** ~3 hours  
**Sites tested:** `google.com` (warm-up) and `https://quotes.toscrape.com/js/` (dynamic content).

---

## Key Learnings
- `wait_for_selector`: wait until a DOM element is available.
- `page.expect_response`: recommended way in Python to wait for a network response.
- `page.wait_for_timeout(ms)`: a blind sleep, useful for debugging only.
- Built a resilient scraper with `try/except`, retry logic, and backoff.

---

## Errors and Results
| Scenario              | Action/Code | Result     | Message/Note |
|-----------------------|-------------|-----------|--------------|
| Correct selector      | `wait_for_selector("div.quote")` | Success | Collected 10 quotes |
| Wrong selector        | `wait_for_selector("div.quotesss")` | Timeout | `TimeoutError` |
| Very short timeout    | `timeout=1000` | Timeout sometimes | Needs longer waits |
| Network response wait | `page.expect_response(lambda r: r.url==... and r.status==200)` | Success | Previewed response body |

---

## Outputs
- Scripts: `day1/code/`
- This daily journal

---

## Notes
- Pylance in VS Code required correct type hints (`Page`, `Response`) and the proper interpreter with `playwright` installed.
