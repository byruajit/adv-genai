# Session 6 hints

Read one hint, close this file, and try again. Open the next hint only if you are still stuck after two minutes.

## Build 2 · get_rate (fill in the blanks)

**Hint 1 (the idea).** The first two blanks are status codes: numbers the head office stamps on every reply. Read the slip on the line below each blank: it tells you which code that `if` is waiting for. The last blank is the name of a box in the JSON reply.

**Hint 2 (in words).** "Not allowed, your key is wrong" is 401. "Not found" is 404. The reply looks like `{"from": "USD", "to": "INR", "rate": 84.5}`, and you want the number.

**Hint 3 (nearly code).** `== 401`, then `== 404`, then `data["rate"]`. The last blank needs the quotes, because a dict key is text.

## Build 3 · submit_application (put the lines in order)

**Hint 1 (the idea).** First send the request. Then read the stamp on the reply: if it says 400, refuse with our own slip. Then let httpx refuse any other bad stamp. Only then read the id.

**Hint 2 (in words).** `response = ...` must come first, because every other line uses `response`. The `raise BadApplicationError` line sits indented under the `if ... == 400:` line. `return` is last.

**Hint 3 (nearly code).** The order is: `response = httpx.post(...)`, `if response.status_code == 400:`, the `raise` indented under it, `response.raise_for_status()`, `return response.json()["id"]`.

## Build 4 · get_with_retry

**Hint 1 (the idea).** Knock on the door. If the answer is "busy, come back in 1 second", wait 1 second and knock again. Do this at most `tries` times. If it was never free, give up with our own slip.

**Hint 2 (in words).** Use a `for` loop that runs `tries` times. Inside it: send the GET. If the status code is NOT 429, check it with `raise_for_status()` and return the JSON. Otherwise read the `Retry-After` header, turn it into a number, and sleep that long. After the loop (it only gets there if every try was busy), raise `TooBusyError`.

**Hint 3 (nearly code).**

```python
for attempt in range(tries):
    response = httpx.get(url, headers=auth(key))
    if response.status_code != 429:
        response.raise_for_status()
        return response.json()
    wait = float(response.headers.get("Retry-After", 1))
    time.sleep(wait)
raise ...
```
