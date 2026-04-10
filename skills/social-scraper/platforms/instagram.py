"""
Instagram profile scraper — browser-free.

Uses instaloader for public profile metadata and recent posts.
Falls back to direct HTTP if instaloader is unavailable.
"""

import json
import logging
from dataclasses import dataclass, asdict, field
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class InstagramProfile:
    username: str
    full_name: str
    biography: str
    followers: int
    following: int
    posts_count: int
    is_private: bool
    is_verified: bool
    profile_pic_url: str
    external_url: Optional[str] = None
    recent_posts: list = field(default_factory=list)

    def to_dict(self):
        return asdict(self)

    def to_json(self, indent=2):
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


class InstagramScraper:
    """Scrape Instagram public profiles without a browser."""

    def __init__(self, max_posts: int = 12):
        self.max_posts = max_posts

    def scrape_profile(self, username: str) -> InstagramProfile:
        try:
            return self._via_instaloader(username)
        except Exception as e:
            logger.warning("instaloader failed for %s: %s — trying HTTP", username, e)
            return self._via_http(username)

    # ── instaloader (preferred) ──────────────────────────────────

    def _via_instaloader(self, username: str) -> InstagramProfile:
        import instaloader

        loader = instaloader.Instaloader(
            download_pictures=False,
            download_videos=False,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=False,
            compress_json=False,
            quiet=True,
        )

        profile = instaloader.Profile.from_username(loader.context, username)

        recent_posts = []
        if not profile.is_private:
            for i, post in enumerate(profile.get_posts()):
                if i >= self.max_posts:
                    break
                recent_posts.append({
                    "shortcode": post.shortcode,
                    "caption": (post.caption or "")[:500],
                    "likes": post.likes,
                    "comments": post.comments,
                    "date": post.date_utc.isoformat(),
                    "is_video": post.is_video,
                    "url": f"https://www.instagram.com/p/{post.shortcode}/",
                })

        return InstagramProfile(
            username=profile.username,
            full_name=profile.full_name,
            biography=profile.biography,
            followers=profile.followers,
            following=profile.followees,
            posts_count=profile.mediacount,
            is_private=profile.is_private,
            is_verified=profile.is_verified,
            profile_pic_url=profile.profile_pic_url,
            external_url=profile.external_url,
            recent_posts=recent_posts,
        )

    # ── HTTP fallback ────────────────────────────────────────────

    def _via_http(self, username: str) -> InstagramProfile:
        import requests

        url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            "X-IG-App-ID": "936619743392459",
            "X-Requested-With": "XMLHttpRequest",
        }

        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        user = data.get("data", {}).get("user", {})
        if not user:
            raise ValueError(f"No public data found for @{username}")

        return InstagramProfile(
            username=user.get("username", username),
            full_name=user.get("full_name", ""),
            biography=user.get("biography", ""),
            followers=user.get("edge_followed_by", {}).get("count", 0),
            following=user.get("edge_follow", {}).get("count", 0),
            posts_count=user.get("edge_owner_to_timeline_media", {}).get("count", 0),
            is_private=user.get("is_private", False),
            is_verified=user.get("is_verified", False),
            profile_pic_url=user.get("profile_pic_url_hd", user.get("profile_pic_url", "")),
            external_url=user.get("external_url"),
        )
