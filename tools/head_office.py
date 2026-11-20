"""Head Office API: a small practice server for Session 6.

It plays the bank's head office. Your code sends it requests over HTTP and
reads its JSON replies, exactly as it would with a real API.

Start it (and leave this terminal open):
    uv run python tools/head_office.py

Then open http://127.0.0.1:8006 in a browser to see what it offers.
Every endpoint except / needs this header:   Authorization: Bearer demo-key
"""

import json
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

KEY = "demo-key"
PORT = 8006

# Practice numbers only: these are not today's real exchange rates.
RATES = {
    ("USD", "INR"): 84.5,
    ("EUR", "INR"): 91.2,
    ("GBP", "INR"): 107.3,
    ("AED", "INR"): 23.0,
    ("SGD", "INR"): 63.4,
}

BRANCHES = [
    "Ameerpet", "Banjara Hills", "Gachibowli", "Kukatpally",
    "Madhapur", "Secunderabad", "Begumpet", "Kondapur",
]
PAGE_SIZE = 3


class HeadOffice(BaseHTTPRequestHandler):
    server_version = "HeadOffice/1.0"

    # ---- helpers -------------------------------------------------------
    def reply(self, status, body, headers=None):
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        for name, value in (headers or {}).items():
            self.send_header(name, value)
        self.end_headers()
        self.wfile.write(data)

    def allowed(self):
        if self.headers.get("Authorization") == f"Bearer {KEY}":
            return True
        self.reply(401, {"error": "missing or wrong API key"})
        return False

    def log_message(self, fmt, *args):
        if not getattr(self.server, "quiet", False):
            sys.stderr.write(f"  {self.command} {self.path}  ->  {args[1] if len(args) > 1 else ''}\n")

    # ---- GET -----------------------------------------------------------
    def do_GET(self):
        url = urlparse(self.path)
        query = {k: v[0] for k, v in parse_qs(url.query).items()}

        if url.path == "/":
            return self.reply(200, {
                "service": "Head Office API (practice)",
                "needs_header": "Authorization: Bearer demo-key",
                "endpoints": [
                    "GET  /rates?from=USD&to=INR",
                    "POST /applications   JSON body: {\"name\": ..., \"amount\": ...}",
                    "GET  /busy",
                    "GET  /branches?page=1",
                ],
            })
        if not self.allowed():
            return

        if url.path == "/rates":
            frm, to = query.get("from"), query.get("to")
            if not frm or not to:
                return self.reply(400, {"error": "send both from and to, e.g. /rates?from=USD&to=INR"})
            pair = (frm.upper(), to.upper())
            if pair not in RATES:
                return self.reply(404, {"error": f"unknown currency pair: {pair[0]} to {pair[1]}"})
            return self.reply(200, {"from": pair[0], "to": pair[1], "rate": RATES[pair]})

        if url.path == "/busy":
            self.server.busy_calls += 1
            self.server.busy_times.append(time.monotonic())
            if self.server.busy_calls % 3 != 0:
                return self.reply(429, {"error": "head office is busy, try again later"},
                                  {"Retry-After": str(self.server.retry_after)})
            return self.reply(200, {"status": "ok", "message": "head office is free now"})

        if url.path == "/branches":
            try:
                page = int(query.get("page", "1"))
            except ValueError:
                return self.reply(400, {"error": "page must be a whole number"})
            start = (page - 1) * PAGE_SIZE
            if page < 1 or start >= len(BRANCHES):
                return self.reply(404, {"error": f"no page {page}"})
            items = BRANCHES[start:start + PAGE_SIZE]
            more = start + PAGE_SIZE < len(BRANCHES)
            return self.reply(200, {"page": page, "branches": items,
                                    "next_page": page + 1 if more else None})

        self.reply(404, {"error": f"no such endpoint: {url.path}"})

    # ---- POST ----------------------------------------------------------
    def do_POST(self):
        url = urlparse(self.path)
        if not self.allowed():
            return
        if url.path != "/applications":
            return self.reply(404, {"error": f"no such endpoint: {url.path}"})
        size = int(self.headers.get("Content-Length", 0))
        try:
            body = json.loads(self.rfile.read(size) or b"null")
        except json.JSONDecodeError:
            return self.reply(400, {"error": "the body is not valid JSON"})
        if not isinstance(body, dict):
            return self.reply(400, {"error": "send a JSON object with name and amount"})
        name, amount = body.get("name"), body.get("amount")
        if not isinstance(name, str) or not name.strip():
            return self.reply(400, {"error": "name is missing"})
        if isinstance(amount, bool) or not isinstance(amount, (int, float)) or amount <= 0:
            return self.reply(400, {"error": "amount must be a positive number"})
        self.server.next_id += 1
        self.reply(201, {"id": f"APP-{self.server.next_id}", "name": name,
                         "amount": amount, "status": "received"})


def start(port=0, retry_after=1, quiet=True):
    """Start the server in the background. Returns (server, base_url). Used by the tests."""
    server = ThreadingHTTPServer(("127.0.0.1", port), HeadOffice)
    server.busy_calls, server.busy_times = 0, []
    server.next_id, server.retry_after, server.quiet = 1000, retry_after, quiet
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_address[1]}"


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", PORT), HeadOffice)
    server.busy_calls, server.busy_times = 0, []
    server.next_id, server.retry_after, server.quiet = 1000, 1, False
    print(f"Head Office API running at http://127.0.0.1:{PORT}   (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
