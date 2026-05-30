from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    higgsfield_api_key: str = ""
    higgsfield_base_url: str = "https://api.higgsfield.ai/v1"

    twitter_client_id: str = ""
    twitter_client_secret: str = ""
    twitter_redirect_uri: str = "http://localhost:8000/api/social/twitter/callback"

    google_client_id: str = ""
    google_client_secret: str = ""
    google_redirect_uri: str = "http://localhost:8000/api/social/youtube/callback"

    tiktok_client_key: str = ""
    tiktok_client_secret: str = ""
    tiktok_redirect_uri: str = "http://localhost:8000/api/social/tiktok/callback"

    secret_key: str = "dev-secret-key-change-me"
    database_url: str = "sqlite:///./dashboard/data/higgsfield.db"
    clips_json_path: str = "./clips.json"
    app_env: str = "development"

    @property
    def mock_mode(self) -> bool:
        return self.app_env == "development" and self.higgsfield_api_key.startswith("test_")


cfg = Config()
