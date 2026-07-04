"""
jd_fetcher: gets raw job description text into state.

- If source_url is set, fetch + strip HTML to plain text.
- Else, fall back to raw_input (user-pasted text).
"""

from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from src.graph.state import JDState

# Sites often block requests with no/obvious-bot User-Agent
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )
}

_TIMEOUT_SECONDS = 10
_MIN_VALID_TEXT_LENGTH = 200  # below this, assume the page didn't render real content


class FetchError(Exception):
    """Raised when a JD URL can't be fetched or yields no usable content."""


def jd_fetcher(state: JDState) -> dict:
    source_url = state.get("source_url")
    raw_input = state.get("raw_input")

    if source_url:
        raw_text = _fetch_from_url(source_url)
    elif raw_input:
        raw_text = raw_input
    else:
        raise ValueError("Provide either source_url or raw_input")

    return {"raw_jd": raw_text}


def _fetch_from_url(url: str) -> str:
    _validate_url(url)

    try:
        response = requests.get(url, headers=_HEADERS, timeout=_TIMEOUT_SECONDS)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise FetchError(f"Timed out fetching {url}")
    except requests.exceptions.HTTPError as e:
        raise FetchError(f"HTTP error fetching {url}: {e}")
    except requests.exceptions.RequestException as e:
        raise FetchError(f"Failed to fetch {url}: {e}")

    text = _extract_text(response.text)

    if len(text) < _MIN_VALID_TEXT_LENGTH:
        # Likely a JS-rendered page (LinkedIn, many ATS platforms) where
        # requests.get() only returns an empty shell. Caller should fall
        # back to asking the user to paste the JD manually, or swap in
        # a headless-browser fetch (Playwright/Selenium) here later.
        raise FetchError(
            f"Fetched content from {url} was too short ({len(text)} chars) — "
            "the page is likely JS-rendered or blocked scraping. "
            "Try pasting the job description text directly instead."
        )

    return text


def _validate_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError(f"Invalid URL: {url}")


def _extract_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    # Strip elements that are never part of the actual JD content
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript", "svg"]):
        tag.decompose()

    text = soup.get_text(separator="\n")

    # Collapse excess blank lines/whitespace left behind by stripped tags
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    return "\n".join(lines)