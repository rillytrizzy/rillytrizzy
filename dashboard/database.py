from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from dashboard.config import cfg

engine = create_engine(cfg.database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    from dashboard import models  # noqa: F401 — ensures models are registered
    Base.metadata.create_all(bind=engine)
    _seed_settings()


def _seed_settings():
    from dashboard.models import Setting

    db = SessionLocal()
    defaults = {
        "auto_pipeline_enabled": "false",
        "pipeline_interval_minutes": "60",
        "pipeline_top_n_clips": "5",
        "pipeline_min_views": "500000",
        "pipeline_platforms": "twitch,kick,youtube",
        "default_post_platforms": "twitter",
        "auto_scrape_on_pipeline": "false",
        "clips_json_path": "./clips.json",
    }
    for key, value in defaults.items():
        if not db.query(Setting).filter_by(key=key).first():
            db.add(Setting(key=key, value=value))
    db.commit()
    db.close()
