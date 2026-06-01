from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()


def _safe(fn):
    def wrapper(*args, **kwargs):
        try:
            fn(*args, **kwargs)
        except Exception as e:
            print(f"[scheduler] {fn.__name__} error: {e}")
    wrapper.__name__ = fn.__name__
    return wrapper


def start():
    from dashboard.services.pipeline import (
        execute_due_posts,
        poll_higgsfield_jobs,
        refresh_pipeline_config,
        run_pipeline_cycle,
    )

    scheduler.add_job(_safe(poll_higgsfield_jobs), "interval", seconds=15, id="poll_higgsfield", replace_existing=True)
    scheduler.add_job(_safe(run_pipeline_cycle), "interval", minutes=60, id="pipeline_cycle", replace_existing=True)
    scheduler.add_job(_safe(execute_due_posts), "interval", minutes=2, id="execute_posts", replace_existing=True)
    scheduler.add_job(_safe(refresh_pipeline_config), "interval", minutes=5, id="refresh_config", replace_existing=True)
    scheduler.start()


def stop():
    if scheduler.running:
        scheduler.shutdown(wait=False)


def reschedule_pipeline():
    from dashboard.database import SessionLocal
    from dashboard.models import Setting
    from dashboard.services.pipeline import run_pipeline_cycle

    db = SessionLocal()
    try:
        row = db.query(Setting).filter_by(key="pipeline_interval_minutes").first()
        minutes = int(row.value) if row and row.value else 60
    finally:
        db.close()

    if scheduler.running:
        scheduler.reschedule_job("pipeline_cycle", trigger="interval", minutes=minutes)
