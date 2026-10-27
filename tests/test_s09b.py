"""Session 9b checkpoint. Run with:  uv run pytest tests/test_s09b.py -rs   (-rs prints why a test was skipped)"""
import json
import os
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "module01"))
from tokens_utils import (PRICE_CARDS, USD_TO_INR, WORDS, chat_client, cost_inr, count_tokens,  # noqa: E402
                          load_points, load_vectors, nearest, show_tokens)

NB_PATH = ROOT / "module01" / "s09b_tokens.ipynb"
ENGLISH = "Can I get a personal loan of 8 lakh rupees for five years?"
KEY = os.getenv("API_KEY", "")


def test_count_tokens_is_sensible():
    n = count_tokens(ENGLISH)
    assert 10 <= n <= 25, f"unexpected token count {n}"
    assert "".join(show_tokens(ENGLISH)) == ENGLISH, "the pieces must glue back to the text"


def test_cost_function():
    card = next(iter(PRICE_CARDS))
    p = PRICE_CARDS[card]
    usd = (1000 * p["input"] + 1000 * p["output"]) / 1_000_000
    assert cost_inr(1000, 1000, card) == round(usd * USD_TO_INR, 4)
    assert cost_inr(1000, 1000, card, calls=1000) == round(usd * USD_TO_INR * 1000, 4)


@pytest.mark.skipif(not KEY or "paste_your" in KEY, reason="no API key in .env")
def test_estimate_matches_model_usage():
    """The provider wraps every message in a chat template. Measure the wrapper with a tiny
    message, subtract it, and your tiktoken estimate should match what the model read."""
    client = chat_client()
    model = os.getenv("MODEL")

    def prompt_tokens(text):
        r = client.chat.completions.create(model=model, max_tokens=8, messages=[{"role": "user", "content": text}])
        return r.usage.prompt_tokens

    wrapper = prompt_tokens("hi") - count_tokens("hi")
    estimate = count_tokens(ENGLISH)
    actual = prompt_tokens(ENGLISH) - wrapper
    assert wrapper > 0, "expected a chat-template wrapper"
    assert abs(actual - estimate) <= max(3, int(0.10 * estimate)), f"estimate {estimate} vs usage-minus-wrapper {actual} (wrapper {wrapper})"


def test_embeddings_give_ten_points_and_loan_has_money_neighbours():
    try:
        pts, source = load_points()
        vecs, _ = load_vectors()
    except RuntimeError as e:
        pytest.skip(str(e))
    assert pts.shape == (len(WORDS), 2), source
    top = [w for w, _ in nearest("loan", WORDS, vecs, k=3)]
    assert set(top) & {"EMI", "interest", "credit score", "bank"}, f"loan's neighbours look wrong: {top}"


def test_notebook_is_valid_and_has_no_keys():
    nbformat = pytest.importorskip("nbformat")
    nb = nbformat.read(str(NB_PATH), as_version=4)
    nbformat.validate(nb)
    for i, c in enumerate(nb.cells):
        if c.cell_type == "code":
            compile(c.source, f"code cell {i}", "exec")
    assert not re.findall(r"gsk_[A-Za-z0-9]{20,}", NB_PATH.read_text(encoding="utf-8")), \
        "the notebook contains something that looks like a real key: remove it and revoke the key"
