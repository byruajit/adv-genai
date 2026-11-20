"""Session 6 checkpoint. Run from the adv-genai folder.

    uv run pytest tests/test_s06.py -k build1     one build at a time
    uv run pytest tests/test_s06.py               everything: 9 passed

The tests read YOUR file: mywork/head_office_client.py
They start their own copy of the head office, so you do not need it running.
"""
import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
MYWORK = ROOT / "mywork"
sys.path.insert(0, str(MYWORK))


def _load_head_office():
    spec = importlib.util.spec_from_file_location("head_office", ROOT / "tools" / "head_office.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def hq():
    server, base_url = _load_head_office().start(retry_after=1)
    server.base_url = base_url
    yield server
    server.shutdown()


@pytest.fixture(scope="module")
def cl():
    if not (MYWORK / "head_office_client.py").exists():
        pytest.fail("mywork/head_office_client.py not found. Copy starters/s06_head_office_client.py "
                    "to mywork/head_office_client.py first (README, Session 6, step 2).")
    import head_office_client
    return head_office_client


def run(fn, what):
    """Call fn. Turn the two beginner slips into a plain message."""
    try:
        return fn()
    except NameError as e:
        if "____" in str(e):
            pytest.fail(f"{what}: there is still a ____ blank to fill in.")
        raise


def must_refuse(fn, slip, why):
    try:
        run(fn, why)
    except slip:
        return
    except Exception as e:
        pytest.fail(f"{why}, so this should raise {slip.__name__}. "
                    f"It raised {type(e).__name__} instead: {e}")
    pytest.fail(f"{why}, so this should raise {slip.__name__}. Nothing was raised.")


# ---- Build 1 ---------------------------------------------------------------

def test_build1_parse_rate(cl):
    got = cl.parse_rate('{"from": "USD", "to": "INR", "rate": 84.5}')
    assert got is not None, "parse_rate returned None. Did you forget the word return?"
    assert not isinstance(got, (dict, str)), \
        f"parse_rate should give back only the rate (a number), but it gave {got!r}"
    assert got == pytest.approx(84.5)


def test_build1_to_json(cl):
    got = cl.to_json("Ravi", 1690000)
    assert got is not None, "to_json returned None. Did you forget the word return?"
    assert isinstance(got, str), f"to_json should give back TEXT (a str), but it gave a {type(got).__name__}"
    assert json.loads(got) == {"name": "Ravi", "amount": 1690000}, \
        f"to_json gave {got}, which is not the JSON for name Ravi and amount 1690000"


# ---- Build 2 ---------------------------------------------------------------

def test_build2_get_rate_returns_the_rate(cl, hq):
    got = run(lambda: cl.get_rate(hq.base_url, "demo-key", "USD", "INR"), "get_rate")
    assert got is not None, "get_rate returned None. Is the return line in place?"
    assert got == pytest.approx(84.5), f"1 USD is 84.5 INR at the head office, but get_rate gave {got!r}"


def test_build2_wrong_key_is_401(cl, hq):
    must_refuse(lambda: cl.get_rate(hq.base_url, "wrong-key", "USD", "INR"),
                cl.AuthError, "With a wrong key the head office answers 401")


def test_build2_unknown_currency_is_404(cl, hq):
    must_refuse(lambda: cl.get_rate(hq.base_url, "demo-key", "XYZ", "INR"),
                cl.UnknownCurrencyError, "There is no rate for XYZ, so the head office answers 404")


# ---- Build 3 ---------------------------------------------------------------

def test_build3_application_gets_an_id(cl, hq):
    got = cl.submit_application(hq.base_url, "demo-key", "Ravi", 1690000)
    assert got is not None, "submit_application returned None. Is the return line in place?"
    assert isinstance(got, str) and got.startswith("APP-"), \
        f"The head office answers with an id like APP-1001, but submit_application gave {got!r}"


def test_build3_bad_application_is_refused(cl, hq):
    must_refuse(lambda: cl.submit_application(hq.base_url, "demo-key", "Ravi", -5),
                cl.BadApplicationError, "An amount of -5 is refused by the head office with 400")


# ---- Build 4 ---------------------------------------------------------------

def test_build4_waits_and_tries_again(cl, hq):
    hq.busy_calls, hq.busy_times = 0, []
    got = cl.get_with_retry(f"{hq.base_url}/busy", "demo-key")
    assert got is not None, "get_with_retry returned None. Return response.json() when it works."
    assert got == {"status": "ok", "message": "head office is free now"}
    assert hq.busy_calls == 3, f"The head office is busy twice, then free: that is 3 calls, but you made {hq.busy_calls}"
    gaps = [b - a for a, b in zip(hq.busy_times, hq.busy_times[1:])]
    assert all(g >= 0.9 for g in gaps), \
        "Retry-After said wait 1 second, but you tried again straight away. Use time.sleep."


def test_build4_gives_up_after_its_tries(cl, hq):
    hq.busy_calls, hq.busy_times = 0, []
    must_refuse(lambda: cl.get_with_retry(f"{hq.base_url}/busy", "demo-key", tries=2),
                cl.TooBusyError, "With only 2 tries the head office is busy both times")
    assert hq.busy_calls == 2, f"tries=2 means 2 calls, but you made {hq.busy_calls}"
