from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from dashboard.database import get_db
from dashboard.models import Job, Schedule, Setting
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="dashboard/templates")


def _get(db: Session, key: str, default: str = "") -> str:
    row = db.query(Setting).filter_by(key=key).first()
    return row.value if row else default


def _set(db: Session, key: str, value: str):
    row = db.query(Setting).filter_by(key=key).first()
    if row:
        row.value = value
    else:
        db.add(Setting(key=key, value=value))
    db.commit()


@router.get("/pipeline", response_class=HTMLResponse)
async def pipeline_page(request: Request, db: Session = Depends(get_db)):
    from dashboard.services.pipeline import get_log
    settings = {
        "auto_pipeline_enabled": _get(db, "auto_pipeline_enabled", "false"),
        "pipeline_interval_minutes": _get(db, "pipeline_interval_minutes", "60"),
        "pipeline_top_n_clips": _get(db, "pipeline_top_n_clips", "5"),
        "pipeline_min_views": _get(db, "pipeline_min_views", "500000"),
        "default_post_platforms": _get(db, "default_post_platforms", "twitter"),
        "auto_scrape_on_pipeline": _get(db, "auto_scrape_on_pipeline", "false"),
    }
    log = get_log()
    return templates.TemplateResponse(
        request, "pipeline.html", {"settings": settings, "log": log}
    )


@router.get("/api/pipeline/status")
async def pipeline_status(db: Session = Depends(get_db)):
    from dashboard.services.pipeline import get_log
    active_jobs = db.query(Job).filter(Job.status.in_(["submitted", "processing"])).count()
    pending_posts = db.query(Schedule).filter_by(status="pending").count()
    return {
        "enabled": _get(db, "auto_pipeline_enabled") == "true",
        "interval_minutes": int(_get(db, "pipeline_interval_minutes", "60")),
        "active_jobs": active_jobs,
        "pending_posts": pending_posts,
        "log": get_log()[:20],
    }


@router.post("/api/pipeline/enable")
async def enable_pipeline(db: Session = Depends(get_db)):
    _set(db, "auto_pipeline_enabled", "true")
    return {"enabled": True}


@router.post("/api/pipeline/disable")
async def disable_pipeline(db: Session = Depends(get_db)):
    _set(db, "auto_pipeline_enabled", "false")
    return {"enabled": False}


@router.post("/api/pipeline/run_now")
async def run_now():
    import threading
    from dashboard.services.pipeline import run_pipeline_cycle
    threading.Thread(target=run_pipeline_cycle, daemon=True).start()
    return {"ok": True, "message": "Pipeline cycle triggered"}


@router.post("/api/pipeline/settings")
async def update_pipeline_settings(
    request: Request,
    db: Session = Depends(get_db),
):
    form = await request.form()
    allowed = [
        "pipeline_interval_minutes", "pipeline_top_n_clips",
        "pipeline_min_views", "default_post_platforms", "auto_scrape_on_pipeline",
    ]
    for key in allowed:
        if key in form:
            _set(db, key, str(form[key]))
    from dashboard.services.scheduler import reschedule_pipeline
    reschedule_pipeline()
    return {"ok": True}
