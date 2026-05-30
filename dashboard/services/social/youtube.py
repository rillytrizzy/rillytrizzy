import json
import os


class YouTubePoster:
    def __init__(self, credentials_json: str):
        self._creds_data = json.loads(credentials_json)

    def post_video(
        self,
        video_path: str,
        title: str,
        description: str,
        tags: list[str],
        privacy: str = "public",
    ) -> str:
        try:
            from google.oauth2.credentials import Credentials
            from googleapiclient.discovery import build
            from googleapiclient.http import MediaFileUpload
        except ImportError:
            raise RuntimeError("google-api-python-client is not installed")

        creds = Credentials(
            token=self._creds_data.get("access_token"),
            refresh_token=self._creds_data.get("refresh_token"),
            token_uri="https://oauth2.googleapis.com/token",
            client_id=self._creds_data.get("client_id"),
            client_secret=self._creds_data.get("client_secret"),
        )
        youtube = build("youtube", "v3", credentials=creds)

        body = {
            "snippet": {"title": title, "description": description, "tags": tags},
            "status": {"privacyStatus": privacy},
        }
        media = MediaFileUpload(video_path, mimetype="video/mp4", resumable=True)
        request = youtube.videos().insert(part=",".join(body.keys()), body=body, media_body=media)

        response = None
        while response is None:
            _, response = request.next_chunk()

        video_id = response["id"]
        return f"https://www.youtube.com/watch?v={video_id}"
