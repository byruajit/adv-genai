"""Session 6 practice. Run from the adv-genai folder, one level at a time:

    uv run pytest tests/test_s06_practice.py -k easy

The tests read YOUR file: mywork/s06_practice.py
"""
import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
MYWORK = ROOT / "mywork"
sys.path.insert(0, str(MYWORK))


@pytest.fixture(scope="module")
def hq():
    spec = importlib.util.spec_from_file_location("head_office", ROOT / "tools" / "head_office.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    server, base_url = module.start()
    yield base_url
    server.shutdown()


@pytest.fixture(scope="module")
def pr():
    if not (MYWORK / "s06_practice.py").exists():
        pytest.fail("mywork/s06_practice.py not found. Copy starters/s06_practice.py "
                    "to mywork/s06_practice.py first.")
    import s06_practice
    return s06_practice


def test_easy_status_meaning(pr):
    for code, words in [(200, "ok"), (201, "created"), (400, "bad request"), (401, "not allowed"),
                        (404, "not found"), (429, "too busy"), (500, "server error")]:
        assert pr.status_meaning(code) == words, f"{code} should mean {words!r}"
    assert pr.status_meaning(418) == "unknown"


def test_medium_convert(pr, hq):
    assert pr.convert(hq, "demo-key", 100, "USD") == pytest.approx(8450.0)
    assert pr.convert(hq, "demo-key", 10, "EUR", to="INR") == pytest.approx(912.0)
    with pytest.raises(pr.UnknownCurrencyError):
        pr.convert(hq, "demo-key", 100, "XYZ")


def test_hard_all_branches(pr, hq):
    got = pr.all_branches(hq, "demo-key")
    assert got is not None, "all_branches returned None. Return the list after the loop."
    assert len(got) == 8, f"There are 8 branches on 3 pages, but you collected {len(got)}"
    assert got[0] == "Ameerpet" and got[-1] == "Kondapur"
