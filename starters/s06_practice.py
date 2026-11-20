"""Session 6 practice: three short exercises, easy to hard.

Check one at a time, from the adv-genai folder:
    uv run pytest tests/test_s06_practice.py -k easy
    uv run pytest tests/test_s06_practice.py -k medium
    uv run pytest tests/test_s06_practice.py -k hard
(The medium and hard tests start their own head office.)
"""

import httpx


def auth(key: str) -> dict[str, str]:
    """Written for you: the header every request carries."""
    return {"Authorization": f"Bearer {key}"}


# ---- EASY: read a status code ----------------------------------------------

def status_meaning(code: int) -> str:
    """Say in words what a status code means.

    200 -> "ok"            201 -> "created"       400 -> "bad request"
    401 -> "not allowed"   404 -> "not found"     429 -> "too busy"
    500 -> "server error"  anything else -> "unknown"
    """
    pass   # YOU: replace this line


# ---- MEDIUM: one GET, then some arithmetic ---------------------------------

class UnknownCurrencyError(Exception):
    """The head office has no rate for this pair."""


def convert(base_url: str, key: str, amount: float, frm: str, to: str = "INR") -> float:
    """Convert amount from frm to to, using the head office's rate. Round to 2 decimals.

    convert(url, "demo-key", 100, "USD")  -> 8450.0
    An unknown currency raises UnknownCurrencyError.
    """
    pass   # YOU: replace this line


# ---- HARD: follow the pages ------------------------------------------------

def all_branches(base_url: str, key: str) -> list[str]:
    """Collect every branch name. GET /branches?page=1, then page 2, and so on.

    Each reply looks like {"page": 1, "branches": [...], "next_page": 2}.
    On the last page next_page is null in JSON, which is None in Python.
    """
    pass   # YOU: replace this line
