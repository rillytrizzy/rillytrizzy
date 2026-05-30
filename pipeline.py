#!/usr/bin/env python3
"""
Agent Network Content Pipeline
URL → Download → Clips → Transcribe → Caption/Hashtags → Account-routed review queue

Usage:
    python pipeline.py <video_url>
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
import sys
from datetime import datetime
from pathlib import Path

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
        "niche": "AI, agents, automation, productivity, future of work, tech culture",
        "status": "ACTIVE",
        "default_hashtags": ["#AI", "#AgentMaxxing", "#automation", "#futureofwork", "#tech", "#AIagents"],
    },
    "agent_afterhours": {
        "niche": "EDM, festivals, dance, nightlife, music culture, EDC, AriAtHome",
        "status": "ACTIVE",
        "default_hashtags": ["#EDM", "#festivals", "#AgentAfterHours", "#nightlife", "#EDC", "#dance"],
    },
    "agent_pastforward": {
        "niche": "history, forgotten technology, old predictions, future forecasting, timelines",
        "status": "RESERVED",
        "default_hashtags": ["#history", "#AgentPastForward", "#technology", "#futureforecasting"],
    },
    "agent_viral": {
        "niche": "viral clips, entertaining content, broad reach",
        "status": "RESERVED",
        "default_hashtags": ["#viral", "#AgentViral", "#fyp", "#trending"],
    },
    "agent_trending": {
        "niche": "current trends, internet culture, news-driven social content",
        "status": "RESERVED",
        "default_hashtags": ["#trending", "#AgentTrending", "#internetculture", "#news"],
    },
}

ACTIVE_ACCOUNTS = [k for k, v in ACCOUNT_PROFILES.items() if v["status"] == "ACTIVE"]

# Low-confidence threshold — clips below this are flagged for manual review
CONFIDENCE_THRESHOLD = 0.70


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
        result = subprocess.run(cmd, capture_output=True)

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
# Step 4: Metadata generation (Claude — caption, hashtags, account routing)
# ---------------------------------------------------------------------------

def generate_metadata(transcript: str, source_title: str, source_url: str) -> dict:
    """
    Use Claude to generate caption, hashtags, and route clip to the correct
    ACTIVE account. Returns dict with keys: account, hook, caption, hashtags,
    confidence.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        # Fallback: route to first active account with defaults
        account = ACTIVE_ACCOUNTS[0]
        return {
            "account": account,
            "hook": source_title[:100],
            "caption": source_title,
            "hashtags": ACCOUNT_PROFILES[account]["default_hashtags"],
            "confidence": 0.0,
        }

    client = Anthropic(api_key=api_key)

    account_descriptions = "\n".join(
        f"  {name} [{profile['status']}]: {profile['niche']}"
        for name, profile in ACCOUNT_PROFILES.items()
    )

    prompt = f"""You are routing content for the Agent Network — a group of sibling social media brands.

Source: {source_title}
URL: {source_url}

Clip transcript:
{transcript or "(no transcript available — use source title to infer content)"}

Accounts (route ONLY to ACTIVE accounts):
{account_descriptions}

Your tasks:
1. ROUTE — Pick the single best ACTIVE account for this clip.
2. HOOK — One sentence, under 100 characters, for the first 3 seconds of the post.
3. CAPTION — Post caption, 150–250 characters, no hashtags.
4. HASHTAGS — 6–8 relevant hashtags for the chosen account.
5. CONFIDENCE — Float 0.0–1.0. Low confidence (<0.7) = content is ambiguous.

Reply with valid JSON only, no markdown fences:
{{"account":"agent_maxxing","hook":"...","caption":"...","hashtags":["#tag"],"confidence":0.85}}"""

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

    # Safety: never route to RESERVED accounts
    if data.get("account") not in ACTIVE_ACCOUNTS:
        data["account"] = ACTIVE_ACCOUNTS[0]
        data["confidence"] = 0.0

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

def run_pipeline(url: str, output_root: Path, clip_duration: int = 45) -> dict:
    """
    Full pipeline: URL → account-routed review queue.
    Returns the review queue manifest dict.
    """
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
        meta = generate_metadata(transcript, video_path.stem, url)

        account = meta["account"]
        confidence = meta.get("confidence", 0.0)
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
            "approved": False,  # humans set this to true before publishing
        })

        flag = " ⚑ LOW CONFIDENCE" if needs_review else ""
        print(f"      {clip.name} → @{account} ({confidence:.0%}){flag}")

    # 5. Write review queue
    print("[4/4] Writing review queue...")
    manifest_path = build_review_queue(run_dir, url, video_path, clip_results)

    # Summary
    by_account: dict[str, int] = {}
    for r in clip_results:
        by_account[r["account"]] = by_account.get(r["account"], 0) + 1

    flagged = sum(1 for r in clip_results if r["needs_review"])
    routing_summary = "  ".join(f"@{a}: {n}" for a, n in by_account.items())

    print(f"\n Done — {run_dir}")
    print(f"  {len(clips)} clips  {routing_summary}")
    if flagged:
        print(f"  ⚑ {flagged} clip(s) flagged for manual review")
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
  python pipeline.py https://www.tiktok.com/@user/video/... --clip-duration 30
  python pipeline.py <url> --output runs/
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

    run_pipeline(args.url, Path(args.output), args.clip_duration)


if __name__ == "__main__":
    main()
