import http.client
import json
import threading
import unittest

import server


class ServerApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.httpd = server.ThreadingHTTPServer(("127.0.0.1", 0), server.SortHandler)
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()
        cls.host, cls.port = cls.httpd.server_address

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()
        cls.thread.join()

    def setUp(self):
        server.sorter.clear()

    def request(self, method, path, payload=None):
        connection = http.client.HTTPConnection(self.host, self.port)
        body = json.dumps(payload).encode("utf-8") if payload is not None else None
        connection.request(method, path, body, {"Content-Type": "application/json"} if body else {})
        response = connection.getresponse()
        raw_body = response.read()
        result = json.loads(raw_body) if response.headers.get_content_type() == "application/json" else raw_body.decode("utf-8")
        connection.close()
        return response.status, result

    def test_health_and_static_files(self):
        status, payload = self.request("GET", "/api/health")
        self.assertEqual((status, payload), (200, {"ok": True}))

        status, body = self.request("GET", "/")
        self.assertEqual(status, 200)
        self.assertIn("Generate a dataset", body if isinstance(body, str) else "")

        for path, marker in (("/styles.css", ".shell"), ("/app.js", "request(")):
            with self.subTest(path=path):
                status, body = self.request("GET", path)
                self.assertEqual(status, 200)
                self.assertIn(marker, body)

    def test_data_can_be_created_sorted_and_deleted(self):
        status, payload = self.request("POST", "/api/data", {"data": [4, 1, 3]})
        self.assertEqual((status, payload), (200, {"data": [4, 1, 3]}))

        status, payload = self.request("POST", "/api/sort", {"algorithm": "quick"})
        self.assertEqual((status, payload), (200, {"data": [1, 3, 4], "algorithm": "quick"}))

        status, payload = self.request("DELETE", "/api/data")
        self.assertEqual((status, payload), (200, {"data": []}))

    def test_invalid_payloads_return_bad_request(self):
        status, payload = self.request("POST", "/api/data", {"data": [1, "two"]})
        self.assertEqual(status, 400)
        self.assertIn("data must be a list of integers", payload["error"])

        status, payload = self.request("POST", "/api/sort", {"algorithm": "unknown"})
        self.assertEqual(status, 400)
        self.assertIn("unknown algorithm", payload["error"])

    def test_generation_validates_range_and_size(self):
        status, payload = self.request("POST", "/api/generate", {"min": 2, "max": 2, "size": 3})
        self.assertEqual(status, 200)
        self.assertEqual(payload["data"], [2, 2, 2])

        status, payload = self.request("POST", "/api/generate", {"min": 5, "max": 1, "size": 3})
        self.assertEqual(status, 400)
        self.assertIn("invalid generation range", payload["error"])


if __name__ == "__main__":
    unittest.main()