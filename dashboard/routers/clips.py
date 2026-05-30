import json
import os
from typing import Optional

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from dashboard.config import cfg
from dashboard.database import get_db
from dashboard.models import Job
from dashboard.services.higgsfield import get_client

router = APIRouter()
templates = Jinja2Templates(directory="dashboard/templates")


def _load_clips() -> list[dict]:
    path = cfg.clips_json_path
    if not os.path.isabs(path):
        path = os.path.join(os.getcwd(), path.lstrip("./"))
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return []


@router.get("/clips", response_class=HTMLResponse)
async def clips_page(request: Request):
    clips = _load_clips()
    return templates.TemplateResponse(request, "clips.html", {"clips": clips})


@router.get("/api/clips")
async def api_clips(
    platform: Optional[str] = None,
    game: Optional[str] = None,
    min_views: int = 0,
    limit: int = 50,
    offset: int = 0,
):
    clips = _load_clips()
    if platform:
        clips = [c for c in clips if c.get("platform") == platform]
    if game:
        clips = [c for c in clips if game.lower() in (c.get("game") or "").lower()]
    if min_views:
        clips = [c for c in clips if c.get("view_count", 0) >= min_views]
    clips.sort(key=lambda c: c.get("view_count", 0), reverse=True)
    return {"total": len(clips), "clips": clips[offset : offset + limit]}


@router.post("/api/clips/{clip_id}/transform", response_class=HTMLResponse)
async def transform_clip(
    request: Request,
    clip_id: str,
    prompt: str = Form(...),
    style: str = Form("cinematic"),
    db: Session = Depends(get_db),
):
    clips = _load_clips()
    clip = next((c for c in clips if c.get("clip_id") == clip_id), None)
    if not clip:
        return HTMLResponse(f'<p class="text-red-400">Clip {clip_id} not found</p>', status_code=404)

    client = get_client()
    try:
        result = client.submit_clip_transform(clip.get("url", ""), prompt, style)
    except Exception as e:
        return HTMLResponse(f'<p class="text-red-400">Higgsfield error: {e}</p>', status_code=500)

    job = Job(
        clip_id=clip_id,
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
    db.refresh(job)

    return templates.TemplateResponse(request, "job_row.html", {"job": job}, status_code=201)
