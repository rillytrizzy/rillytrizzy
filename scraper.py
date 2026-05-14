#!/usr/bin/env python3
"""
Scrape the most popular/viewed Twitch clips targeting streamer audiences.

Uses the Twitch Helix API (client credentials flow — no user login required).
Fetches top clips across the most-watched games and outputs JSON + CSV.

Setup:
    1. Register a Twitch app at https://dev.twitch.tv/console/apps
    2. Copy .env.example -> .env and fill in your credentials
    3. pip install -r requirements.txt
    4. python scraper.py

Optional flags:
    --games N    Number of top games to pull clips from  (default: 10)
    --clips N    Clips per game                          (default: 20)
    --days  N    Lookback window in days                 (default: 7)
    --json  PATH JSON output file                        (default: clips.json)
    --csv   PATH CSV output file                         (default: clips.csv)
"""

import argparse
import csv
import json
import os
import time
from datetime import datetime, timedelta, timezone

import requests
from dotenv import load_dotenv

load_dotenv()

_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID", "")
_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET", "")

_AUTH_URL = "https://id.twitch.tv/oauth2/token"
_BASE_URL = "https://api.twitch.tv/helix"

# Twitch rate-limit headroom: ~800 req/min on default tier.
# 0.1 s between calls keeps us well under the limit.
_REQUEST_DELAY = 0.1


def _get_token() -> str:
    resp = requests.post(
        _AUTH_URL,
        params={
            "client_id": _CLIENT_ID,
            "client_secret": _CLIENT_SECRET,
            "grant_type": "client_credentials",
        },
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def _get(token: str, path: str, params: dict) -> dict:
    headers = {
        "Client-ID": _CLIENT_ID,
        "Authorization": f"Bearer {token}",
    }
    resp = requests.get(
        f"{_BASE_URL}/{path}",
        headers=headers,
        params=params,
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()


def get_top_games(token: str, limit: int = 10) -> list[dict]:
    return _get(token, "games/top", {"first": limit})["data"]


def get_top_clips(
    token: str,
    *,
    game_id: str | None = None,
    broadcaster_id: str | None = None,
    started_at: str | None = None,
    ended_at: str | None = None,
    limit: int = 20,
) -> list[dict]:
    params: dict = {"first": limit}
    if game_id:
        params["game_id"] = game_id
    if broadcaster_id:
        params["broadcaster_id"] = broadcaster_id
    if started_at:
        params["started_at"] = started_at
    if ended_at:
        params["ended_at"] = ended_at
    return _get(token, "clips", params).get("data", [])


def scrape(
    top_games: int = 10,
    clips_per_game: int = 20,
    period_days: int = 7,
    output_json: str = "clips.json",
    output_csv: str = "clips.csv",
) -> list[dict]:
    if not _CLIENT_ID or not _CLIENT_SECRET:
        raise RuntimeError(
            "TWITCH_CLIENT_ID and TWITCH_CLIENT_SECRET must be set. "
            "Copy .env.example to .env and fill in your app credentials."
        )

    print("Authenticating with Twitch...")
    token = _get_token()

    now = datetime.now(timezone.utc)
    started_at = (now - timedelta(days=period_days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    ended_at = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    print(f"Fetching top {top_games} games...")
    games = get_top_games(token, top_games)

    all_clips: list[dict] = []

    for game in games:
        game_name = game["name"]
        game_id = game["id"]
        print(f"  [{game_name}] fetching up to {clips_per_game} clips...")

        try:
            clips = get_top_clips(
                token,
                game_id=game_id,
                started_at=started_at,
                ended_at=ended_at,
                limit=clips_per_game,
            )
        except requests.HTTPError as exc:
            print(f"    Warning: {exc} — skipping {game_name}")
            continue

        for clip in clips:
            all_clips.append(
                {
                    "game": game_name,
                    "game_id": game_id,
                    "clip_id": clip["id"],
                    "title": clip["title"],
                    "broadcaster_name": clip["broadcaster_name"],
                    "creator_name": clip["creator_name"],
                    "view_count": clip["view_count"],
                    "duration": clip["duration"],
                    "created_at": clip["created_at"],
                    "url": clip["url"],
                    "thumbnail_url": clip["thumbnail_url"],
                }
            )

        time.sleep(_REQUEST_DELAY)

    # Sort overall by view count so the most viral clips bubble to the top.
    all_clips.sort(key=lambda c: c["view_count"], reverse=True)

    # --- persist ---
    with open(output_json, "w", encoding="utf-8") as fh:
        json.dump(all_clips, fh, indent=2, ensure_ascii=False)
    print(f"\nSaved {len(all_clips)} clips -> {output_json}")

    if all_clips:
        with open(output_csv, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(all_clips[0].keys()))
            writer.writeheader()
            writer.writerows(all_clips)
        print(f"Saved {len(all_clips)} clips -> {output_csv}")

    # Print quick summary
    print("\nTop 10 clips by view count:")
    for i, clip in enumerate(all_clips[:10], 1):
        print(
            f"  {i:2}. [{clip['view_count']:>8,} views] "
            f"{clip['title']!r} — {clip['broadcaster_name']} ({clip['game']})"
        )
        print(f"       {clip['url']}")

    return all_clips


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scrape the most popular Twitch clips for streamer audiences."
    )
    parser.add_argument(
        "--games", type=int, default=10, metavar="N",
        help="Number of top games to scrape (default: 10)",
    )
    parser.add_argument(
        "--clips", type=int, default=20, metavar="N",
        help="Max clips per game (default: 20)",
    )
    parser.add_argument(
        "--days", type=int, default=7, metavar="N",
        help="Lookback window in days (default: 7)",
    )
    parser.add_argument(
        "--json", dest="json_out", default="clips.json", metavar="PATH",
        help="JSON output file (default: clips.json)",
    )
    parser.add_argument(
        "--csv", dest="csv_out", default="clips.csv", metavar="PATH",
        help="CSV output file (default: clips.csv)",
    )
    args = parser.parse_args()

    scrape(
        top_games=args.games,
        clips_per_game=args.clips,
        period_days=args.days,
        output_json=args.json_out,
        output_csv=args.csv_out,
    )


if __name__ == "__main__":
    main()
