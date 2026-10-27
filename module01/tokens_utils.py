"""Session 9b helpers — tokens, cost, embeddings. Imported by the notebook and the checkpoint test."""
from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
import tiktoken
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)   # .env wins over anything an editor put in the environment

# ---------------------------------------------------------------- tokenizer
# gpt-oss models use the o200k_harmony encoding, which tiktoken ships, so for the
# course model the count is exact. For other models (llama3.2 on Ollama) it is an
# estimate: the model's own usage field is the truth after you send.
ENCODING = "o200k_harmony"


def count_tokens(text: str, encoding: str = ENCODING) -> int:
    """How many tokens the text is, on this encoding."""
    return len(tiktoken.get_encoding(encoding).encode(text))


def show_tokens(text: str, encoding: str = ENCODING) -> list[str]:
    """The text split into the pieces the model sees."""
    enc = tiktoken.get_encoding(encoding)
    return [enc.decode([t]) for t in enc.encode(text)]


# ---------------------------------------------------------------- cost
# Price cards, USD per 1M tokens. The first is Groq's published price for gpt-oss-20b
# (checked Oct 2026); the other two are indicative tiers. Prices change: edit them.
PRICE_CARDS = {
    "groq gpt-oss-20b": {"input": 0.075, "output": 0.30},
    "frontier economy": {"input": 0.50, "output": 2.50},
    "frontier flagship": {"input": 5.00, "output": 25.00},
}
USD_TO_INR = 94.0            # approximate, Oct 2026


def cost_inr(prompt_tokens: int, completion_tokens: int, card: str, calls: int = 1) -> float:
    """Cost in rupees of `calls` calls with these token counts, on one price card."""
    p = PRICE_CARDS[card]
    usd = (prompt_tokens * p["input"] + completion_tokens * p["output"]) / 1_000_000
    return round(usd * USD_TO_INR * calls, 4)


# ---------------------------------------------------------------- clients
def chat_client() -> OpenAI:
    """The provider in .env (Groq by default)."""
    return OpenAI(base_url=os.getenv("BASE_URL"), api_key=os.getenv("API_KEY"))


def ollama_client() -> OpenAI:
    """Local Ollama. A provider is just a base URL."""
    return OpenAI(base_url="http://localhost:11434/v1", api_key="ollama", max_retries=0, timeout=60)


def usage_for(client: OpenAI, model: str, text: str) -> tuple[int, int]:
    """Send text as one user message; return (prompt_tokens, completion_tokens) as the model counted them."""
    r = client.chat.completions.create(model=model, max_tokens=16, messages=[{"role": "user", "content": text}])
    return r.usage.prompt_tokens, r.usage.completion_tokens


def wrapper_size(client: OpenAI, model: str) -> int:
    """The chat-template tokens the provider adds round one user message: usage('hi') minus count('hi')."""
    return usage_for(client, model, "hi")[0] - count_tokens("hi")


# ---------------------------------------------------------------- embeddings
WORDS = ["loan", "EMI", "interest", "credit score", "bank", "hospital", "doctor", "prescription", "cricket", "monsoon"]
CACHE = Path(__file__).with_name("embeddings_10words.json")
EMBED_MODEL = "nomic-embed-text"


def embed_via_ollama(words: list[str], model: str = EMBED_MODEL) -> np.ndarray:
    r = ollama_client().embeddings.create(model=model, input=words)
    return np.array([d.embedding for d in r.data], dtype=float)


def load_vectors(words: list[str] = WORDS) -> tuple[np.ndarray, str]:
    """The full vectors for the words: Ollama first, the cached file second. Returns (vectors, source)."""
    try:
        return embed_via_ollama(words), f"ollama:{EMBED_MODEL}"
    except Exception:
        if CACHE.exists():
            data = json.loads(CACHE.read_text())
            missing = [w for w in words if w not in data]
            if not missing:
                return np.array([data[w] for w in words], dtype=float), f"cache:{CACHE.name}"
        raise RuntimeError(
            "No embedding source. Start Ollama and run `ollama pull nomic-embed-text`, "
            "or `git pull` to get module01/embeddings_10words.json."
        )


def pca_2d(x: np.ndarray) -> np.ndarray:
    """Project N×D vectors to N×2 with plain NumPy (centre, SVD, keep two directions)."""
    xc = x - x.mean(axis=0)
    _, _, vt = np.linalg.svd(xc, full_matrices=False)
    return xc @ vt[:2].T


def load_points(words: list[str] = WORDS) -> tuple[np.ndarray, str]:
    """2-D points for the words (for the picture). Returns (points, source)."""
    vecs, source = load_vectors(words)
    return pca_2d(vecs), source


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    """1 = same direction, 0 = unrelated, -1 = opposite."""
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))


def nearest(word: str, words: list[str], vecs: np.ndarray, k: int = 3) -> list[tuple[str, float]]:
    """The k words whose vectors point most nearly the same way as `word`, using all dimensions."""
    i = words.index(word)
    scores = [(w, cosine(vecs[i], vecs[j])) for j, w in enumerate(words) if j != i]
    return sorted(scores, key=lambda s: s[1], reverse=True)[:k]


def write_cache(words: list[str] = WORDS) -> Path:
    """Instructor: run once with Ollama up to (re)create the fallback file."""
    vecs = embed_via_ollama(words)
    CACHE.write_text(json.dumps({w: v.tolist() for w, v in zip(words, vecs)}))
    return CACHE
