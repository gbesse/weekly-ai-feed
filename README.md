# Weekly AI Feed

**Read AIHOT’s daily issues as a week-by-week JSON API.**

[English](README.md) · [Français](README.fr.md) · [Español](README.es.md)

## Related projects

- [AIHOT](https://github.com/KKKKhazix/AIHOT) — Publishes the feed consumed here.
- [Weekly API request #18](https://github.com/KKKKhazix/AIHOT/issues/18) — Asks for a less dense weekly REST view.
- [Daily RSS route](https://github.com/KKKKhazix/AIHOT/blob/main/apps/api/src/routes/feeds.ts) — Defines the real `/feed/daily.xml` route.

Links describe technical neighbors, not an affiliation.

## Try it

```sh
python3 weekly_feed.py demo
```

## What this checks

Parses the public `/feed/daily.xml` RSS feed and serves a local read-only `/api/weekly?week=YYYY-Www` endpoint. The index keeps dates, titles and source links; it does not invent a summary.

## Use with your data

```sh
curl -fsSL https://aihot.news/feed/daily.xml > /tmp/aihot-daily.xml
python3 weekly_feed.py serve --file /tmp/aihot-daily.xml --port 8765
curl "http://127.0.0.1:8765/api/weekly?week=2026-W40"
```

Fetch the public feed, then launch the local server against the saved XML as shown. A live RSS sample was parsed successfully on 30 September 2026.

## Scope and limits

AIHOT retains at most 30 daily issues in this feed, so older or incomplete weeks cannot be reconstructed. The API is an index, not a generated weekly narrative; it binds to localhost only and does not modify AIHOT.

## Tests

```sh
python3 -m unittest discover -s tests -v
```

MIT · v0.1.0-alpha.1
