from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from dashboard.database import init_db
from dashboard.routers import clips, jobs, pipeline, schedules, settings
from dashboard.services import scheduler as sched_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    sched_service.start()
    yield
    sched_service.stop()


app = FastAPI(title="Higgsfield Command Center", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="dashboard/static"), name="static")

templates = Jinja2Templates(directory="dashboard/templates")

app.include_router(clips.router)
app.include_router(jobs.router)
app.include_router(schedules.router)
app.include_router(pipeline.router)
app.include_router(settings.router)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    import json, os
    from dashboard.config import cfg
    from dashboard.database import SessionLocal
    from dashboard.models import Job, Schedule, Setting

    db = SessionLocal()
    try:
        total_clips = 0
        clips_path = cfg.clips_json_path
        if not os.path.isabs(clips_path):
            clips_path = os.path.join(os.getcwd(), clips_path.lstrip("./"))
        try:
            with open(clips_path) as f:
                all_clips = json.load(f)
                total_clips = len(all_clips)
                top_clips = sorted(all_clips, key=lambda c: c.get("view_count", 0), reverse=True)[:10]
        except Exception:
            all_clips = []
            top_clips = []

        active_jobs = db.query(Job).filter(Job.status.in_(["submitted", "processing"])).count()
        pending_posts = db.query(Schedule).filter_by(status="pending").count()
        recent_done = db.query(Job).filter_by(status="done").order_by(Job.updated_at.desc()).limit(5).all()
        pipeline_enabled = (db.query(Setting).filter_by(key="auto_pipeline_enabled").first() or Setting(value="false")).value == "true"
    finally:
        db.close()

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "total_clips": total_clips,
            "active_jobs": active_jobs,
            "pending_posts": pending_posts,
            "pipeline_enabled": pipeline_enabled,
            "recent_done": recent_done,
            "top_clips": top_clips,
        },
    )
