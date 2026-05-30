#!/usr/bin/env python3
"""
Agent Network Content Pipeline
URL → Download → Clips → Transcribe → Caption/Hashtags → Account-routed review queue

Usage:
    python pipeline.py <video_url>
    python pipeline.py <video_url> --brands agent_maxxing
    python pipeline.py <video_url> --brands agent_afterhours --series fastest_timeline
    python pipeline.py <video_url> --clip-duration 30 --output my_output/

Requires:
    - ffmpeg installed (system)
    - OPENAI_API_KEY in .env (Whisper transcription)
    - ANTHROPIC_API_KEY in .env (caption + routing via Claude)
"""

import argparse
import json
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import yt_dlp
from anthropic import Anthropic
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# ---------------------------------------------------------------------------
# Account profiles — mirrors BRAND_ARCHITECTURE.md
# ---------------------------------------------------------------------------

ACCOUNT_PROFILES = {
    "agent_maxxing": {
        "niche": "AI tool demos, agent workflows, automation hacks, future-of-work commentary, build logs",
        "pillars": [
            "AI Tool Demos — walkthroughs of new AI tools, agents, and automations",
            "Agent Culture — clips on the agentic AI movement, researchers, founders, builders",
            "Productivity Hacks — workflow automations that save real time (before/after format)",
            "Future-of-Work Commentary — reaction and opinion on AI, jobs, the builder economy",
            "Build Logs — behind-the-scenes of building automation pipelines and AI workflows",
        ],
        "sources": ["youtube_search", "x_embeds", "youtube_channels"],
        "status": "ACTIVE",
        "default_hashtags": ["#AI", "#AgentMaxxing", "#automation", "#futureofwork", "#tech", "#AIagents"],
    },
    "agent_afterhours": {
        "niche": "festival highlights, DJ set clips, music drops, nightlife vibe content, artist spotlights",
        "pillars": [
            "Festival Highlights — best moments from EDC, Ultra, AriAtHome, Coachella, Tomorrowland",
            "DJ Set Clips — 30–60s drop moments, booth angles, crowd reactions",
            "Music Drops & Previews — new track releases, ID reveals, festival previews",
            "Nightlife Culture — vibe content, aesthetic clips, venue visuals, dance floor energy",
            "Artist Spotlights — mini-docs or clip compilations on rising and established artists",
        ],
        "sources": ["youtube_search", "youtube_channels"],
        "status": "ACTIVE",
        "default_hashtags": ["#EDM", "#festivals", "#AgentAfterHours", "#nightlife", "#EDC", "#dance"],
    },
    "agent_viral": {
        "niche": "viral fails, crowd reactions, unexpected moments, trending clips, cross-genre entertainment",
        "pillars": [
            "Top Clips of the Week — curated best-of from Twitch, Kick, YouTube",
            "Reaction Compilations — crowd or audience reaction moments with high shareability",
            "Unexpected Moments — game fails, sports bloopers, live TV mistakes, unexpected wins",
            "Trending Formats — adapt current viral video formats to new content (fast-follow)",
            "Cross-Genre Entertainment — gaming, sports, animals, humans — peak entertainment value",
        ],
        "sources": ["twitch", "kick", "youtube_search"],
        "status": "ACTIVE",
        "default_hashtags": ["#viral", "#AgentViral", "#fyp", "#entertainment"],
    },
    "agent_pastforward": {
        "niche": "historical predictions, forgotten technology, then-vs-now timelines, future forecasting",
        "pillars": [
            "'They Predicted This' — old footage/text predictions shown alongside today's reality",
            "Forgotten Technology — inventions and ideas ahead of their time that failed or vanished",
            "Timeline Comparisons — then vs. now comparisons showing acceleration of change",
            "Future Forecasting — predict what comes next based on historical acceleration patterns",
            "Historical Turning Points — key decisions or events that bent the arc of technology",
        ],
        "sources": ["archive_org", "youtube_search", "wikimedia"],
        "status": "RESERVED",
        "default_hashtags": ["#history", "#AgentPastForward", "#technology", "#futureforecasting"],
    },
    # agent_trending: RETIRED — handle and niche absorbed. Do not route content here.
}

ACTIVE_ACCOUNTS = [k for k, v in ACCOUNT_PROFILES.items() if v["status"] == "ACTIVE"]

# Low-confidence threshold — clips below this are flagged for manual review
CONFIDENCE_THRESHOLD = 0.70

# Music platform domains that signal high copyright risk
MUSIC_DOMAINS = {
    "soundcloud.com", "spotify.com", "bandcamp.com",
    "music.youtube.com", "tidal.com", "deezer.com",
}


# ---------------------------------------------------------------------------
# Step 1: Download
# ---------------------------------------------------------------------------

def download_video(url: str, output_dir: Path) -> Path:
    """Download video from URL via yt-dlp. Returns path to downloaded file."""
    output_dir.mkdir(parents=True, exist_ok=True)

    ydl_opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "outtmpl": str(output_dir / "%(title).80s.%(ext)s"),
        "quiet": True,
        "no_warnings": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    path = Path(filename)
    if not path.exists():
        # yt-dlp may merge to a different extension
        for p in output_dir.iterdir():
            if p.suffix in (".mp4", ".mkv", ".webm"):
                path = p
                break

    return path


# ---------------------------------------------------------------------------
# Step 2: Clip extraction (9:16 vertical, center-cropped)
# ---------------------------------------------------------------------------

def get_duration(video_path: Path) -> float:
    """Return video duration in seconds via ffprobe."""
    result = subprocess.run(
        [
            "ffprobe", "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            str(video_path),
        ],
        capture_output=True,
        text=True,
    )
    return float(json.loads(result.stdout)["format"]["duration"])


def extract_clips(video_path: Path, output_dir: Path, clip_duration: int = 45) -> list[Path]:
    """
    Slice video into fixed-length clips and reformat to 9:16 vertical.
    Source is center-cropped so the subject stays in frame.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    total = get_duration(video_path)
    clips = []

    start = 0
    idx = 0
    while start < total - 10:  # skip trailing segments shorter than 10s
        end = min(start + clip_duration, total)
        clip_path = output_dir / f"clip_{idx:02d}.mp4"

        cmd = [
            "ffmpeg", "-y",
            "-ss", str(start),
            "-i", str(video_path),
            "-t", str(end - start),
            # Center-crop to 9:16, then scale to 1080x1920
            "-vf", "crop=ih*9/16:ih:(iw-ih*9/16)/2:0,scale=1080:1920",
            "-c:v", "libx264", "-crf", "23", "-preset", "fast",
            "-c:a", "aac", "-b:a", "128k",
            "-movflags", "+faststart",
            str(clip_path),
        ]
        subprocess.run(cmd, capture_output=True)

        if clip_path.exists() and clip_path.stat().st_size > 0:
            clips.append(clip_path)

        start += clip_duration
        idx += 1

    return clips


# ---------------------------------------------------------------------------
# Step 3: Transcription (OpenAI Whisper API)
# ---------------------------------------------------------------------------

def transcribe(clip_path: Path) -> str:
    """Transcribe clip audio. Returns empty string if API key not set."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return ""

    client = OpenAI(api_key=api_key)
    with open(clip_path, "rb") as f:
        result = client.audio.transcriptions.create(model="whisper-1", file=f)
    return result.text.strip()


# ---------------------------------------------------------------------------
# Copyright pre-screen
# ---------------------------------------------------------------------------

def check_copyright_risk(url: str, transcript: str = "") -> bool:
    """Pre-screen for copyright risk. Music-domain URLs are high risk by default."""
    domain = urlparse(url).netloc.lower().lstrip("www.")
    if domain in MUSIC_DOMAINS:
        return True
    music_keywords = {"lyrics", "chorus", "verse", "beat drop", "sample", "remix"}
    keyword_hits = sum(1 for kw in music_keywords if kw in transcript.lower())
    return keyword_hits >= 2


# ---------------------------------------------------------------------------
# Step 4: Metadata generation (Claude — caption, hashtags, account routing)
# ---------------------------------------------------------------------------

def generate_metadata(
    transcript: str,
    source_title: str,
    source_url: str,
    accounts: list[str] | None = None,
) -> dict:
    """
    Use Claude to generate caption, hashtags, and route clip to the correct
    account. Returns dict with keys: account, hook, caption, hashtags,
    confidence, copyright_risk.
    """
    route_accounts = accounts if accounts else ACTIVE_ACCOUNTS

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        account = route_accounts[0]
        return {
            "account": account,
            "hook": source_title[:100],
            "caption": source_title,
            "hashtags": ACCOUNT_PROFILES[account]["default_hashtags"],
            "confidence": 0.0,
            "copyright_risk": check_copyright_risk(source_url, transcript),
        }

    client = Anthropic(api_key=api_key)

    account_descriptions = "\n".join(
        "  {name} [{status}]: {niche}\n    Pillars: {pillars}".format(
            name=name,
            status=ACCOUNT_PROFILES[name]["status"],
            niche=ACCOUNT_PROFILES[name]["niche"],
            pillars=" | ".join(ACCOUNT_PROFILES[name].get("pillars", [])),
        )
        for name in route_accounts
        if name in ACCOUNT_PROFILES
    )

    prompt = f"""You are routing content for the Agent Network — a group of sibling social media brands.

Source: {source_title}
URL: {source_url}

Clip transcript:
{transcript or "(no transcript available — use source title to infer content)"}

Accounts (route ONLY to one of these):
{account_descriptions}

Your tasks:
1. ROUTE — Pick the single best account for this clip.
2. HOOK — One sentence, under 100 characters, for the first 3 seconds of the post.
3. CAPTION — Post caption, 150–250 characters, no hashtags.
4. HASHTAGS — 6–8 relevant hashtags for the chosen account.
5. CONFIDENCE — Float 0.0–1.0. Low confidence (<0.7) = content is ambiguous.
6. COPYRIGHT_RISK — true if the clip contains recognizable music, song lyrics, or copyrighted audio. false otherwise.

Reply with valid JSON only, no markdown fences:
{{"account":"agent_maxxing","hook":"...","caption":"...","hashtags":["#tag"],"confidence":0.85,"copyright_risk":false}}"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response.content[0].text.strip()
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        raise ValueError(f"Claude returned non-JSON: {raw}")

    data = json.loads(match.group())

    # Safety: never route to accounts outside the allowed set
    if data.get("account") not in route_accounts:
        data["account"] = route_accounts[0]
        data["confidence"] = 0.0

    # Pre-check can upgrade copyright_risk to true even if Claude said false
    if check_copyright_risk(source_url, transcript):
        data["copyright_risk"] = True
    elif "copyright_risk" not in data:
        data["copyright_risk"] = False

    return data


# ---------------------------------------------------------------------------
# Step 5: Review queue output
# ---------------------------------------------------------------------------

def build_review_queue(
    run_dir: Path,
    source_url: str,
    video_path: Path,
    clip_results: list[dict],
) -> Path:
    """Write review_queue.json — human approval required before publishing."""
    manifest = {
        "run_id": run_dir.name,
        "source_url": source_url,
        "source_video": str(video_path.relative_to(run_dir)),
        "generated_at": datetime.now().isoformat(),
        "governance": "AI assists production. Humans approve publication.",
        "clips": clip_results,
    }
    path = run_dir / "review_queue.json"
    path.write_text(json.dumps(manifest, indent=2))
    return path


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def run_pipeline(
    url: str,
    output_root: Path,
    clip_duration: int = 45,
    brands: list[str] | None = None,
    series: str | None = None,
) -> dict:
    """
    Full pipeline: URL → account-routed review queue.
    Returns the review queue manifest dict.
    """
    # Validate and resolve target accounts
    if brands:
        unknown = [b for b in brands if b not in ACCOUNT_PROFILES]
        if unknown:
            print(f"Warning: unknown brand(s) ignored: {', '.join(unknown)}")
        route_accounts = [b for b in brands if b in ACCOUNT_PROFILES]
        if not route_accounts:
            print("Warning: no valid brands specified — routing to all active accounts")
            route_accounts = ACTIVE_ACCOUNTS
    else:
        route_accounts = ACTIVE_ACCOUNTS

    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = output_root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n Agent Network Pipeline  run {run_id}")
    print(f" Source: {url}\n")

    # 1. Download
    print("[1/4] Downloading...")
    video_path = download_video(url, run_dir / "source")
    print(f"      {video_path.name}")

    # 2. Extract clips
    print(f"[2/4] Extracting {clip_duration}s clips (9:16 vertical)...")
    clips = extract_clips(video_path, run_dir / "clips", clip_duration)
    print(f"      {len(clips)} clip(s) extracted")

    # 3 + 4. Transcribe and generate metadata
    print("[3/4] Transcribing + generating metadata...")
    clip_results = []
    for clip in clips:
        transcript = transcribe(clip)
        meta = generate_metadata(transcript, video_path.stem, url, accounts=route_accounts)

        account = meta["account"]
        confidence = meta.get("confidence", 0.0)
        copyright_risk = meta.get("copyright_risk", False)
        needs_review = confidence < CONFIDENCE_THRESHOLD

        clip_results.append({
            "clip": str(clip.relative_to(run_dir)),
            "account": account,
            "hook": meta.get("hook", ""),
            "caption": meta.get("caption", ""),
            "hashtags": meta.get("hashtags", ACCOUNT_PROFILES[account]["default_hashtags"]),
            "transcript": transcript,
            "confidence": round(confidence, 2),
            "needs_review": needs_review,
            "copyright_risk": copyright_risk,
            "series": series,
            "approved": False,  # humans set this to true before publishing
        })

        flags = []
        if needs_review:
            flags.append("⚑ LOW CONFIDENCE")
        if copyright_risk:
            flags.append("© MUSIC RISK")
        flag_str = "  " + "  ".join(flags) if flags else ""
        print(f"      {clip.name} → @{account} ({confidence:.0%}){flag_str}")

    # 5. Write review queue
    print("[4/4] Writing review queue...")
    manifest_path = build_review_queue(run_dir, url, video_path, clip_results)

    # Summary
    by_account: dict[str, int] = {}
    for r in clip_results:
        by_account[r["account"]] = by_account.get(r["account"], 0) + 1

    flagged = sum(1 for r in clip_results if r["needs_review"])
    music_risk = sum(1 for r in clip_results if r["copyright_risk"])
    routing_summary = "  ".join(f"@{a}: {n}" for a, n in by_account.items())

    print(f"\n Done — {run_dir}")
    print(f"  {len(clips)} clips  {routing_summary}")
    if flagged:
        print(f"  ⚑ {flagged} clip(s) flagged for manual review")
    if music_risk:
        print(f"  © {music_risk} clip(s) flagged for copyright risk")
    print(f"  Review queue: {manifest_path}\n")

    return json.loads(manifest_path.read_text())


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Agent Network Content Pipeline — URL → review queue",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pipeline.py https://www.youtube.com/watch?v=...
  python pipeline.py <url> --brands agent_maxxing
  python pipeline.py <url> --brands agent_afterhours --series fastest_timeline
  python pipeline.py <url> --clip-duration 30 --output runs/
        """,
    )
    parser.add_argument("url", help="Source video URL (YouTube, TikTok, Twitch, Kick, Instagram)")
    parser.add_argument(
        "--clip-duration", type=int, default=45, metavar="SECONDS",
        help="Length of each output clip in seconds (default: 45)",
    )
    parser.add_argument(
        "--output", default="output", metavar="DIR",
        help="Root output directory (default: output/)",
    )
    parser.add_argument(
        "--brands", nargs="+", metavar="BRAND",
        help="Restrict routing to these brand(s) only (default: all active brands)",
    )
    parser.add_argument(
        "--series", default=None, metavar="NAME",
        help='Tag all clips with a series name (e.g., "fastest_timeline")',
    )
    args = parser.parse_args()

    missing = []
    if not os.getenv("OPENAI_API_KEY"):
        missing.append("OPENAI_API_KEY (transcription will be skipped)")
    if not os.getenv("ANTHROPIC_API_KEY"):
        missing.append("ANTHROPIC_API_KEY (routing will use defaults)")
    if missing:
        print("Warning: missing env vars:")
        for m in missing:
            print(f"  - {m}")
        print()

    run_pipeline(args.url, Path(args.output), args.clip_duration, brands=args.brands, series=args.series)


if __name__ == "__main__":
    main()
