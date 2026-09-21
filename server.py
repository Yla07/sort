import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from backend import sortowanie


ROOT = Path(__file__).parent
WEB_ROOT = ROOT / "web"
sorter = sortowanie()


class SortHandler(BaseHTTPRequestHandler):
    def _send_json(self, payload, status=200):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path):
        if not path.is_file():
            self.send_error(404)
            return

        content_types = {
            ".css": "text/css; charset=utf-8",
            ".html": "text/html; charset=utf-8",
            ".js": "text/javascript; charset=utf-8",
        }
        body = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_types.get(path.suffix, "application/octet-stream"))
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length) or b"{}")

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/data":
            self._send_json({"data": sorter.get_data()})
            return
        if path == "/api/health":
            self._send_json({"ok": True})
            return

        requested = "index.html" if path == "/" else path.removeprefix("/")
        file_path = (WEB_ROOT / requested).resolve()
        if WEB_ROOT.resolve() not in file_path.parents and file_path != WEB_ROOT.resolve():
            self.send_error(403)
            return
        self._send_file(file_path)

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            payload = self._read_json()
            if path == "/api/data":
                data = payload.get("data")
                if not isinstance(data, list) or any(not isinstance(value, int) for value in data):
                    raise ValueError("data must be a list of integers")
                sorter.data = data
                self._send_json({"data": sorter.get_data()})
                return

            if path == "/api/generate":
                minimum = int(payload["min"])
                maximum = int(payload["max"])
                size = int(payload["size"])
                if maximum < minimum or size < 1 or size > 1000:
                    raise ValueError("invalid generation range")
                sorter.data = sorter.generate_data(minimum, maximum, size)
                self._send_json({"data": sorter.get_data()})
                return

            if path == "/api/sort":
                algorithm = payload.get("algorithm")
                algorithms = {
                    "bubble": sorter.bubble_sort,
                    "quick": sorter.quick_sort,
                    "insertion": sorter.insertion_sort,
                    "selection": sorter.selection_sort,
                }
                if algorithm not in algorithms:
                    raise ValueError("unknown algorithm")
                sorter.data = algorithms[algorithm](list(sorter.get_data()))
                self._send_json({"data": sorter.get_data(), "algorithm": algorithm})
                return

            self.send_error(404)
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
            self._send_json({"error": str(error)}, 400)

    def do_DELETE(self):
        if urlparse(self.path).path != "/api/data":
            self.send_error(404)
            return
        sorter.clear()
        self._send_json({"data": sorter.get_data()})

    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}")


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 8000), SortHandler)
    print("Sort web app running at http://127.0.0.1:8000")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()