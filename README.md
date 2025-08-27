# Playwright Daily Scraping

A day-by-day practice repository to learn **web scraping with Playwright (Python)**.  
Starting with simple waits and error handling (Day 1), then expanding to assertions, debugging, pagination, and anti-blocking on Day 2.

---

##  Project Structure

```
Playwright_daily_scraping/
├─ README.md
├─ requirements.txt
├─ day1/
│  ├─ code/
│  └─ journal_day1.md
└─ day2/
   ├─ code/
   └─ journal_day2.md
```

---

## Quickstart

### 1) Install dependencies
```bash
pip install -r requirements.txt
python -m playwright install
```

### 2) Day 1 examples:
```bash
python day1/code/day1_basic_wait.py
python day1/code/day1_wait_for_response.py
python day1/code/day1_error_handling.py
python day1/code/day1_resilient_scraper.py --headful --max-retries 4 --timeout 8000
```

### 3) Day 2 examples:
```bash
python day2/code/day2_assertions_books_simple.py
python day2/code/day2_screenshot_on_error.py
python day2/code/day2_pagination.py
python day2/code/day2_anti_blocking_basics.py
```

---

## Learning Highlights

###  Day 1
- Navigate and wait for dynamic content (`wait_for_selector`, `expect_response`)
- Handle timeouts and errors with retry logic
- Start daily journals (Day 1 already documented)

###  Day 2
- Use `expect(...)` for **web-first assertions** (URL, title, counts, visibility)
- Capture **screenshots + HTML dumps** when things fail → faster debugging
- **Scrape multiple pages** via pagination (e.g., “Next” link loops)
- Add **anti-blocking basics**:
  - Rotate User-Agent
  - Set headers like `Accept-Language`
  - Add human-like delays
  - Mask `navigator.webdriver`
  - Export data to **CSV**

---

## Day 2 Outputs
- Assertions approach using Pythonic `expect`
- Screenshots/HTML captured on failure
- Book title + price scraped across multiple pages → exported to `books_day2.csv`
- Enhanced debugging and bot‑avoidance techniques

---

## Journals
- Day 1 journal: [day1/journal_day1.md](day1/journal_day1.md)  
- Day 2 journal: [day2/journal_day2.md](day2/journal_day2.md)

---

## Roadmap
- **Day 3**: JSON export, testing with `pytest-playwright`, pagination improvements  
- **Day 4**: Playwright tracing, HAR files, configurable proxies/robot fingerprinting  
- **Day 5+**: AI-assisted data interpretation and integration into business workflows (e.g., feed scraped results into a model or analysis pipeline)

---

## License
MIT License

---

## Topics
`python` • `playwright` • `web-scraping` • `automation` • `learning`
