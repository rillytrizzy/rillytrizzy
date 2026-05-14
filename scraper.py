#!/usr/bin/env python3
"""
Scrape the most popular/viewed clips from Twitch, Kick, and YouTube
for streamer audiences. No API credentials required.

Usage:
    python scraper.py                                    # all 3 platforms
    python scraper.py --platforms twitch kick            # pick platforms
    python scraper.py --period LAST_MONTH --games 15     # Twitch options
    python scraper.py --json out.json --csv out.csv      # custom output

Period options (Twitch + Kick): LAST_DAY  LAST_WEEK  LAST_MONTH  ALL_TIME
"""

import argparse
import csv
import json
import re
import time
from typing import Optional

import requests

# ── shared ────────────────────────────────────────────────────────────────────

_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)
_DELAY = 0.4  # polite pause between requests (seconds)


def _get(url: str, headers: Optional[dict] = None, **kwargs) -> requests.Response:
    h = {"User-Agent": _UA}
    if headers:
        h.update(headers)
    resp = requests.get(url, headers=h, timeout=15, **kwargs)
    resp.raise_for_status()
    return resp


# ── Twitch ────────────────────────────────────────────────────────────────────
# Uses Twitch's own public GQL endpoint — the same one your browser sends
# when you visit twitch.tv. The client-id is publicly embedded in every page.

_TWITCH_GQL = "https://gql.twitch.tv/gql"
_TWITCH_CID = "kimne78kx3ncx6brgo4mv6wki5h1ko"

_TOP_GAMES_QUERY = """
query TopGames($limit: Int!) {
  games(first: $limit) { edges { node { name } } }
}
"""

_GAME_CLIPS_QUERY = """
query GameClips($gameName: String!, $criteria: GameClipsCriteria!, $limit: Int!) {
  game(name: $gameName) {
    clips(criteria: $criteria, first: $limit) {
      edges {
        node {
          id title viewCount durationSeconds createdAt url thumbnailURL
          broadcaster { displayName login }
          curator      { displayName }
        }
      }
    }
  }
}
"""

_TWITCH_FALLBACK_GAMES = [
    "Just Chatting", "Fortnite", "League of Legends", "Minecraft",
    "Grand Theft Auto V", "Valorant", "Counter-Strike 2", "Apex Legends",
    "Call of Duty: Warzone", "World of Warcraft",
]


def _twitch_gql(payload: list) -> list:
    resp = requests.post(
        _TWITCH_GQL,
        headers={"Client-ID": _TWITCH_CID, "Content-Type": "application/json"},
        json=payload,
        timeout=15,
    )
    if resp.status_code == 403:
        raise PermissionError(
            "Twitch GQL returned 403. Twitch now requires registered credentials for "
            "reliable API access. Register a free app at https://dev.twitch.tv/console/apps "
            "and set TWITCH_CLIENT_ID + TWITCH_CLIENT_SECRET in .env, then re-run with "
            "`python scraper.py --platforms twitch` (the .env-based Helix path will be used)."
        )
    resp.raise_for_status()
    return resp.json()


def _twitch_top_games(limit: int) -> list[str]:
    try:
        data = _twitch_gql([{"query": _TOP_GAMES_QUERY, "variables": {"limit": limit}}])
        return [e["node"]["name"] for e in data[0]["data"]["games"]["edges"]]
    except PermissionError as exc:
        print(f"\n  [Twitch] {exc}\n")
        print("  Falling back to hardcoded top-games list for this run.")
        return _TWITCH_FALLBACK_GAMES[:limit]
    except Exception as exc:
        print(f"  [Twitch] top-games query failed ({exc}), using fallback list")
        return _TWITCH_FALLBACK_GAMES[:limit]


def scrape_twitch(top_games: int = 10, clips_per_game: int = 20, period: str = "LAST_WEEK") -> list[dict]:
    print(f"\n[Twitch] Fetching top {top_games} games...")
    games = _twitch_top_games(top_games)
    print(f"  Games: {', '.join(games)}")

    clips: list[dict] = []
    _twitch_403_warned = False
    for game_name in games:
        print(f"  [{game_name}] fetching clips...")
        try:
            result = _twitch_gql([{
                "query": _GAME_CLIPS_QUERY,
                "variables": {
                    "gameName": game_name,
                    "limit": clips_per_game,
                    "criteria": {"filter": period},
                },
            }])
            game_data = (result[0].get("data") or {}).get("game") or {}
            nodes = [e["node"] for e in game_data.get("clips", {}).get("edges", [])]
        except PermissionError:
            if not _twitch_403_warned:
                print("    Twitch requires credentials — skipping remaining games.")
                _twitch_403_warned = True
            break
        except Exception as exc:
            print(f"    Skipped: {exc}")
            continue

        for n in nodes:
            clips.append({
                "platform": "twitch",
                "game": game_name,
                "clip_id": n["id"],
                "title": n["title"],
                "channel": n["broadcaster"]["displayName"],
                "channel_url": f"https://twitch.tv/{n['broadcaster']['login']}",
                "creator": (n.get("curator") or {}).get("displayName", ""),
                "view_count": n["viewCount"],
                "duration_sec": n["durationSeconds"],
                "created_at": n["createdAt"],
                "url": n["url"],
                "thumbnail_url": n["thumbnailURL"],
            })
        time.sleep(_DELAY)

    print(f"  Collected {len(clips)} Twitch clips")
    return clips


# ── Kick ──────────────────────────────────────────────────────────────────────

_KICK_API = "https://kick.com/api/v2/clips"
_KICK_PERIOD = {"LAST_DAY": "day", "LAST_WEEK": "week", "LAST_MONTH": "month", "ALL_TIME": "all"}


def scrape_kick(limit: int = 100, period: str = "LAST_WEEK") -> list[dict]:
    kperiod = _KICK_PERIOD.get(period, "week")
    print(f"\n[Kick] Fetching top clips (period={kperiod})...")

    clips: list[dict] = []
    page = 1
    while len(clips) < limit:
        try:
            resp = _get(
                _KICK_API,
                headers={"Accept": "application/json"},
                params={"sort": "view_count", "time": kperiod, "page": page},
            )
        except requests.HTTPError as exc:
            print(f"  [Kick] request failed: {exc}")
            break

        data = resp.json()
        # Kick has used two different response shapes
        raw = data.get("clips") or (data.get("data") or {}).get("clips") or []
        if not raw:
            break

        for c in raw:
            ch = c.get("channel") or {}
            user = ch.get("user") or {}
            cat = c.get("category") or {}
            slug = ch.get("slug") or user.get("username", "")
            clips.append({
                "platform": "kick",
                "game": cat.get("name", ""),
                "clip_id": str(c.get("id", "")),
                "title": c.get("title", ""),
                "channel": slug,
                "channel_url": f"https://kick.com/{slug}" if slug else "",
                "creator": user.get("username", ""),
                "view_count": c.get("views") or c.get("view_count") or 0,
                "duration_sec": c.get("duration") or 0,
                "created_at": c.get("created_at", ""),
                "url": c.get("clip_url", ""),
                "thumbnail_url": c.get("thumbnail_url", ""),
            })

        if len(raw) < 20:
            break  # last page
        page += 1
        time.sleep(_DELAY)

    result = clips[:limit]
    print(f"  Collected {len(result)} Kick clips")
    return result


# ── YouTube ───────────────────────────────────────────────────────────────────
# Extracts the ytInitialData blob that YouTube embeds in every search-results
# page. No API key needed — same data your browser parses when you search.

_YT_SEARCH = "https://www.youtube.com/results"
_YT_SORT_VIEWS = "CAMSAhAB"  # protobuf-encoded sort=view_count param

_YT_QUERIES = [
    "best twitch clips",
    "best kick clips",
    "best streaming clips highlights",
]


def _parse_views(text: str) -> int:
    text = text.lower().replace(",", "").replace(" views", "").strip()
    try:
        if text.endswith("b"):
            return int(float(text[:-1]) * 1_000_000_000)
        if text.endswith("m"):
            return int(float(text[:-1]) * 1_000_000)
        if text.endswith("k"):
            return int(float(text[:-1]) * 1_000)
        return int(text)
    except (ValueError, AttributeError):
        return 0


def _parse_yt_html(html: str) -> list[dict]:
    m = re.search(r"var ytInitialData\s*=\s*(\{.+?\});\s*</script>", html, re.DOTALL)
    if not m:
        return []
    try:
        data = json.loads(m.group(1))
    except json.JSONDecodeError:
        return []

    try:
        items = (
            data["contents"]["twoColumnSearchResultsRenderer"]
            ["primaryContents"]["sectionListRenderer"]
            ["contents"][0]["itemSectionRenderer"]["contents"]
        )
    except (KeyError, IndexError):
        return []

    videos = []
    for item in items:
        vr = item.get("videoRenderer") or {}
        if not vr:
            continue
        vid_id = vr.get("videoId", "")
        title = ((vr.get("title") or {}).get("runs") or [{}])[0].get("text", "")
        channel = ((vr.get("ownerText") or {}).get("runs") or [{}])[0].get("text", "")
        vct = vr.get("viewCountText") or {}
        view_text = vct.get("simpleText") or (vct.get("runs") or [{}])[0].get("text", "")
        thumbs = (vr.get("thumbnail") or {}).get("thumbnails") or []
        published = (vr.get("publishedTimeText") or {}).get("simpleText", "")
        if vid_id and title:
            videos.append({
                "video_id": vid_id,
                "title": title,
                "channel": channel,
                "view_count": _parse_views(view_text),
                "published": published,
                "url": f"https://www.youtube.com/watch?v={vid_id}",
                "thumbnail_url": thumbs[-1]["url"] if thumbs else "",
            })
    return videos


def scrape_youtube(limit: int = 60, queries: Optional[list[str]] = None) -> list[dict]:
    if queries is None:
        queries = _YT_QUERIES
    print(f"\n[YouTube] Searching for streamer clips...")

    seen: set[str] = set()
    clips: list[dict] = []

    for query in queries:
        print(f"  Query: {query!r}")
        try:
            resp = _get(_YT_SEARCH, params={"search_query": query, "sp": _YT_SORT_VIEWS})
        except Exception as exc:
            print(f"    Skipped: {exc}")
            continue

        for v in _parse_yt_html(resp.text):
            if v["video_id"] in seen:
                continue
            seen.add(v["video_id"])
            clips.append({
                "platform": "youtube",
                "game": "",
                "clip_id": v["video_id"],
                "title": v["title"],
                "channel": v["channel"],
                "channel_url": "",
                "creator": v["channel"],
                "view_count": v["view_count"],
                "duration_sec": 0,
                "created_at": v["published"],
                "url": v["url"],
                "thumbnail_url": v["thumbnail_url"],
            })
        time.sleep(_DELAY)

    result = sorted(clips, key=lambda c: c["view_count"], reverse=True)[:limit]
    print(f"  Collected {len(result)} YouTube clips")
    return result


# ── combined ──────────────────────────────────────────────────────────────────


def scrape_all(
    platforms: list[str],
    period: str = "LAST_WEEK",
    twitch_games: int = 10,
    twitch_clips: int = 20,
    kick_clips: int = 100,
    yt_clips: int = 60,
    output_json: str = "clips.json",
    output_csv: str = "clips.csv",
) -> list[dict]:
    all_clips: list[dict] = []

    if "twitch" in platforms:
        all_clips.extend(scrape_twitch(twitch_games, twitch_clips, period))
    if "kick" in platforms:
        all_clips.extend(scrape_kick(kick_clips, period))
    if "youtube" in platforms:
        all_clips.extend(scrape_youtube(yt_clips))

    all_clips.sort(key=lambda c: c["view_count"], reverse=True)

    with open(output_json, "w", encoding="utf-8") as fh:
        json.dump(all_clips, fh, indent=2, ensure_ascii=False)
    print(f"\nSaved {len(all_clips)} clips -> {output_json}")

    if all_clips:
        with open(output_csv, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(all_clips[0].keys()))
            writer.writeheader()
            writer.writerows(all_clips)
        print(f"Saved {len(all_clips)} clips -> {output_csv}")

    print("\nTop 10 clips across all platforms:")
    for i, clip in enumerate(all_clips[:10], 1):
        tag = clip["platform"].upper()
        game = f" ({clip['game']})" if clip["game"] else ""
        print(
            f"  {i:2}. [{tag:7}] [{clip['view_count']:>9,} views] "
            f"{clip['title']!r} — {clip['channel']}{game}"
        )
        print(f"       {clip['url']}")

    return all_clips


# ── CLI ───────────────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scrape popular clips from Twitch, Kick, and YouTube (no credentials needed)."
    )
    parser.add_argument(
        "--platforms", nargs="+",
        default=["twitch", "kick", "youtube"],
        choices=["twitch", "kick", "youtube"],
        help="Platforms to include (default: all three)",
    )
    parser.add_argument(
        "--period", default="LAST_WEEK",
        choices=["LAST_DAY", "LAST_WEEK", "LAST_MONTH", "ALL_TIME"],
        help="Time window for popularity on Twitch + Kick (default: LAST_WEEK)",
    )
    parser.add_argument("--games", type=int, default=10, metavar="N",
                        help="Top games for Twitch scraping (default: 10)")
    parser.add_argument("--twitch-clips", type=int, default=20, metavar="N",
                        help="Clips per Twitch game (default: 20)")
    parser.add_argument("--kick-clips", type=int, default=100, metavar="N",
                        help="Total Kick clips (default: 100)")
    parser.add_argument("--yt-clips", type=int, default=60, metavar="N",
                        help="Total YouTube clips (default: 60)")
    parser.add_argument("--json", dest="json_out", default="clips.json", metavar="PATH",
                        help="JSON output file (default: clips.json)")
    parser.add_argument("--csv", dest="csv_out", default="clips.csv", metavar="PATH",
                        help="CSV output file (default: clips.csv)")
    args = parser.parse_args()

    scrape_all(
        platforms=args.platforms,
        period=args.period,
        twitch_games=args.games,
        twitch_clips=args.twitch_clips,
        kick_clips=args.kick_clips,
        yt_clips=args.yt_clips,
        output_json=args.json_out,
        output_csv=args.csv_out,
    )


if __name__ == "__main__":
    main()
