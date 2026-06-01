from typing import Optional

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from dashboard.database import get_db
from dashboard.models import Job
from dashboard.services.higgsfield import get_client
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="dashboard/templates")


@router.get("/jobs", response_class=HTMLResponse)
async def jobs_page(request: Request, db: Session = Depends(get_db)):
    jobs = db.query(Job).order_by(Job.created_at.desc()).all()
    return templates.TemplateResponse(request, "jobs.html", {"jobs": jobs})


@router.get("/api/jobs")
async def api_jobs(
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    q = db.query(Job)
    if status:
        q = q.filter(Job.status == status)
    total = q.count()
    jobs = q.order_by(Job.created_at.desc()).offset(offset).limit(limit).all()
    return {
        "total": total,
        "jobs": [
            {
                "id": j.id,
                "clip_title": j.clip_title,
                "job_type": j.job_type,
                "prompt": j.prompt,
                "status": j.status,
                "progress_pct": j.progress_pct,
                "output_url": j.output_url,
                "created_at": j.created_at.isoformat() if j.created_at else None,
            }
            for j in jobs
        ],
    }


@router.get("/api/jobs/{job_id}/row", response_class=HTMLResponse)
async def job_row(request: Request, job_id: int, db: Session = Depends(get_db)):
    job = db.get(Job, job_id)
    if not job:
        return HTMLResponse("", status_code=404)
    return templates.TemplateResponse(request, "job_row.html", {"job": job})


@router.post("/api/jobs", response_class=HTMLResponse)
async def create_text_to_video_job(
    request: Request,
    prompt: str = Form(...),
    duration_sec: int = Form(4),
    aspect_ratio: str = Form("9:16"),
    db: Session = Depends(get_db),
):
    client = get_client()
    try:
        result = client.submit_text_to_video(prompt, duration_sec, aspect_ratio)
    except Exception as e:
        return HTMLResponse(f'<p class="text-red-400">Error: {e}</p>', status_code=500)

    job = Job(
        job_type="text_to_video",
        prompt=prompt,
        higgsfield_job_id=result.get("job_id"),
        status="submitted",
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return templates.TemplateResponse(request, "job_row.html", {"job": job}, status_code=201)


@router.delete("/api/jobs/{job_id}")
async def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.get(Job, job_id)
    if job:
        db.delete(job)
        db.commit()
    return {"ok": True}


@router.post("/api/jobs/{job_id}/retry", response_class=HTMLResponse)
async def retry_job(request: Request, job_id: int, db: Session = Depends(get_db)):
    job = db.get(Job, job_id)
    if not job or job.status != "failed":
        return HTMLResponse('<p class="text-red-400">Job not found or not failed</p>', status_code=400)

    client = get_client()
    try:
        if job.job_type == "clip_transform":
            result = client.submit_clip_transform(job.clip_url or "", job.prompt or "")
        else:
            result = client.submit_text_to_video(job.prompt or "")
    except Exception as e:
        return HTMLResponse(f'<p class="text-red-400">Error: {e}</p>', status_code=500)

    job.higgsfield_job_id = result.get("job_id")
    job.status = "submitted"
    job.progress_pct = 0
    job.output_url = None
    job.error_msg = None
    db.commit()
    db.refresh(job)
    return templates.TemplateResponse(request, "job_row.html", {"job": job})
