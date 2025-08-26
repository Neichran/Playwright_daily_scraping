# Playwright Daily Scraping

A day-by-day practice repository to learn **web scraping with Playwright (Python)**.  
**Day 1** covers waiting strategies (`wait_for_selector`, `expect_response`), basic error handling, retry/backoff, and daily journaling.

---

## 📁 Structure
```
Playwright_daily_scraping/
├─ README.md
├─ requirements.txt
└─ day1/
   ├─ code/
   └─ journal_day1.md
```

---

## 🚀 Quickstart

### 1) Install dependencies
```bash
pip install -r requirements.txt
python -m playwright install
```

### 2) Run examples
```bash
# Wait for a dynamic DOM element
python day1/code/day1_basic_wait.py

# Wait for a network response (page/context examples)
python day1/code/day1_wait_for_response.py
python day1/code/day1_capture_network_response.py

# Error handling scenarios
python day1/code/day1_error_handling.py

# Resilient scraper with retry/backoff
python day1/code/day1_resilient_scraper.py --headful --max-retries 4 --timeout 8000
```

---

## 🧩 Day 1 Goals
- Learn the difference between `wait_for_selector`, `expect_response`, and `wait_for_timeout`
- Handle errors (`TimeoutError`) gracefully
- Add simple retry/backoff
- Document progress in a short daily journal

---

## 🛠 Tips
- Always select the correct Python interpreter in VS Code where `playwright` is installed.
- Use type hints (`Page`, `Response`) to help Pylance understand methods and attributes.
- Prefer `page.expect_response(predicate)` in Python for race-free network waits.

---

## 📒 Journal
See `day1/journal_day1.md` for today’s notes.

---

## 🗺 Roadmap
- **Day 2**: Web-first assertions (`expect`), error screenshots/HTML dumps, pagination  
- **Day 3**: Export to CSV/JSON, pytest integration (`pytest-playwright`)  
- **Day 4**: Tracing/HAR capture, proxy & user-agent tweaks, CI setup

---

## 📄 License
MIT (or your choice)
