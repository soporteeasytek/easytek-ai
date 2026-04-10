"""
Facebook page / profile scraper — browser-free.

Strategy:
  1. Graph API (if FACEBOOK_ACCESS_TOKEN is set) — most reliable
  2. Public page HTML scraping fallback (limited data)

Note: Personal profiles are heavily restricted. This works best with
public Facebook Pages (businesses, creators, public figures).
"""

import json
import logging
import os
import re
from dataclasses import dataclass, asdict, field
from typing import Optional

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

FB_TOKEN = os.environ.get("FACEBOOK_ACCESS_TOKEN", "")


@dataclass
class FacebookProfile:
    page_id: str
    name: str
    category: str
    description: str
    about: str
    followers: int
    likes: int
    website: str
    phone: str
    email: str
    address: str
    profile_url: str
    profile_pic_url: str = ""
    is_verified: bool = False
    hours: dict = field(default_factory=dict)
    recent_posts: list = field(default_factory=list)

    def to_dict(self):
        return asdict(self)

    def to_json(self, indent=2):
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


class FacebookScraper:
    """Scrape Facebook public pages without a browser."""

    def __init__(self, max_posts: int = 10):
        self.max_posts = max_posts
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        })

    def scrape_profile(self, page_id_or_slug: str) -> FacebookProfile:
        """
        Scrape a public Facebook page.

        Args:
            page_id_or_slug: Numeric page ID or vanity slug
                             e.g. "cocacola" or "123456789"
        """
        if FB_TOKEN:
            try:
                return self._via_graph_api(page_id_or_slug)
            except Exception as e:
                logger.warning("Graph API failed for %s: %s — trying HTML", page_id_or_slug, e)

        return self._via_html(page_id_or_slug)

    # ── Graph API (requires access token) ────────────────────────

    def _via_graph_api(self, page_id: str) -> FacebookProfile:
        fields = (
            "id,name,category,description,about,fan_count,followers_count,"
            "website,phone,emails,single_line_address,verification_status,"
            "hours,picture.type(large),link"
        )
        url = f"https://graph.facebook.com/v19.0/{page_id}"
        params = {"fields": fields, "access_token": FB_TOKEN}

        resp = self.session.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        if "error" in data:
            raise ValueError(data["error"].get("message", "Unknown Graph API error"))

        # Fetch recent posts
        posts = []
        posts_url = f"https://graph.facebook.com/v19.0/{page_id}/posts"
        posts_params = {
            "fields": "message,created_time,shares,permalink_url",
            "limit": self.max_posts,
            "access_token": FB_TOKEN,
        }
        presp = self.session.get(posts_url, params=posts_params, timeout=15)
        if presp.status_code == 200:
            for p in (presp.json().get("data") or []):
                posts.append({
                    "message": (p.get("message") or "")[:500],
                    "created_time": p.get("created_time", ""),
                    "shares": (p.get("shares") or {}).get("count", 0),
                    "url": p.get("permalink_url", ""),
                })

        emails = data.get("emails") or []
        pic = (data.get("picture") or {}).get("data", {}).get("url", "")

        return FacebookProfile(
            page_id=data.get("id", page_id),
            name=data.get("name", ""),
            category=data.get("category", ""),
            description=data.get("description", ""),
            about=data.get("about", ""),
            followers=data.get("followers_count", 0),
            likes=data.get("fan_count", 0),
            website=data.get("website", ""),
            phone=data.get("phone", ""),
            email=emails[0] if emails else "",
            address=data.get("single_line_address", ""),
            profile_url=data.get("link", f"https://www.facebook.com/{page_id}"),
            profile_pic_url=pic,
            is_verified=data.get("verification_status") == "blue_verified",
            hours=data.get("hours", {}),
            recent_posts=posts,
        )

    # ── HTML fallback (no auth) ──────────────────────────────────

    def _via_html(self, page_slug: str) -> FacebookProfile:
        """
        Scrape basic info from a public Facebook page via HTML.
        Facebook heavily obfuscates its HTML, so this extracts
        what's available from meta tags and structured data.
        """
        url = f"https://www.facebook.com/{page_slug}/"
        resp = self.session.get(url, timeout=15, allow_redirects=True)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "lxml")

        # Extract from Open Graph meta tags
        og = {}
        for meta in soup.find_all("meta", attrs={"property": True}):
            prop = meta.get("property", "")
            if prop.startswith("og:"):
                og[prop] = meta.get("content", "")

        # Extract from JSON-LD structured data
        name = og.get("og:title", "")
        description = og.get("og:description", "")
        profile_pic = og.get("og:image", "")
        profile_url = og.get("og:url", f"https://www.facebook.com/{page_slug}")

        # Try to find follower counts in page source
        followers = 0
        likes = 0
        followers_match = re.search(r'"followers_count":(\d+)', resp.text)
        likes_match = re.search(r'"fan_count":(\d+)', resp.text)
        if followers_match:
            followers = int(followers_match.group(1))
        if likes_match:
            likes = int(likes_match.group(1))

        # Try JSON-LD
        address = ""
        phone = ""
        website = ""
        category = ""
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                ld = json.loads(script.string or "")
                if isinstance(ld, dict):
                    address = self._extract_address(ld)
                    phone = ld.get("telephone", "")
                    website = ld.get("url", "")
                    category = ld.get("@type", "")
            except (json.JSONDecodeError, TypeError):
                continue

        return FacebookProfile(
            page_id=page_slug,
            name=name,
            category=category,
            description=description,
            about="",
            followers=followers,
            likes=likes,
            website=website,
            phone=phone,
            email="",
            address=address,
            profile_url=profile_url,
            profile_pic_url=profile_pic,
        )

    @staticmethod
    def _extract_address(ld: dict) -> str:
        addr = ld.get("address", {})
        if isinstance(addr, dict):
            parts = [
                addr.get("streetAddress", ""),
                addr.get("addressLocality", ""),
                addr.get("addressRegion", ""),
                addr.get("postalCode", ""),
                addr.get("addressCountry", ""),
            ]
            return ", ".join(p for p in parts if p)
        return str(addr) if addr else ""
