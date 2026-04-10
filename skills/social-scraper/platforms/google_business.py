"""
Google Business Profile scraper — browser-free.

Strategy:
  1. Google Maps "place details" via the public maps endpoint
  2. Google Search structured data extraction (Knowledge Panel)

For full API access, set GOOGLE_PLACES_API_KEY in your environment
to use the official Places API.
"""

import json
import logging
import os
import re
from dataclasses import dataclass, asdict, field
from typing import Optional
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

PLACES_KEY = os.environ.get("GOOGLE_PLACES_API_KEY", "")


@dataclass
class GoogleBusinessProfile:
    name: str
    address: str
    phone: str
    website: str
    rating: float
    reviews_count: int
    category: str
    hours: dict = field(default_factory=dict)
    latitude: float = 0.0
    longitude: float = 0.0
    place_id: str = ""
    maps_url: str = ""
    photos_count: int = 0
    description: str = ""
    attributes: list = field(default_factory=list)
    reviews_sample: list = field(default_factory=list)

    def to_dict(self):
        return asdict(self)

    def to_json(self, indent=2):
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


class GoogleBusinessScraper:
    """Scrape Google Business Profile data without a browser."""

    def __init__(self, max_reviews: int = 5):
        self.max_reviews = max_reviews
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        })

    def scrape_profile(self, query: str) -> GoogleBusinessProfile:
        """
        Scrape a Google Business Profile.

        Args:
            query: Business name + location, e.g. "Starbucks Times Square NYC"
                   Or a Google Maps Place ID prefixed with "place_id:"
        """
        if PLACES_KEY:
            try:
                return self._via_places_api(query)
            except Exception as e:
                logger.warning("Places API failed for '%s': %s — trying HTML", query, e)

        return self._via_maps_search(query)

    # ── Official Places API ──────────────────────────────────────

    def _via_places_api(self, query: str) -> GoogleBusinessProfile:
        # Resolve place_id
        if query.startswith("place_id:"):
            place_id = query.replace("place_id:", "").strip()
        else:
            place_id = self._find_place_id(query)

        # Place Details
        url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            "place_id": place_id,
            "fields": (
                "name,formatted_address,formatted_phone_number,website,"
                "rating,user_ratings_total,types,opening_hours,geometry,"
                "photos,editorial_summary,reviews,url"
            ),
            "key": PLACES_KEY,
        }
        resp = self.session.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        if data.get("status") != "OK":
            raise ValueError(f"Places API error: {data.get('status')} — {data.get('error_message', '')}")

        result = data["result"]
        loc = result.get("geometry", {}).get("location", {})
        hours = {}
        oh = result.get("opening_hours", {})
        if oh.get("weekday_text"):
            for line in oh["weekday_text"]:
                parts = line.split(": ", 1)
                if len(parts) == 2:
                    hours[parts[0]] = parts[1]

        reviews = []
        for r in (result.get("reviews") or [])[:self.max_reviews]:
            reviews.append({
                "author": r.get("author_name", ""),
                "rating": r.get("rating", 0),
                "text": (r.get("text") or "")[:500],
                "time": r.get("relative_time_description", ""),
            })

        types = result.get("types", [])
        category = types[0].replace("_", " ").title() if types else ""

        return GoogleBusinessProfile(
            name=result.get("name", ""),
            address=result.get("formatted_address", ""),
            phone=result.get("formatted_phone_number", ""),
            website=result.get("website", ""),
            rating=result.get("rating", 0.0),
            reviews_count=result.get("user_ratings_total", 0),
            category=category,
            hours=hours,
            latitude=loc.get("lat", 0.0),
            longitude=loc.get("lng", 0.0),
            place_id=place_id,
            maps_url=result.get("url", ""),
            photos_count=len(result.get("photos", [])),
            description=(result.get("editorial_summary") or {}).get("overview", ""),
            reviews_sample=reviews,
        )

    def _find_place_id(self, query: str) -> str:
        url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
        params = {
            "input": query,
            "inputtype": "textquery",
            "fields": "place_id",
            "key": PLACES_KEY,
        }
        resp = self.session.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        candidates = data.get("candidates", [])
        if not candidates:
            raise ValueError(f"No Google place found for: {query}")
        return candidates[0]["place_id"]

    # ── HTML fallback (no API key) ───────────────────────────────

    def _via_maps_search(self, query: str) -> GoogleBusinessProfile:
        """
        Search Google Maps and extract business data from the HTML response.
        Limited but functional without API keys.
        """
        search_url = f"https://www.google.com/maps/search/{quote_plus(query)}"
        resp = self.session.get(search_url, timeout=15, allow_redirects=True)
        resp.raise_for_status()

        text = resp.text

        # Google Maps embeds business data in a JS variable.
        # Extract what we can with regex patterns.
        name = self._extract_pattern(r'"([^"]{2,80})",null,null,null,null,null,null,\[\[', text) or query
        address = self._extract_pattern(r'"([\d]+ [^"]{5,120})"', text) or ""
        phone = self._extract_pattern(r'"(\+?[\d\s\-\(\)]{7,20})"', text) or ""
        website = self._extract_pattern(r'"(https?://(?!www\.google)[^"]{5,200})"', text) or ""

        # Rating
        rating = 0.0
        rating_match = re.search(r'(\d+\.\d+),\s*"[\d,]+ review', text)
        if rating_match:
            rating = float(rating_match.group(1))

        reviews_count = 0
        reviews_match = re.search(r'"([\d,]+) reviews?"', text)
        if reviews_match:
            reviews_count = int(reviews_match.group(1).replace(",", ""))

        # Coordinates
        lat, lng = 0.0, 0.0
        coord_match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', resp.url)
        if coord_match:
            lat = float(coord_match.group(1))
            lng = float(coord_match.group(2))

        return GoogleBusinessProfile(
            name=name,
            address=address,
            phone=phone,
            website=website,
            rating=rating,
            reviews_count=reviews_count,
            category="",
            latitude=lat,
            longitude=lng,
            maps_url=resp.url,
            description=f"Scraped via Google Maps search for: {query}",
        )

    @staticmethod
    def _extract_pattern(pattern: str, text: str) -> str:
        match = re.search(pattern, text)
        return match.group(1) if match else ""
