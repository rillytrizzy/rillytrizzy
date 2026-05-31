import json
import os
import random
import subprocess
import sys
from datetime import datetime, timedelta

from dashboard.database import SessionLocal
from dashboard.models import Job, Schedule, Setting
from dashboard.services.higgsfield import get_client

_LOG: list[dict] = []  # in-memory activity log (last 100 entries)


def _get_setting(db, key: str, default: str = "") -> str:
    row = db.query(Setting).filter_by(key=key).first()
    return row.value if row else default


def _log(msg: str):
    _LOG.append({"ts": datetime.utcnow().isoformat(), "msg": msg})
    if len(_LOG) > 100:
        _LOG.pop(0)


def get_log() -> list[dict]:
    return list(reversed(_LOG))


def run_pipeline_cycle(force: bool = False):
    db = SessionLocal()
    try:
        enabled = _get_setting(db, "auto_pipeline_enabled", "false")
        if enabled != "true" and not force:
            return

        _log("Pipeline cycle started")

        auto_scrape = _get_setting(db, "auto_scrape_on_pipeline", "false")
        if auto_scrape == "true":
            try:
                import subprocess
                project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                subprocess.run([sys.executable, "scraper.py"], cwd=project_root, timeout=300, check=True)
                _log("Scraper refresh completed")
            except Exception as e:
                _log(f"Scraper refresh failed: {e}")

        clips_path = _get_setting(db, "clips_json_path", "./clips.json")
        if not os.path.isabs(clips_path):
            clips_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))), clips_path.lstrip("./")
            )

        try:
            with open(clips_path) as f:
                clips = json.load(f)
        except Exception as e:
            _log(f"Could not load clips.json: {e}")
            return

        min_views = int(_get_setting(db, "pipeline_min_views", "500000"))
        top_n = int(_get_setting(db, "pipeline_top_n_clips", "5"))

        existing_ids = {j.clip_id for j in db.query(Job).filter(Job.status != "failed").all() if j.clip_id}
        candidates = [
            c for c in clips
            if c.get("view_count", 0) >= min_views and c.get("clip_id") not in existing_ids
        ]
        candidates.sort(key=lambda c: c.get("view_count", 0), reverse=True)
        selected = candidates[:top_n]

        if not selected:
            _log("No new clips meet criteria")
            return

        client = get_client()
        submitted = 0
        for clip in selected:
            prompt = (
                f"Transform this {clip.get('platform', '')} gaming clip into a cinematic "
                "highlight reel with dynamic cuts and epic music."
            )
            try:
                result = client.submit_clip_transform(clip.get("url", ""), prompt)
                job = Job(
                    clip_id=clip.get("clip_id"),
                    clip_platform=clip.get("platform"),
                    clip_url=clip.get("url"),
                    clip_title=clip.get("title"),
                    job_type="clip_transform",
                    prompt=prompt,
                    higgsfield_job_id=result.get("job_id"),
                    status="submitted",
                )
                db.add(job)
                db.commit()
                submitted += 1
            except Exception as e:
                _log(f"Failed to submit clip {clip.get('clip_id')}: {e}")

        _log(f"Pipeline cycle done: {submitted} job(s) submitted from {len(selected)} candidates")

    finally:
        db.close()


def poll_higgsfield_jobs():
    db = SessionLocal()
    try:
        active_jobs = db.query(Job).filter(Job.status.in_(["submitted", "processing"])).all()
        if not active_jobs:
            return

        client = get_client()
        for job in active_jobs:
            if not job.higgsfield_job_id:
                continue
            try:
                result = client.get_job_status(job.higgsfield_job_id)
                job.status = result.get("status", job.status)
                job.progress_pct = result.get("progress", job.progress_pct)
                job.output_url = result.get("output_url") or job.output_url
                job.error_msg = result.get("error") or job.error_msg
                job.updated_at = datetime.utcnow()

                if job.status == "done":
                    _auto_schedule(db, job)
            except Exception as e:
                _log(f"Poll error for job {job.id}: {e}")

        db.commit()
    finally:
        db.close()


def _auto_schedule(db, job: Job):
    enabled = _get_setting(db, "auto_pipeline_enabled", "false")
    if enabled != "true":
        return
    if db.query(Schedule).filter_by(job_id=job.id).first():
        return  # already scheduled

    platforms_str = _get_setting(db, "default_post_platforms", "twitter")
    platforms = [p.strip() for p in platforms_str.split(",") if p.strip()]

    game = ""
    if job.clip_platform:
        game = job.clip_platform
    caption = f"{job.clip_title or 'Gaming clip'} — AI transformed with Higgsfield #gaming #{game}"
    hashtags = json.dumps(["gaming", game] if game else ["gaming"])

    for platform in platforms:
        offset_minutes = random.randint(0, 30)
        sched = Schedule(
            job_id=job.id,
            platform=platform,
            post_title=job.clip_title or "Higgsfield clip",
            post_caption=caption,
            hashtags=hashtags,
            scheduled_at=datetime.utcnow() + timedelta(minutes=offset_minutes),
        )
        db.add(sched)
    db.commit()


def execute_due_posts():
    db = SessionLocal()
    try:
        due = (
            db.query(Schedule)
            .filter(Schedule.status == "pending", Schedule.scheduled_at <= datetime.utcnow())
            .all()
        )
        for sched in due:
            sched.status = "posting"
            db.commit()
            try:
                from dashboard.services.social import post_to_platform
                url = post_to_platform(sched)
                sched.status = "posted"
                sched.post_url = url
                _log(f"Posted to {sched.platform}: {url}")
            except Exception as e:
                sched.status = "failed"
                sched.error_msg = str(e)
                _log(f"Post failed ({sched.platform}): {e}")
            db.commit()
    finally:
        db.close()


def refresh_pipeline_config():
    """Re-read interval from DB and reschedule the pipeline job."""
    from dashboard.services.scheduler import reschedule_pipeline
    reschedule_pipeline()
