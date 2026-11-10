import json, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import events

HTML = Path(__file__).with_name("dashboard.html")


def make_handler(on_run):
    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_GET(self):
            if self.path == "/events":
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Cache-Control", "no-cache")
                self.end_headers()
                i = events.last_reset()
                try:
                    while True:
                        for e in events.since(i):
                            self.wfile.write(f"data: {json.dumps(e)}\n\n".encode())
                            i += 1
                        self.wfile.flush()
                        time.sleep(0.1)
                except (BrokenPipeError, ConnectionResetError):
                    return
            body = HTML.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(body)

        def do_POST(self):
            ok = on_run()
            self.send_response(200 if ok else 409)
            self.end_headers()
            self.wfile.write(b"started" if ok else b"busy")
    return H


def serve(on_run, port=8000):
    srv = ThreadingHTTPServer(("127.0.0.1", port), make_handler(on_run))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
