# Terms from Session 9b — what they are, and where they come back

Every new word introduced in Session 9b. The notebook (`s09b_tokens.ipynb`, Part A3) explains each one in full, with an analogy, an example and the term it is most often confused with.

| Term | What it is | Say it as | Comes back at |
|---|---|---|---|
| Provider | Where the model runs: a cloud service (Groq) or your own machine (Ollama). Set by `BASE_URL`. | A place. | S10 selection · S11 · S12 local · Module 13 cloud |
| Model | The trained weights that answer. Set by `MODEL`. | A brain. | Every session |
| Token | The unit a model reads and writes: a piece of text from a fixed dictionary; about ¾ of an English word. | Not a word — a dictionary entry. | Every cost line · S19 · S34 budget exit · S38 |
| Tokenizer | The dictionary and rules that cut text into tokens. Belongs to the model. | Different model, different cuts. | S19 · S38 |
| Encoding (`o200k_harmony`) / `tiktoken` | The name of one tokenizer dictionary / the library that counts with it on your laptop. | The dictionary's name / the counter. | Whenever you count before sending: S19, S38 |
| Token ID | The whole number that names one dictionary piece. The model receives these numbers, not text. | The brick's catalogue number. | S11 (logit bias, intuition) |
| `usage` | Returned after every call: `prompt_tokens`, `completion_tokens`, `total_tokens`. | The truth after you send. | Every lab · S53 cost tracking · S54 |
| Chat template (the wrapper) | Extra tokens the provider wraps round your messages (role markers, a default system message). Counted in `usage` and billed. | The envelope round your letter. | S19 · S38 · S53 |
| Input / output price | Separate prices per million tokens for what the model reads and what it writes; output is higher. | Two meters; the ride meter runs faster. | S10 · S53 · S54 |
| Context window | The most tokens a model can see in one call: system prompt, history, documents, tool results and the answer. | A desk of fixed size. | S19 memory windows · S30 · S34 · S38 |
| Stateless model | The model keeps nothing between calls; your code re-sends the history every turn. | No memory — only the desk. | S19 · S38 |
| Next-token prediction | How answers are produced: score every possible next token, pick one, add it, repeat. | One token at a time. | S11 temperature · S15 reasoning |
| Attention | How the model weighs which earlier tokens matter for the next one. | Underlining what matters. | Intuition only |
| Temperature | How much randomness in each pick; 0 = the most likely token every time. | The randomness dial. | S11 (the lab) · S34 agents at 0–0.3 |
| Reasoning model | A model that spends hidden tokens thinking before the visible answer; gpt-oss is one. | Thinks first; costs more. | S15 · S37 |
| Embedding (vector) | A list of numbers standing for a text's meaning; similar meanings point the same way. | Meaning as coordinates. | S24 · Modules 4–5 · S39 |
| Embedding model | A model whose output is a vector, not text. It never answers. | Text in, numbers out. | S24 · Module 5 |
| Cosine similarity | How closely two vectors point the same way: 1 = same direction, 0 = unrelated. | The angle between two arrows. | S24 · Module 4 |
| PCA | Flattens many dimensions to two so people can look. Pictures only. | For the picture, not the search. | S24 inspecting an index |
| Pre-training | Learning to predict the next token over a huge corpus. Produces a base model. | Reading the library. | S10 · S12 |
| Fine-tuning (instruction tuning) | Further training on instruction-and-answer pairs. Produces a chat model. | Learning to follow instructions. | Module 11 fine-tuning |
| Preference tuning (RLHF) | Nudging the model towards answers people preferred. | Learning manners. | S15 · responsible AI |
| Base model vs chat model | Pre-trained only vs fine-tuned to follow instructions. You call chat models. | Raw vs trained to talk. | S10 · S12 |
| Knowledge cutoff | The date the model stopped seeing training data; anything later must be in the context. | The library closed on a date. | S10 · Module 5 (why retrieval exists) |
| Open-weight vs frontier | Downloadable weights (Llama, Qwen, gpt-oss) vs vendor-API-only (GPT, Claude, Gemini). | Can you run it yourself? | S10 · S12 |
