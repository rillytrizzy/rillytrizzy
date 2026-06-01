from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from dashboard.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    clip_id = Column(String, nullable=True)
    clip_platform = Column(String, nullable=True)
    clip_url = Column(Text, nullable=True)
    clip_title = Column(String, nullable=True)
    job_type = Column(String, nullable=False)  # text_to_video | clip_transform
    prompt = Column(Text, nullable=True)
    higgsfield_job_id = Column(String, unique=True, nullable=True)
    status = Column(String, nullable=False, default="queued")
    progress_pct = Column(Integer, default=0)
    output_url = Column(Text, nullable=True)
    error_msg = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    schedules = relationship("Schedule", back_populates="job")


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    platform = Column(String, nullable=False)  # twitter | youtube | tiktok
    post_title = Column(String, nullable=True)
    post_caption = Column(Text, nullable=True)
    hashtags = Column(Text, nullable=True)  # JSON array string
    scheduled_at = Column(DateTime, nullable=False)
    status = Column(String, nullable=False, default="pending")  # pending|posting|posted|failed
    post_url = Column(Text, nullable=True)
    error_msg = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    job = relationship("Job", back_populates="schedules")


class SocialAccount(Base):
    __tablename__ = "social_accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    platform = Column(String, nullable=False, unique=True)
    account_handle = Column(String, nullable=True)
    access_token = Column(Text, nullable=True)
    refresh_token = Column(Text, nullable=True)
    token_expiry = Column(DateTime, nullable=True)
    extra_json = Column(Text, nullable=True)  # JSON blob for platform-specific fields
    connected_at = Column(DateTime, default=datetime.utcnow)


class Setting(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String, nullable=False, unique=True)
    value = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
