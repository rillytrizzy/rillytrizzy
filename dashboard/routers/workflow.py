import json
import os

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from dashboard.config import cfg
from dashboard.database import get_db
from dashboard.models import Job, Schedule, Setting
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="dashboard/templates")


def _clips_count() -> int:
    path = cfg.clips_json_path
    if not os.path.isabs(path):
        path = os.path.join(os.getcwd(), path.lstrip("./"))
    try:
        with open(path) as f:
            return len(json.load(f))
    except Exception:
        return 0


def _workflow_state(db: Session) -> dict:
    clips = _clips_count()
    queued = db.query(Job).filter(Job.status.in_(["queued", "submitted"])).count()
    processing = db.query(Job).filter_by(status="processing").count()
    done = db.query(Job).filter_by(status="done").count()
    failed = db.query(Job).filter_by(status="failed").count()
    pending_posts = db.query(Schedule).filter_by(status="pending").count()
    posted = db.query(Schedule).filter_by(status="posted").count()
    pipeline_on = (
        (db.query(Setting).filter_by(key="auto_pipeline_enabled").first() or Setting(value="false")).value == "true"
    )
    return {
        "clips": clips,
        "queued": queued,
        "processing": processing,
        "done": done,
        "failed": failed,
        "pending_posts": pending_posts,
        "posted": posted,
        "pipeline_on": pipeline_on,
    }


@router.get("/workflow", response_class=HTMLResponse)
async def workflow_page(request: Request, db: Session = Depends(get_db)):
    state = _workflow_state(db)
    return templates.TemplateResponse(request, "workflow.html", {"state": state})


@router.get("/api/workflow/status")
async def workflow_status(db: Session = Depends(get_db)):
    return _workflow_state(db)
