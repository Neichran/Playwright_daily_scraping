# day1_resilient_scraper_pylance_dataclass.py
# ------------------------------------------------------------
# Pylance-friendly Playwright scraper with:
#   • explicit type hints (Page, Response)
#   • dataclass-based CLI args (no "unknown attribute" warnings)
#   • expect_response for network wait + wait_for_selector for DOM
#   • retry/backoff and clean logging
#
# Target: https://quotes.toscrape.com/js/
# Usage:
#   python day1_resilient_scraper_pylance_dataclass.py --headful
#   python day1_resilient_scraper_pylance_dataclass.py --max-retries 5 --timeout 8000
# ------------------------------------------------------------

from __future__ import annotations

import argparse
import sys
import time
from dataclasses import dataclass
from typing import List, Optional

from playwright.sync_api import (
    sync_playwright,
    TimeoutError as PlaywrightTimeoutError,
    Page,
    Response,
)


@dataclass
class CLIArgs:
    url: str
    max_retries: int
    timeout: int
    headful: bool


def parse_args(argv: Optional[List[str]] = None) -> CLIArgs:
    parser = argparse.ArgumentParser(description="Pylance-friendly resilient Playwright scraper (Day 1)")
    parser.add_argument("--url", type=str, default="https://quotes.toscrape.com/js/", help="Target URL to scrape.")
    parser.add_argument("--max-retries", type=int, default=3, help="Maximum number of retry attempts.")
    parser.add_argument("--timeout", type=int, default=5000, help="Timeout per attempt (milliseconds).")
    parser.add_argument("--headful", action="store_true", help="Run browser with UI (headful).")
    ns = parser.parse_args(argv)
    return CLIArgs(
        url=ns.url,
        max_retries=ns.max_retries,
        timeout=ns.timeout,
        headful=ns.headful,
    )


def wait_and_get_quotes(page: Page, timeout_ms: int = 5000) -> List[str]:
    """
    Wait for a dynamic DOM element and collect its text contents.
    - Page.wait_for_selector(...)
    - Locator.all_text_contents()
    """
    page.wait_for_selector("div.quote", timeout=timeout_ms)
    return page.locator("div.quote").all_text_contents()


def wait_for_main_doc_response(
    page: Page,
    target_url: str,
    timeout_ms: int = 5000,
    preview_len: int = 200,
) -> str:
    """
    Use page.expect_response(predicate) to capture the main document response (status 200).
    Return a short preview of the response body for quick inspection.
    """
    def predicate(resp: Response) -> bool:
        return (resp.url == target_url) and (resp.status == 200)

    with page.expect_response(predicate, timeout=timeout_ms) as resp_info:
        page.goto(target_url, timeout=timeout_ms)
    resp: Response = resp_info.value

    try:
        body = resp.text()
    except Exception as exc:
        return f"[!] Could not read response text (maybe binary). status={resp.status}, url={resp.url}, err={exc}"

    return body[:preview_len] if body else ""


def run(
    target_url: str,
    max_retries: int,
    per_try_timeout_ms: int,
    headless: bool,
) -> int:
    """
    Main routine with retry/backoff. All symbols are strongly typed so Pylance
    recognizes attributes and methods without warnings.
    """
    print(f"[i] Target URL: {target_url}")
    print(f"[i] Retries: {max_retries}, Timeout per try (ms): {per_try_timeout_ms}, Headless: {headless}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page: Page = browser.new_page()

        for attempt in range(1, max_retries + 1):
            try:
                print(f"\n[TRY {attempt}/{max_retries}] Waiting for document response (status=200)...")
                doc_preview = wait_for_main_doc_response(
                    page=page,
                    target_url=target_url,
                    timeout_ms=per_try_timeout_ms,
                    preview_len=200,
                )
                print("[i] Document response preview:")
                print(doc_preview if doc_preview else "[i] (empty body preview)")

                print("[i] Waiting for dynamic DOM element: div.quote ...")
                quotes: List[str] = wait_and_get_quotes(page, timeout_ms=per_try_timeout_ms)
                print(f"[✓] Collected {len(quotes)} quote blocks.")

                for i, q in enumerate(quotes[:3], 1):
                    trimmed = " ".join(q.split())
                    if len(trimmed) > 120:
                        trimmed = trimmed[:117] + "..."
                    print(f"   {i:02d}. {trimmed}")

                browser.close()
                return 0

            except PlaywrightTimeoutError as te:
                print(f"[!] TimeoutError: {te}. Retrying...")
            except Exception as e:
                print(f"[!] Unexpected error: {e}. Retrying...")

            time.sleep(min(2 * attempt, 6))

        print("\n[x] Failed after max retries. Please verify selectors, timeouts, or network conditions.")
        browser.close()
        return 1


if __name__ == "__main__":
    args = parse_args()
    exit_code = run(
        target_url=args.url,
        max_retries=args.max_retries,
        per_try_timeout_ms=args.timeout,
        headless=not args.headful,
    )
    sys.exit(exit_code)
