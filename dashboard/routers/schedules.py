import json
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from dashboard.database import get_db
from dashboard.models import Job, Schedule
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="dashboard/templates")


@router.get("/schedules", response_class=HTMLResponse)
async def schedules_page(request: Request, db: Session = Depends(get_db)):
    schedules = db.query(Schedule).order_by(Schedule.scheduled_at.desc()).all()
    done_jobs = db.query(Job).filter(Job.status == "done").order_by(Job.created_at.desc()).all()
    return templates.TemplateResponse(
        request, "schedules.html", {"schedules": schedules, "done_jobs": done_jobs}
    )


@router.get("/api/schedules")
async def api_schedules(
    status: Optional[str] = None,
    platform: Optional[str] = None,
    db: Session = Depends(get_db),
):
    q = db.query(Schedule)
    if status:
        q = q.filter(Schedule.status == status)
    if platform:
        q = q.filter(Schedule.platform == platform)
    items = q.order_by(Schedule.scheduled_at).all()
    return [
        {
            "id": s.id,
            "job_id": s.job_id,
            "platform": s.platform,
            "post_caption": s.post_caption,
            "scheduled_at": s.scheduled_at.isoformat() if s.scheduled_at else None,
            "status": s.status,
            "post_url": s.post_url,
        }
        for s in items
    ]


@router.post("/api/schedules")
async def create_schedule(
    job_id: int = Form(...),
    platform: str = Form(...),
    post_caption: str = Form(""),
    post_title: str = Form(""),
    hashtags: str = Form("[]"),
    scheduled_at: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        dt = datetime.fromisoformat(scheduled_at)
    except ValueError:
        return {"error": "Invalid scheduled_at format, use ISO 8601"}

    sched = Schedule(
        job_id=job_id,
        platform=platform,
        post_title=post_title,
        post_caption=post_caption,
        hashtags=hashtags,
        scheduled_at=dt,
    )
    db.add(sched)
    db.commit()
    db.refresh(sched)
    return {"id": sched.id, "status": sched.status}


@router.delete("/api/schedules/{schedule_id}")
async def cancel_schedule(schedule_id: int, db: Session = Depends(get_db)):
    sched = db.get(Schedule, schedule_id)
    if sched and sched.status == "pending":
        sched.status = "failed"
        sched.error_msg = "Cancelled by user"
        db.commit()
    return {"ok": True}


@router.post("/api/schedules/{schedule_id}/trigger")
async def trigger_schedule(schedule_id: int, db: Session = Depends(get_db)):
    sched = db.get(Schedule, schedule_id)
    if not sched:
        return {"error": "Not found"}
    if sched.status not in ("pending", "failed"):
        return {"error": f"Cannot trigger schedule with status {sched.status}"}

    sched.status = "posting"
    db.commit()
    try:
        from dashboard.services.social import post_to_platform
        url = post_to_platform(sched)
        sched.status = "posted"
        sched.post_url = url
        db.commit()
        return {"ok": True, "post_url": url}
    except Exception as e:
        sched.status = "failed"
        sched.error_msg = str(e)
        db.commit()
        return {"error": str(e)}
