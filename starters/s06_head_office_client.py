"""Session 6: head_office_client.py  (YOUR file)

Ravi wants a loan to study in the USA. To process it, our branch has to talk
to the bank's head office: ask for today's dollar rate, send the application,
and wait politely when the head office is busy.

    parse_rate, to_json    JSON: the form written as text, so it can travel
    get_rate               GET a rate; turn 401 and 404 into our own slips
    submit_application     POST the application as JSON; get back an id
    get_with_retry         on 429 (too busy), wait and try again

Start the head office first, in its own terminal:
    uv run python tools/head_office.py
Check one build at a time, from the adv-genai folder (you do NOT need the
head office running for the tests: they start their own):
    uv run pytest tests/test_s06.py -k build1
Stuck for two minutes? Read ONE hint in starters/s06_hints.md.
Then run this file:  uv run python mywork/head_office_client.py
"""

import json
import time

import httpx

BASE_URL = "http://127.0.0.1:8006"
KEY = "demo-key"


class AuthError(Exception):
    """401: the head office did not accept our key."""


class UnknownCurrencyError(Exception):
    """404: the head office has no rate for this pair of currencies."""


class BadApplicationError(Exception):
    """400: the head office could not accept the application as sent."""


class TooBusyError(Exception):
    """429 on every try: the head office stayed busy."""


def auth(key: str) -> dict[str, str]:
    """The header every request carries: who is asking. (Written for you.)"""
    return {"Authorization": f"Bearer {key}"}


def parse_rate(text: str) -> float:
    """Turn the head office's reply, which arrives as text, into the rate."""
    pass   # BUILD 1 (together): replace this line


def to_json(name: str, amount: float) -> str:
    """Turn an application into JSON text, ready to travel."""
    pass   # BUILD 1 (together): replace this line


def get_rate(base_url: str, key: str, frm: str, to: str) -> float:
    """Ask the head office for one exchange rate."""
    # BUILD 2 (fill in the blanks): replace each ____ . Change nothing else.
    response = httpx.get(f"{base_url}/rates", params={"from": frm, "to": to}, headers=auth(key))
    if response.status_code == ____:
        raise AuthError("the head office did not accept our key")
    if response.status_code == ____:
        raise UnknownCurrencyError(response.json()["error"])
    response.raise_for_status()
    data = response.json()
    return data[____]


def submit_application(base_url: str, key: str, name: str, amount: float) -> str:
    """Send an application. Returns the id the head office gives it."""
    # BUILD 3 (put the lines in order): every line you need is below, shuffled.
    # Type them under this comment in the right order, with the right indentation.
    #
    #     return response.json()["id"]
    #     raise BadApplicationError(response.json()["error"])
    #     response = httpx.post(f"{base_url}/applications", json={"name": name, "amount": amount}, headers=auth(key))
    #     response.raise_for_status()
    #     if response.status_code == 400:
    pass   # BUILD 3: replace this line


def get_with_retry(url: str, key: str, tries: int = 3) -> dict:
    """GET url. On 429, wait as long as Retry-After says, then try again."""
    pass   # BUILD 4 (on your own): replace this line. Stuck? Open starters/s06_hints.md


if __name__ == "__main__":
    rate = get_rate(BASE_URL, KEY, "USD", "INR")
    print("1 USD =", rate, "INR")
    print("Ravi needs 20,000 USD =", round(20000 * rate), "INR")
    app_id = submit_application(BASE_URL, KEY, "Ravi", round(20000 * rate))
    print("Application sent:", app_id)
    print(get_with_retry(f"{BASE_URL}/busy", KEY))
