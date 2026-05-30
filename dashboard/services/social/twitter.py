import os
from typing import Optional

from dashboard.config import cfg


class TwitterPoster:
    def __init__(self, access_token: str, access_token_secret: Optional[str] = None):
        self.access_token = access_token
        self.access_token_secret = access_token_secret

    def post_video(self, video_path: str, caption: str, hashtags: list[str]) -> str:
        try:
            import tweepy
        except ImportError:
            raise RuntimeError("tweepy is not installed")

        tag_str = " ".join(f"#{t.lstrip('#')}" for t in hashtags)
        full_text = f"{caption}\n{tag_str}".strip()

        # OAuth 1.0a client for media upload (v1.1 endpoint required for media)
        auth = tweepy.OAuth1UserHandler(
            cfg.twitter_client_id,
            cfg.twitter_client_secret,
            self.access_token,
            self.access_token_secret or "",
        )
        api = tweepy.API(auth)
        media = api.chunked_upload(filename=video_path, media_category="tweet_video")

        # Post tweet via API v2
        client = tweepy.Client(
            consumer_key=cfg.twitter_client_id,
            consumer_secret=cfg.twitter_client_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret or "",
        )
        resp = client.create_tweet(text=full_text, media_ids=[media.media_id_string])
        tweet_id = resp.data["id"]
        return f"https://twitter.com/i/web/status/{tweet_id}"
