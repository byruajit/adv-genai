# Pre-read for Session 9b — ten minutes

**What the model actually sees.** A language model never sees letters or words. It sees *tokens*: pieces of text, roughly three-quarters of an English word each, from a fixed dictionary called a *tokenizer*. The loan question "Can I get a personal loan of 8 lakh rupees for five years?" is 16 tokens; the same question in Telugu is 25, because the dictionary was built mostly from English and code.

**Why you care.** Three reasons, and they run through the whole course:
1. **Cost** — every provider charges per token, in and out, and output costs more. Your `hello.py` printed `prompt=96 completion=105 total=201`. That is the bill.
2. **The context window** — a model can only see a fixed number of tokens at once. Everything — your instructions, the conversation so far, retrieved documents, tool results — must fit. The model remembers nothing between calls: your code re-sends the whole conversation every turn.
3. **Speed** — the model produces one token at a time. More tokens out, more waiting.

**Tokenizers differ by model.** The tokenizer belongs to the model, not to the text. Our default model (`openai/gpt-oss-20b`) uses an encoding called `o200k_harmony`; Llama models use a different one. In class we count with `tiktoken` (exact for gpt-oss) and then check against the `usage` field the model returns — which is always a bit bigger, because the provider wraps your message in a *chat template*.

**Embeddings — the other thing a model can produce.** An *embedding model* does not answer; it turns text into a list of numbers (a *vector*) such that texts with similar meaning end up close together. That is the machinery behind semantic search and RAG (Modules 4 and 5). In class we embed ten banking and everyday words and draw them on a plane.

**Three questions to arrive with**
- If Telugu costs about one and a half times as many tokens as English, what does that mean for a bank whose customers write in Telugu?
- Your chatbot has a 30-turn conversation. What is in the context window at turn 30, and who pays for it?
- What can an embedding model *not* do?
