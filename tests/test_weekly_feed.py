import json
import threading
import unittest
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

from weekly_feed import make_handler, parse_feed, week_index


class WeeklyFeedTests(unittest.TestCase):
    def setUp(self):
        self.issues = parse_feed((Path(__file__).parent.parent / "fixtures" / "daily.xml").read_bytes())

    def test_only_requested_week_and_deduplicated_links(self):
        result = week_index(self.issues + [self.issues[0]], "2026-W40")
        self.assertEqual(result["count"], 2)
        self.assertEqual(result["issues"][0]["title"], "Daily issue 1")

    def test_http_api_returns_week(self):
        server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(self.issues))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{server.server_port}/api/weekly?week=2026-W40") as response:
                self.assertEqual(json.load(response)["count"], 2)
        finally:
            server.shutdown()
            server.server_close()

    def test_rejects_invalid_week(self):
        with self.assertRaises(ValueError):
            week_index(self.issues, "bad")
