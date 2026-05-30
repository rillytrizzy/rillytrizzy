import httpx


class TikTokPoster:
    BASE_URL = "https://open.tiktokapis.com/v2"

    def __init__(self, access_token: str):
        self.access_token = access_token

    def post_video(
        self,
        video_path: str,
        caption: str,
        privacy_level: str = "PUBLIC_TO_EVERYONE",
    ) -> str:
        headers = {"Authorization": f"Bearer {self.access_token}"}
        file_size = None
        import os
        file_size = os.path.getsize(video_path)

        with httpx.Client(timeout=60) as client:
            # Step 1: init upload
            init_resp = client.post(
                f"{self.BASE_URL}/post/publish/video/init/",
                headers=headers,
                json={
                    "post_info": {
                        "title": caption[:150],
                        "privacy_level": privacy_level,
                        "disable_duet": False,
                        "disable_comment": False,
                        "disable_stitch": False,
                    },
                    "source_info": {
                        "source": "FILE_UPLOAD",
                        "video_size": file_size,
                        "chunk_size": file_size,
                        "total_chunk_count": 1,
                    },
                },
            )
            init_resp.raise_for_status()
            data = init_resp.json()["data"]
            upload_url = data["upload_url"]
            publish_id = data["publish_id"]

            # Step 2: upload file
            with open(video_path, "rb") as f:
                video_bytes = f.read()
            put_resp = client.put(
                upload_url,
                content=video_bytes,
                headers={
                    "Content-Type": "video/mp4",
                    "Content-Range": f"bytes 0-{file_size - 1}/{file_size}",
                },
            )
            put_resp.raise_for_status()

            # Step 3: poll for publish status
            import time
            for _ in range(20):
                time.sleep(3)
                status_resp = client.post(
                    f"{self.BASE_URL}/post/publish/status/fetch/",
                    headers=headers,
                    json={"publish_id": publish_id},
                )
                status_resp.raise_for_status()
                status_data = status_resp.json()["data"]
                if status_data["status"] == "PUBLISH_COMPLETE":
                    video_id = status_data.get("publicaly_available_post_id", [publish_id])[0]
                    return f"https://www.tiktok.com/@me/video/{video_id}"
                if status_data["status"] in ("FAILED", "SPAM_RISK_TOO_MANY_POSTS"):
                    raise RuntimeError(f"TikTok publish failed: {status_data}")

        raise RuntimeError("TikTok publish timed out")
