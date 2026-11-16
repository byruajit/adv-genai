# Advanced Agentic AI & AI Agents with Generative AI — course repository

This repository is the single source of truth for the course: every command shown in class is here, character for character. If a slide and this README disagree, the README wins.

**Rule for the whole course: every Python command starts with `uv run`.** Never plain `python`, never `conda`. Have Anaconda? Keep it — it is never used and never touched. See `(base)` in your prompt? Ignore it.

**Start every session with `git pull` in this folder.**

---

## Session 9a — set up your machine (Windows, PowerShell)

Already have Git, VS Code or Python? Keep them: run the version check only and skip the install line. Everyone runs steps 2 and 4–8.

| # | Step | Command |
|---|---|---|
| 1 | Git — verify; install only if missing, then **close and reopen the terminal** | `git --version` · `winget install --id Git.Git -e` |
| 2 | Clone this repo into Documents — never into `C:\WINDOWS\system32` | `cd ~\Documents` · `git clone https://github.com/byruajit/adv-genai.git` · `cd adv-genai` · `code .` |
| 3 | uv — one line, then **close and reopen the terminal** (have uv? `uv self update`) | `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"` then `uv self version` |
| 3b | Only if step 3 still says "not recognized" after reopening | `[Environment]::SetEnvironmentVariable('Path', $env:Path + ';' + $HOME + '\.local\bin', 'User')` → reopen |
| 4 | Python 3.12 via uv — everyone, even with Python or Anaconda installed | `uv python install 3.12` then `uv python list` |
| 5 | Install the pinned packages (VS Code terminal: Ctrl+`) | `uv sync` |
| 6 | Private config — paste **your own** Groq key as `API_KEY` (free: console.groq.com → API Keys → Create); do not touch `MODEL`; no quotes; no trailing space | `copy .env.example .env` · `notepad .env` |
| 7 | First LLM call — read the token line | `uv run python hello.py` |
| 8 | **Checkpoint** — show the lab assistant | `uv run pytest tests/test_setup.py` → `3 passed` |
| 9 | At home tonight | ollama.com → install → `ollama pull llama3.2:3b` (about 2 GB) |

Then open today's notebook: `uv run jupyter lab module01/s09a_first_call.ipynb` (it runs without a key; model cells print `skipped` until `.env` is right). Its own check: `uv run pytest tests/test_s09a.py` → `6 passed`.

### Mac / Linux differences
Step 1: `xcode-select --install` (Mac) or `sudo apt install git` (Ubuntu) · VS Code from code.visualstudio.com, then Command Palette → "Shell Command: Install code command in PATH" · Step 3: `curl -LsSf https://astral.sh/uv/install.sh | sh` · Step 6: `cp .env.example .env`. Everything else is identical.

### Switching to Ollama (rate limits, or private data)
In `.env`, put `#` in front of the three Groq lines and remove `#` from the three Ollama lines. No code changes. Switch back the same way.

---

## Session 9b — How LLMs work: tokens, cost, the context window, embeddings

| # | Step | Command |
|---|---|---|
| 1 | Get today's files (in the `adv-genai` folder, VS Code terminal) | `git pull` · `uv sync` |
| 2 | Optional, for the embeddings section (Ollama running) | `ollama pull nomic-embed-text` (about 270 MB) — without it the notebook uses the cached vectors in the repo |
| 3 | Pre-read (10 minutes) | `module01/reading_tokens.md` |
| 4 | Lab | `uv run jupyter lab module01/s09b_tokens.ipynb` |
| 5 | **Checkpoint** | `uv run pytest tests/test_s09b.py -rs` → `5 passed` (a skipped test is not a pass: `-rs` says why) |

The first time the notebook counts tokens, `tiktoken` downloads its dictionary file (about 3 MB) once; after that it works offline.

---

## Session 3 — Python essentials I: clean and mask a customer message

| # | Step | Command |
|---|---|---|
| 1 | Get today's files (in the `adv-genai` folder) | `git pull` |
| 2 | Copy the starter into your work repository | `copy starters\s03_clean_text.py mywork\clean_text.py` |
| 3 | Fill in the six function bodies in `mywork\clean_text.py` — Copilot off, names unchanged | `code mywork\clean_text.py` |
| 4 | **Checkpoint** (from the `adv-genai` folder) | `uv run pytest tests/test_s03.py` → `8 passed` |
| 5 | See it work, then save your work | `uv run python mywork\clean_text.py` · in `mywork`: `git add clean_text.py` · `git commit -m "Add text cleaning and masking"` · `git push` |

Mac / Linux: `cp starters/s03_clean_text.py mywork/clean_text.py`.

---

## Session 4 — Python essentials II: decide loan eligibility

| # | Step | Command |
|---|---|---|
| 1 | Get today's files (in the `adv-genai` folder) | `git pull` |
| 2 | Copy the starter into your work repository | `copy starters\s04_loan_rules.py mywork\loan_rules.py` |
| 3 | Fill in the five function bodies in `mywork\loan_rules.py` — Copilot off, names unchanged | `code mywork\loan_rules.py` |
| 4 | **Checkpoint** (from the `adv-genai` folder) | `uv run pytest tests/test_s04.py` → `8 passed` |
| 5 | See it work, then save your work | `uv run python mywork\loan_rules.py` · in `mywork`: `git add loan_rules.py` · `git commit -m "Add loan eligibility rules"` · `git push` |

Mac / Linux: `cp starters/s04_loan_rules.py mywork/loan_rules.py`.

---

## Git and your work repository (`mywork`)

You use two repositories, in two directions:

| Repository | Where | What you do there |
|---|---|---|
| **Course repository** (this one) | `Documents\adv-genai` | `git pull` at the start of every session. Never commit or push here. |
| **Your work repository** | `Documents\adv-genai\mywork` | Everything you build in class. `git add` → `git commit` → `git push` to **your own** GitHub. |

`mywork` sits inside this folder but is its own repository with its own history. This repository ignores it (`mywork/` is in `.gitignore`), so the two never mix.

**Set it up once** (Git identity first if this laptop has never committed: `git config --global user.name "Your Name"` and `git config --global user.email "you@example.com"`):

| # | Step | Command |
|---|---|---|
| 1 | On github.com create an **empty** repository (no README, no .gitignore), e.g. `adv-genai-work` | — |
| 2 | Create the folder and make it a repository | `cd ~\Documents\adv-genai` · `mkdir mywork` · `cd mywork` · `git init -b main` |
| 3 | First commit | create `notes.md` · `git add notes.md` · `git commit -m "Start my work repository"` |
| 4 | Link it to your GitHub repository and push | `git remote add origin https://github.com/<you>/adv-genai-work.git` · `git push -u origin main` |

The first push opens a browser window to sign in to GitHub once (Git Credential Manager). Already have `mywork` from an earlier session? Check with `git remote -v` inside it: if it lists your GitHub repository, you are done.

**Every session:** `git pull` in `adv-genai` · work inside `mywork` · end with `git add` → `git commit -m "..."` → `git push` inside `mywork`. Commands run from `mywork` still find the `.env` in `adv-genai`, because `load_dotenv()` searches parent folders; never create a second `.env` inside `mywork`.

**Secrets:** `.env` is in `.gitignore`, so `git add` ignores it. If a key ever reaches a commit it is public within minutes — revoke it in the Groq console and create a new one.

---

## Troubleshooting — the errors that cover almost everything

**`uv` is not recognized** — you did not reopen the terminal. Close every terminal (including VS Code's) and open again. Still failing → step 3b.

**401 invalid API key** — open `.env` (not `.env.example`). No quotes around the key, no trailing space, not the placeholder. If in doubt, create a new key in the Groq console and paste it again.

**Model not found (404)** — the pinned model was retired. Run `uv run python list_models.py` and tell the instructor; do not change `MODEL` on your own.

**429 rate limit** — the free tier was busy. Wait 30 seconds and run again; if it keeps happening, switch `.env` to Ollama.

**Ollama: model not found / connection refused** — not found → `ollama pull llama3.2:3b`. Connection refused → Ollama is not running: check the tray icon, or run `ollama serve` in a second terminal.

Also seen: a warning that `UV_NATIVE_TLS` is deprecated — harmless, ignore. `uv version` (no dashes) errors outside a project — use `uv self version`.

---

## Keys
You create your own free Groq key at console.groq.com. It lives in `.env` and nowhere else. If it ever appears in chat, code or a screenshot, revoke it in the console immediately and create a new one.

## Layout
```
hello.py                          Session 9a first call
list_models.py                    which models your key can use
tests/test_setup.py               Session 9a checkpoint (3 tests)
tests/test_s03.py                 Session 3 checkpoint: reads mywork/clean_text.py (8 tests)
starters/s03_clean_text.py        Session 3 starter: copy to mywork/clean_text.py
tests/test_s04.py                 Session 4 checkpoint: reads mywork/loan_rules.py (8 tests)
starters/s04_loan_rules.py        Session 4 starter: copy to mywork/loan_rules.py
tests/test_s09a.py                checks the Session 9a notebook (offline, 6 tests)
tests/test_s09b.py                Session 9b checkpoint (5 tests)
module01/s09a_first_call.ipynb    Session 9a notebook: hello.py rebuilt cell by cell
module01/terms_s09a.md            every new term from Session 9a, and where it comes back
module01/s09b_tokens.ipynb        Session 9b notebook: tokens, usage, cost, context window, embeddings
module01/tokens_utils.py          Session 9b helpers (count_tokens, cost_inr, wrapper_size, nearest ...)
module01/embeddings_10words.json  cached nomic-embed-text vectors for the ten words (no Ollama needed)
module01/reading_tokens.md        Session 9b pre-read
module01/terms_s09b.md            every new term from Session 9b, and where it comes back
cheatsheet/python-for-agents.md   the six Python patterns agents use
guides/Environment_Setup_Guide.docx  step-by-step setup guide with every fix (Session 9a)
mywork/                           your own work repository (ignored by this one; pushed to your GitHub)
.env.example                      copy to .env
pyproject.toml + uv.lock          pinned dependencies (uv sync)
```
Modules are added as the course progresses (`module01/ … module14/`).
