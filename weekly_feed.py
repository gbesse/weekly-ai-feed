#!/usr/bin/env python3
"""Expose a weekly, source-linked index of AIHOT daily RSS issues."""
import argparse
import json
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

DEFAULT_URL = "https://aihot.news/feed/daily.xml"


def parse_feed(xml_bytes):
    root = ET.fromstring(xml_bytes)
    if root.tag != "rss":
        raise ValueError("expected an RSS 2.0 feed")
    channel = root.find("channel")
    if channel is None:
        raise ValueError("RSS channel is missing")
    issues = []
    for item in channel.findall("item"):
        title = item.findtext("title") or ""
        link = item.findtext("link") or ""
        date = item.findtext("pubDate") or ""
        if not title or not link or not date:
            continue
        published = parsedate_to_datetime(date).astimezone(timezone.utc)
        issues.append({"title": title, "link": link, "published": published.isoformat(),
                       "description_html": item.findtext("description") or ""})
    return issues


def week_index(issues, week):
    try:
        year, number = week.split("-W")
        datetime.fromisocalendar(int(year), int(number), 1)
    except (ValueError, TypeError) as error:
        raise ValueError("week must use YYYY-Www, for example 2026-W40") from error
    selected = [item for item in issues if datetime.fromisoformat(item["published"]).date().isocalendar()[:2] == (int(year), int(number))]
    unique = {item["link"]: item for item in selected}
    return {"week": week, "source": DEFAULT_URL, "count": len(unique),
            "issues": sorted(unique.values(), key=lambda x: x["published"]),
            "note": "Deterministic index of available daily issues; no generated summary. RSS keeps at most 30 issues."}


def load_xml(path=None, url=DEFAULT_URL):
    if path:
        return sys.stdin.buffer.read() if str(path) == "-" else Path(path).read_bytes()
    with urllib.request.urlopen(url, timeout=15) as response:
        return response.read(4 * 1024 * 1024)


def make_handler(issues):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            if parsed.path != "/api/weekly":
                self.send_error(404)
                return
            week = urllib.parse.parse_qs(parsed.query).get("week", [datetime.now(timezone.utc).strftime("%G-W%V")])[0]
            try:
                data = week_index(issues, week)
                body = json.dumps(data, ensure_ascii=False).encode("utf-8")
                status = 200
            except ValueError as error:
                body = json.dumps({"error": str(error)}).encode()
                status = 400
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *_):
            pass

    return Handler


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("demo", "render", "serve"))
    parser.add_argument("--file", type=Path)
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--week", default=datetime.now(timezone.utc).strftime("%G-W%V"))
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args(argv)
    path = Path(__file__).parent / "fixtures" / "daily.xml" if args.command == "demo" else args.file
    try:
        issues = parse_feed(load_xml(path, args.url))
        if args.command == "serve":
            if not 1 <= args.port <= 65535:
                parser.error("port must be between 1 and 65535")
            server = ThreadingHTTPServer(("127.0.0.1", args.port), make_handler(issues))
            print(f"http://127.0.0.1:{args.port}/api/weekly?week={args.week}")
            server.serve_forever()
            return 0
        print(json.dumps(week_index(issues, "2026-W40" if args.command == "demo" else args.week), ensure_ascii=False, indent=2))
        return 0
    except (OSError, ET.ParseError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
