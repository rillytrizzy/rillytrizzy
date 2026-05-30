import json
import os

import requests

from dashboard.database import SessionLocal
from dashboard.models import Schedule, SocialAccount


def download_video_to_temp(url: str, job_id: int) -> str:
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    videos_dir = os.path.join(base, "dashboard", "data", "videos")
    os.makedirs(videos_dir, exist_ok=True)
    dest = os.path.join(videos_dir, f"job_{job_id}.mp4")
    if os.path.exists(dest):
        return dest
    r = requests.get(url, stream=True, timeout=120)
    r.raise_for_status()
    with open(dest, "wb") as f:
        for chunk in r.iter_content(chunk_size=65536):
            f.write(chunk)
    return dest


def post_to_platform(schedule: Schedule) -> str:
    db = SessionLocal()
    try:
        account = db.query(SocialAccount).filter_by(platform=schedule.platform).first()
        if not account:
            raise RuntimeError(f"No connected {schedule.platform} account")

        job = schedule.job
        video_path = download_video_to_temp(job.output_url, job.id)
        hashtags = json.loads(schedule.hashtags or "[]")

        if schedule.platform == "twitter":
            from dashboard.services.social.twitter import TwitterPoster
            extra = json.loads(account.extra_json or "{}")
            poster = TwitterPoster(account.access_token, extra.get("access_token_secret"))
            return poster.post_video(video_path, schedule.post_caption or "", hashtags)

        elif schedule.platform == "youtube":
            from dashboard.services.social.youtube import YouTubePoster
            extra = json.loads(account.extra_json or "{}")
            poster = YouTubePoster(json.dumps(extra))
            return poster.post_video(
                video_path,
                title=schedule.post_title or job.clip_title or "Higgsfield clip",
                description=schedule.post_caption or "",
                tags=hashtags,
            )

        elif schedule.platform == "tiktok":
            from dashboard.services.social.tiktok import TikTokPoster
            poster = TikTokPoster(account.access_token)
            return poster.post_video(video_path, schedule.post_caption or "")

        else:
            raise RuntimeError(f"Unknown platform: {schedule.platform}")
    finally:
        db.close()
