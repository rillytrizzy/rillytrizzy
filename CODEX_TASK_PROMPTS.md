# Agent Network — Codex Task Prompts
**Version:** 1.0
**Date:** 2026-05-30
**Ref:** AUTOMATION_TASKS.md T05–T13, pipeline.py, scraper.py

Copy-paste prompts for Codex (or any code-capable AI agent).
Each prompt is self-contained and includes acceptance criteria.
Run one at a time. Verify each before moving to the next.

---

## CODEX PROMPT: T05 + T07 — Update Pipeline Routing

**File:** `pipeline.py`
**Scope:** `ACCOUNT_PROFILES` dict and `generate_metadata()` function

```
Update pipeline.py with two changes:

CHANGE 1 — Update ACCOUNT_PROFILES (lines ~36–62)
Replace the `niche` field value for each account with the exact text below.
Do not change any other field. Do not change status or default_hashtags.

"agent_maxxing": niche = "AI tool demos, agent workflows, automation hacks, future-of-work commentary, build logs"
"agent_afterhours": niche = "festival highlights, DJ set clips, music drops, nightlife vibe content, artist spotlights"
"agent_pastforward": niche = "historical predictions, forgotten technology, then-vs-now timelines, future forecasting"
"agent_viral": niche = "viral fails, crowd reactions, unexpected moments, trending clips, cross-genre entertainment"
"agent_trending": niche = "current trends, internet culture, commentary on trending topics, cultural moments"

CHANGE 2 — Extend generate_metadata() routing prompt
In the function generate_metadata() (search for the string "You are routing content for the Agent Network"),
replace the prompt variable so that the account descriptions section lists both the niche AND
the content pillars for each account.

The new account_descriptions variable should produce this format per account:
  agent_maxxing [STATUS]: AI tool demos, agent workflows, automation hacks, future-of-work commentary, build logs
    Pillars: AI Tool Demos | Agent Culture | Productivity Hacks | Future-of-Work Commentary | Build Logs

  agent_afterhours [STATUS]: festival highlights, DJ set clips, music drops, nightlife vibe content, artist spotlights
    Pillars: Festival Highlights | DJ Set Clips | Music Drops | Nightlife Culture | Artist Spotlights

  agent_pastforward [STATUS]: historical predictions, forgotten technology, then-vs-now timelines, future forecasting
    Pillars: They Predicted This | Forgotten Technology | Timeline Comparisons | Future Forecasting | Historical Turning Points

  agent_viral [STATUS]: viral fails, crowd reactions, unexpected moments, trending clips, cross-genre entertainment
    Pillars: Top Clips of the Week | Reaction Compilations | Unexpected Moments | Trending Formats | Cross-Genre Entertainment

  agent_trending [STATUS]: current trends, internet culture, commentary on trending topics, cultural moments
    Pillars: Trend Breakdowns | Internet Culture | News-Driven Content | Cultural Commentary

Build this string from ACCOUNT_PROFILES. Add a `pillars` list field to each profile dict
to store these values, then use them in the prompt construction.

Acceptance criteria:
- ACCOUNT_PROFILES niche values match the strings above exactly
- ACCOUNT_PROFILES has a new `pillars` list field for each account
- generate_metadata() prompt includes both niche and pillars per account
- No other functions are modified
- All existing tests pass (run: python -c "import pipeline; print('OK')")
```

---

## CODEX PROMPT: T08 — Add Copyright Risk Flag

**File:** `pipeline.py`
**Scope:** `generate_metadata()` function and output manifest

```
Add copyright_risk detection to pipeline.py.

STEP 1 — Extend generate_metadata() return value
In generate_metadata(), update the Claude prompt to ask for a copyright_risk boolean.
Add this to the JSON the prompt requests:

  "copyright_risk": true | false

Trigger copyright_risk: true when ANY of the following are detected:
- Transcript contains recognizable song lyrics (more than 4 consecutive words that sound like song lyrics)
- Source URL domain is: soundcloud.com, spotify.com, bandcamp.com, beatport.com, audiomack.com
- Source URL domain is: youtube.com AND title contains artist name + "official audio/video"
- Transcript contains phrases like "the chorus", "verse", "hook", "bridge" in a music context

STEP 2 — Add fallback copyright check in the calling code
In the loop that calls generate_metadata() per clip (in run_pipeline()),
add a pre-check BEFORE calling Claude:

music_domains = {"soundcloud.com", "spotify.com", "bandcamp.com", "beatport.com"}
if any(domain in source_url for domain in music_domains):
    force_copyright_risk = True
else:
    force_copyright_risk = False

Pass force_copyright_risk into generate_metadata() as a parameter.
If force_copyright_risk is True, set copyright_risk: True regardless of Claude output.

STEP 3 — Add copyright_risk to clip_results dict
In the clip_results.append() call in run_pipeline(), add:
  "copyright_risk": meta.get("copyright_risk", force_copyright_risk),

STEP 4 — Print copyright warning in terminal output
In the per-clip print statement, add:
  © = "© MUSIC RISK" if r["copyright_risk"] else ""
  Print: f"      {clip.name} → @{account} ({confidence:.0%}){flag}{©}"

Acceptance criteria:
- review_queue.json includes "copyright_risk": true|false for every clip
- Music domain URLs always produce copyright_risk: true
- Terminal output shows "© MUSIC RISK" for flagged clips
- No other pipeline behavior changes
- run: python -c "import pipeline; print('OK')"
```

---

## CODEX PROMPT: T09 — Add --brands CLI Argument

**File:** `pipeline.py`
**Scope:** `main()` function and `run_pipeline()` function

```
Add a --brands CLI argument to pipeline.py that restricts which accounts the
routing classifier is allowed to route content to.

STEP 1 — Add argparse argument in main()
After the existing `parser.add_argument("--output", ...)` line, add:

parser.add_argument(
    "--brands",
    nargs="+",
    metavar="ACCOUNT",
    help="Restrict routing to these accounts only (e.g. --brands agent_maxxing agent_afterhours)",
)

STEP 2 — Pass brands to run_pipeline()
Update the run_pipeline() call in main() to pass args.brands:
  run_pipeline(args.url, Path(args.output), args.clip_duration, allowed_brands=args.brands)

STEP 3 — Add allowed_brands parameter to run_pipeline()
Update the run_pipeline() function signature:
  def run_pipeline(url: str, output_root: Path, clip_duration: int = 45, allowed_brands: list = None) -> dict:

STEP 4 — Filter ACCOUNT_PROFILES when allowed_brands is set
After the existing `run_dir.mkdir(...)` line in run_pipeline(), add:

if allowed_brands:
    invalid = [b for b in allowed_brands if b not in ACCOUNT_PROFILES]
    if invalid:
        print(f"Warning: unknown brands ignored: {invalid}")
    active_for_run = [b for b in allowed_brands if b in ACCOUNT_PROFILES]
else:
    active_for_run = ACTIVE_ACCOUNTS

STEP 5 — Pass active_for_run into generate_metadata()
Update the generate_metadata() call to pass the allowed account list.
In generate_metadata(), use this list instead of deriving from ACCOUNT_PROFILES directly
when building the account_descriptions string shown to Claude.

Also: if the routed account is not in active_for_run, override with active_for_run[0]
and set confidence to 0.0.

Acceptance criteria:
- `python pipeline.py <url> --brands agent_maxxing` only routes to agent_maxxing
- `python pipeline.py <url> --brands agent_viral agent_maxxing` routes to either
- Without --brands, behavior is unchanged (routes to ACTIVE_ACCOUNTS)
- Unknown brand names print a warning and are ignored
- run: python pipeline.py --help  shows --brands in usage
```

---

## CODEX PROMPT: T10 + T11 + T12 — YouTube Search Scraper + Brand Presets + --brand Argument

**File:** `scraper.py`
**Scope:** New function, new config dict, new CLI argument

```
Add three things to scraper.py:

CHANGE 1 — Add BRAND_SEARCH_QUERIES config dict (insert after the imports section,
before any function definitions)

BRAND_SEARCH_QUERIES = {
    "agent_maxxing": [
        "AI agent demo 2026",
        "Claude automation workflow",
        "AI productivity hack tutorial",
        "LLM agent build walkthrough",
        "AI coding agent maxxing",
    ],
    "agent_afterhours": [
        "EDC 2026 festival highlights",
        "festival drop reaction crowd",
        "DJ set best moment 2026",
        "AriAtHome highlights set",
        "Tomorrowland 2026 main stage",
    ],
    "agent_pastforward": [
        "old prediction came true technology",
        "retro futurism technology comparison",
        "vintage future prediction accurate",
        "1980s prediction today technology",
        "they predicted smartphones internet",
    ],
    "agent_viral": [
        "best clip of the week compilation",
        "unexpected moment caught on camera",
        "funny viral fail 2026",
        "crowd reaction compilation",
        "unbelievable moment sports 2026",
    ],
    "agent_trending": [
        "viral trend explained 2026",
        "internet culture moment 2026",
        "trending topic breakdown",
        "social media trend reaction",
    ],
}

CHANGE 2 — Add scrape_youtube_search(query, limit, brand=None) function
Add this function after the existing scrape_youtube() function (or after scrape_kick()
if scrape_youtube() does not exist):

def scrape_youtube_search(query: str, limit: int = 10, brand: str = None) -> list[dict]:
    """Search YouTube for clips matching query using yt-dlp. Returns same schema as other scrapers."""
    import yt_dlp
    print(f"\n[YouTube Search] Query: '{query}' (limit={limit})")
    
    search_url = f"ytsearch{limit}:{query}"
    results = []
    
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
        "skip_download": True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_url, download=False)
            entries = info.get("entries") or []
            for entry in entries:
                if not entry:
                    continue
                results.append({
                    "platform": "youtube",
                    "game": "",
                    "clip_id": entry.get("id", ""),
                    "title": entry.get("title", ""),
                    "channel": entry.get("uploader") or entry.get("channel", ""),
                    "channel_url": f"https://youtube.com/channel/{entry.get('channel_id', '')}",
                    "view_count": entry.get("view_count") or 0,
                    "duration_sec": entry.get("duration") or 0,
                    "created_at": entry.get("upload_date", ""),
                    "url": f"https://youtube.com/watch?v={entry.get('id', '')}",
                    "thumbnail_url": entry.get("thumbnail", ""),
                    "account": brand or "",
                    "search_query": query,
                })
    except Exception as exc:
        print(f"  [YouTube Search] Failed for query '{query}': {exc}")
    
    print(f"  Collected {len(results)} results")
    return results

CHANGE 3 — Add --brand CLI argument
In the main() function's argparse setup, add:

parser.add_argument(
    "--brand",
    choices=list(BRAND_SEARCH_QUERIES.keys()),
    metavar="BRAND",
    help="Run YouTube search for a specific brand using preset queries (e.g. --brand agent_maxxing)",
)

In the main() function body, after the existing platform scraping logic, add:

if args.brand:
    queries = BRAND_SEARCH_QUERIES[args.brand]
    for q in queries:
        brand_clips = scrape_youtube_search(q, limit=5, brand=args.brand)
        clips.extend(brand_clips)

Acceptance criteria:
- python scraper.py --brand agent_maxxing runs 5 YouTube searches and returns results
- Results include "account": "agent_maxxing" field
- python scraper.py (no --brand) behavior is unchanged
- scrape_youtube_search() returns same schema as scrape_twitch()
- run: python -c "from scraper import scrape_youtube_search, BRAND_SEARCH_QUERIES; print('OK')"
```

---

## CODEX PROMPT: T13 — Archive.org Scraper Stub

**File:** `scraper.py`
**Scope:** New function `scrape_archive_org()`

```
Add a scrape_archive_org() function to scraper.py for agent_pastforward source discovery.

Add this function after scrape_youtube_search():

def scrape_archive_org(query: str, limit: int = 10, collection: str = "prelinger") -> list[dict]:
    """
    Search Archive.org for public domain video clips matching query.
    Default collection: Prelinger Archives (historical footage, fully public domain).
    Returns same schema as other scraper functions.
    """
    import urllib.parse
    
    print(f"\n[Archive.org] Query: '{query}' | Collection: {collection}")
    
    params = {
        "q": f"collection:{collection} mediatype:movies {query}",
        "fl[]": ["identifier", "title", "description", "date", "downloads"],
        "sort[]": "downloads desc",
        "rows": limit,
        "page": 1,
        "output": "json",
    }
    
    url = "https://archive.org/advancedsearch.php"
    results = []
    
    try:
        resp = _get(url, params=params)
        data = resp.json()
        docs = data.get("response", {}).get("docs", [])
        
        for doc in docs:
            identifier = doc.get("identifier", "")
            if not identifier:
                continue
            
            results.append({
                "platform": "archive.org",
                "game": "",
                "clip_id": identifier,
                "title": doc.get("title", ""),
                "channel": "Archive.org / Prelinger",
                "channel_url": f"https://archive.org/details/{identifier}",
                "view_count": doc.get("downloads", 0),
                "duration_sec": 0,
                "created_at": doc.get("date", ""),
                "url": f"https://archive.org/download/{identifier}/{identifier}.mp4",
                "thumbnail_url": f"https://archive.org/services/img/{identifier}",
                "account": "agent_pastforward",
                "license": "public_domain",
                "search_query": query,
            })
    except Exception as exc:
        print(f"  [Archive.org] Search failed: {exc}")
    
    print(f"  Found {len(results)} Archive.org items")
    return results

Also add archive.org to BRAND_SEARCH_QUERIES for agent_pastforward as additional
search terms (append to existing list, do not replace):
    "prelinger futurism",
    "1950s technology prediction film",
    "space age future documentary",

Also add "archive" as an optional platform choice in the --platforms argument
if it already uses choices=[]. If it uses a free-form list, add archive.org handling
in main() after the brand section:

if "archive" in (args.platforms or []):
    for q in BRAND_SEARCH_QUERIES.get("agent_pastforward", [])[:3]:
        clips.extend(scrape_archive_org(q, limit=5))

Acceptance criteria:
- python -c "from scraper import scrape_archive_org; print('OK')"
- scrape_archive_org("futurism film", limit=3) returns a list (may be empty if network unavailable)
- All returned items have "license": "public_domain" and "account": "agent_pastforward"
- Existing scraper behavior unchanged
- URL format: https://archive.org/download/<identifier>/<identifier>.mp4
```

---

## CODEX PROMPT: T17 — Add Series Field to Pipeline Manifest

**File:** `pipeline.py`
**Scope:** `run_pipeline()` function and `generate_metadata()` function

```
Add a `series` field to the pipeline.py output manifest to support campaign tagging.

STEP 1 — Add --series CLI argument in main()
After the --brands argument, add:

parser.add_argument(
    "--series",
    default=None,
    metavar="SERIES_NAME",
    help="Tag all output clips with a series name (e.g. --series fastest_timeline)",
)

STEP 2 — Pass series to run_pipeline()
Update run_pipeline() call: run_pipeline(..., series=args.series)
Update run_pipeline() signature: def run_pipeline(..., series: str = None) -> dict:

STEP 3 — Add series to clip_results
In clip_results.append(), add:
  "series": series,

STEP 4 — Add series to the manifest
In build_review_queue(), the manifest dict already includes "clips".
The series field is per-clip — no manifest-level change needed.

Acceptance criteria:
- python pipeline.py <url> --series fastest_timeline produces review_queue.json
  where every clip has "series": "fastest_timeline"
- python pipeline.py <url> (no --series) produces clips with "series": null
- python pipeline.py --help shows --series in usage
- No other behavior changes
```
