import json
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from dashboard.config import cfg
from dashboard.database import get_db
from dashboard.models import Setting, SocialAccount
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="dashboard/templates")


def _get(db: Session, key: str, default: str = "") -> str:
    row = db.query(Setting).filter_by(key=key).first()
    return row.value if row else default


def _set(db: Session, key: str, value: str):
    row = db.query(Setting).filter_by(key=key).first()
    if row:
        row.value = value
    else:
        db.add(Setting(key=key, value=value))
    db.commit()


@router.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request, db: Session = Depends(get_db)):
    accounts = {a.platform: a for a in db.query(SocialAccount).all()}
    return templates.TemplateResponse(
        request,
        "settings.html",
        {
            "higgsfield_key_set": bool(cfg.higgsfield_api_key and not cfg.higgsfield_api_key.startswith("your_")),
            "mock_mode": cfg.mock_mode,
            "accounts": accounts,
        },
    )


@router.get("/api/settings")
async def get_settings(db: Session = Depends(get_db)):
    rows = db.query(Setting).all()
    return {r.key: r.value for r in rows}


@router.post("/api/settings")
async def update_setting(
    key: str = Form(...),
    value: str = Form(...),
    db: Session = Depends(get_db),
):
    _set(db, key, value)
    return {"ok": True, "key": key}


# ── Social OAuth ──────────────────────────────────────────────────────────────

@router.get("/api/social/twitter/auth")
async def twitter_auth():
    import tweepy
    oauth2_user_handler = tweepy.OAuth2UserHandler(
        client_id=cfg.twitter_client_id,
        redirect_uri=cfg.twitter_redirect_uri,
        scope=["tweet.read", "tweet.write", "users.read", "offline.access"],
        client_secret=cfg.twitter_client_secret,
    )
    url = oauth2_user_handler.get_authorization_url()
    return RedirectResponse(url)


@router.get("/api/social/twitter/callback")
async def twitter_callback(code: str, state: str, db: Session = Depends(get_db)):
    import tweepy
    oauth2_user_handler = tweepy.OAuth2UserHandler(
        client_id=cfg.twitter_client_id,
        redirect_uri=cfg.twitter_redirect_uri,
        scope=["tweet.read", "tweet.write", "users.read", "offline.access"],
        client_secret=cfg.twitter_client_secret,
    )
    token = oauth2_user_handler.fetch_token(f"{cfg.twitter_redirect_uri}?code={code}&state={state}")
    client = tweepy.Client(access_token=token["access_token"])
    me = client.get_me()
    handle = me.data.username if me.data else "unknown"

    account = db.query(SocialAccount).filter_by(platform="twitter").first()
    if not account:
        account = SocialAccount(platform="twitter")
        db.add(account)
    account.account_handle = handle
    account.access_token = token["access_token"]
    account.refresh_token = token.get("refresh_token")
    account.connected_at = datetime.utcnow()
    db.commit()
    return RedirectResponse("/settings?connected=twitter")


@router.post("/api/social/{platform}/revoke")
async def revoke_social(platform: str, db: Session = Depends(get_db)):
    account = db.query(SocialAccount).filter_by(platform=platform).first()
    if account:
        db.delete(account)
        db.commit()
    return {"ok": True}


@router.get("/api/social/youtube/auth")
async def youtube_auth():
    from google_auth_oauthlib.flow import Flow
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": cfg.google_client_id,
                "client_secret": cfg.google_client_secret,
                "redirect_uris": [cfg.google_redirect_uri],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=["https://www.googleapis.com/auth/youtube.upload"],
        redirect_uri=cfg.google_redirect_uri,
    )
    url, _ = flow.authorization_url(access_type="offline", include_granted_scopes="true")
    return RedirectResponse(url)


@router.get("/api/social/youtube/callback")
async def youtube_callback(code: str, db: Session = Depends(get_db)):
    from google_auth_oauthlib.flow import Flow
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": cfg.google_client_id,
                "client_secret": cfg.google_client_secret,
                "redirect_uris": [cfg.google_redirect_uri],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=["https://www.googleapis.com/auth/youtube.upload"],
        redirect_uri=cfg.google_redirect_uri,
    )
    flow.fetch_token(code=code)
    creds = flow.credentials

    account = db.query(SocialAccount).filter_by(platform="youtube").first()
    if not account:
        account = SocialAccount(platform="youtube")
        db.add(account)
    account.access_token = creds.token
    account.refresh_token = creds.refresh_token
    account.extra_json = json.dumps({
        "access_token": creds.token,
        "refresh_token": creds.refresh_token,
        "client_id": cfg.google_client_id,
        "client_secret": cfg.google_client_secret,
    })
    account.connected_at = datetime.utcnow()
    db.commit()
    return RedirectResponse("/settings?connected=youtube")
