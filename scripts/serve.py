#!/usr/bin/env python3
"""Local preview server for the Pooch Parlor site.

No dependencies — just Python 3. Serves the static site with clean URLs and
live reload: save any file under the site root and the browser refreshes itself.

    ./scripts/serve.py                  # serves ./site at http://localhost:8000
    ./scripts/serve.py --port 3000
    ./scripts/serve.py --root somewhere --no-open

Clean URLs mean /services loads site/services.html, which keeps the prototype's
link structure identical to what it will be once this moves to WordPress.
"""

import argparse
import hashlib
import mimetypes
import os
import socket
import sys
import threading
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

RELOAD_PATH = "/__reload"
POLL_MS = 400
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".claude"}

LIVE_RELOAD_JS = f"""
<script>
(function () {{
  var last = null;
  function poll() {{
    fetch("{RELOAD_PATH}", {{ cache: "no-store" }})
      .then(function (r) {{ return r.text(); }})
      .then(function (stamp) {{
        if (last !== null && stamp !== last) {{ location.reload(); return; }}
        last = stamp;
        setTimeout(poll, {POLL_MS});
      }})
      .catch(function () {{ setTimeout(poll, {POLL_MS} * 5); }});
  }}
  poll();
}})();
</script>
"""

EXTRA_TYPES = {
    ".webp": "image/webp",
    ".avif": "image/avif",
    ".svg": "image/svg+xml",
    ".woff": "font/woff",
    ".woff2": "font/woff2",
    ".webmanifest": "application/manifest+json",
}


def tree_stamp(root: Path) -> str:
    """Fingerprint of every file's path, size and mtime under root."""
    h = hashlib.sha1()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not d.startswith("."))
        for name in sorted(filenames):
            if name.startswith("."):
                continue
            p = Path(dirpath) / name
            try:
                st = p.stat()
            except OSError:
                continue
            h.update(str(p).encode())
            h.update(f"{st.st_mtime_ns}:{st.st_size}".encode())
    return h.hexdigest()


class PreviewHandler(SimpleHTTPRequestHandler):
    root = Path.cwd()

    def resolve(self, url_path: str):
        """Map a URL path to a file, honouring directory indexes and clean URLs."""
        rel = unquote(urlparse(url_path).path).lstrip("/")
        if ".." in Path(rel).parts:
            return None

        base = (self.root / rel).resolve()
        try:
            base.relative_to(self.root.resolve())
        except ValueError:
            return None  # escaped the site root

        candidates = []
        if rel in ("", "/"):
            candidates.append(self.root / "index.html")
        elif base.is_dir():
            candidates.append(base / "index.html")
        else:
            candidates.append(base)
            if not base.suffix:
                candidates.append(base.with_suffix(".html"))

        for c in candidates:
            if c.is_file():
                return c
        return None

    def send_bytes(self, status: int, body: bytes, content_type: str):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def serve_file(self, path: Path, status: int = 200):
        ctype = EXTRA_TYPES.get(path.suffix.lower()) or (
            mimetypes.guess_type(str(path))[0] or "application/octet-stream"
        )
        body = path.read_bytes()
        if path.suffix.lower() in (".html", ".htm"):
            text = body.decode("utf-8", "replace")
            if "</body>" in text:
                text = text.replace("</body>", LIVE_RELOAD_JS + "</body>", 1)
            else:
                text += LIVE_RELOAD_JS
            body = text.encode("utf-8")
            ctype = "text/html; charset=utf-8"
        self.send_bytes(status, body, ctype)

    def handle_request(self):
        if urlparse(self.path).path == RELOAD_PATH:
            self.send_bytes(200, tree_stamp(self.root).encode(), "text/plain")
            return

        target = self.resolve(self.path)
        if target:
            self.serve_file(target)
            return

        custom_404 = self.root / "404.html"
        if custom_404.is_file():
            self.serve_file(custom_404, status=404)
        else:
            self.send_bytes(404, b"<h1>404 - not found</h1>", "text/html; charset=utf-8")

    do_GET = handle_request
    do_HEAD = handle_request

    def log_message(self, fmt, *args):
        if RELOAD_PATH in (args[0] if args else ""):
            return  # the reload poller would drown out everything else
        sys.stderr.write("  %s\n" % (fmt % args))


def pick_port(preferred: int, tries: int = 20) -> int:
    for port in range(preferred, preferred + tries):
        with socket.socket() as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    raise SystemExit(f"No free port in {preferred}-{preferred + tries}")


def main():
    here = Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser(description="Preview the Pooch Parlor site locally.")
    ap.add_argument("--root", default=str(here / "site"), help="directory to serve (default: ./site)")
    ap.add_argument("--port", type=int, default=8000, help="preferred port (default: 8000)")
    ap.add_argument("--no-open", action="store_true", help="don't open a browser")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        raise SystemExit(f"Site root does not exist: {root}")

    PreviewHandler.root = root
    port = pick_port(args.port)
    url = f"http://localhost:{port}/"

    print(f"\n  Pooch Parlor preview")
    print(f"  serving  {root}")
    print(f"  at       {url}")
    print(f"  live reload on — edit a file and the page refreshes")
    print(f"  ctrl-c to stop\n")

    if not args.no_open:
        threading.Timer(0.4, lambda: webbrowser.open(url)).start()

    with ThreadingHTTPServer(("127.0.0.1", port), PreviewHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n  stopped\n")


if __name__ == "__main__":
    main()
