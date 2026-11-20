"""Session 6: an LLM call with no SDK. Just HTTP and JSON.

The OpenAI client you have used since Session 2 does exactly this for you:
it POSTs JSON to BASE_URL + /chat/completions with your key in a header,
and reads the JSON that comes back.

Run it from the adv-genai folder (it reads BASE_URL, API_KEY and MODEL from .env):
    uv run python starters/s06_raw_llm_call.py
"""

import json
import os

import httpx
from dotenv import load_dotenv

load_dotenv(override=True)

url = os.getenv("BASE_URL").rstrip("/") + "/chat/completions"
headers = {"Authorization": f"Bearer {os.getenv('API_KEY')}"}
body = {
    "model": os.getenv("MODEL"),
    "messages": [{"role": "user", "content": "In one sentence: what is an EMI?"}],
}

print("POST", url)
print("JSON we send:")
print(json.dumps(body, indent=2))

response = httpx.post(url, json=body, headers=headers, timeout=60)
print("\nStatus code:", response.status_code)
response.raise_for_status()

data = response.json()
print("Top-level boxes in the reply:", list(data))
print("\nThe answer is at data['choices'][0]['message']['content']:")
print(data["choices"][0]["message"]["content"])
