import time
import uuid
from typing import Optional

import requests

from dashboard.config import cfg

_MOCK_JOBS: dict[str, dict] = {}


class HiggsfieldClient:
    def __init__(self):
        self.api_key = cfg.higgsfield_api_key
        self.base_url = cfg.higgsfield_base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(
            {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        )

    def _is_mock(self) -> bool:
        return cfg.mock_mode

    def submit_text_to_video(
        self, prompt: str, duration_sec: int = 4, aspect_ratio: str = "9:16"
    ) -> dict:
        if self._is_mock():
            return self._mock_submit(prompt)
        resp = self.session.post(
            f"{self.base_url}/generations/text-to-video",
            json={"prompt": prompt, "duration": duration_sec, "aspect_ratio": aspect_ratio},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    def submit_clip_transform(
        self, clip_url: str, prompt: str, style: str = "cinematic"
    ) -> dict:
        if self._is_mock():
            return self._mock_submit(prompt)
        resp = self.session.post(
            f"{self.base_url}/generations/video-to-video",
            json={"video_url": clip_url, "prompt": prompt, "style": style},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    def get_job_status(self, job_id: str) -> dict:
        if self._is_mock():
            return self._mock_status(job_id)
        resp = self.session.get(f"{self.base_url}/generations/{job_id}", timeout=15)
        resp.raise_for_status()
        return resp.json()

    def list_videos(self, limit: int = 20, offset: int = 0) -> list:
        if self._is_mock():
            done = [j for j in _MOCK_JOBS.values() if j["status"] == "done"]
            return done[offset : offset + limit]
        resp = self.session.get(
            f"{self.base_url}/generations", params={"limit": limit, "offset": offset}, timeout=15
        )
        resp.raise_for_status()
        return resp.json()

    def download_video(self, output_url: str, dest_path: str) -> str:
        r = requests.get(output_url, stream=True, timeout=60)
        r.raise_for_status()
        with open(dest_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        return dest_path

    # ── mock helpers ─────────────────────────────────────────────────────────

    def _mock_submit(self, prompt: str) -> dict:
        job_id = f"mock_{uuid.uuid4().hex[:8]}"
        _MOCK_JOBS[job_id] = {
            "job_id": job_id,
            "status": "processing",
            "progress": 0,
            "output_url": None,
            "error": None,
            "created_at": time.time(),
            "prompt": prompt,
        }
        return {"job_id": job_id, "status": "processing"}

    def _mock_status(self, job_id: str) -> dict:
        if job_id not in _MOCK_JOBS:
            return {"job_id": job_id, "status": "failed", "progress": 0, "output_url": None, "error": "not found"}
        job = _MOCK_JOBS[job_id]
        elapsed = time.time() - job["created_at"]
        # Simulate ~30s processing
        progress = min(100, int(elapsed / 30 * 100))
        if progress >= 100:
            job["status"] = "done"
            job["progress"] = 100
            job["output_url"] = (
                "https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4"
            )
        else:
            job["status"] = "processing"
            job["progress"] = progress
        return {
            "job_id": job_id,
            "status": job["status"],
            "progress": job["progress"],
            "output_url": job["output_url"],
            "error": job["error"],
        }


def get_client() -> HiggsfieldClient:
    return HiggsfieldClient()
