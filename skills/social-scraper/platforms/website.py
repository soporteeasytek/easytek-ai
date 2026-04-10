"""
Generic website scraper — browser-free.

Extracts structured profile/business data from any website:
  - Meta tags (Open Graph, Twitter Cards, standard)
  - JSON-LD structured data (Schema.org)
  - Contact info (email, phone, social links)
  - RSS/sitemap discovery
"""

import json
import logging
import re
from dataclasses import dataclass, asdict, field
from typing import Optional
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


@dataclass
class WebsiteProfile:
    url: str
    title: str
    description: str
    og_image: str
    language: str
    favicon: str
    emails: list = field(default_factory=list)
    phones: list = field(default_factory=list)
    social_links: dict = field(default_factory=dict)
    meta_tags: dict = field(default_factory=dict)
    structured_data: list = field(default_factory=list)
    technologies: list = field(default_factory=list)
    rss_feeds: list = field(default_factory=list)

    def to_dict(self):
        return asdict(self)

    def to_json(self, indent=2):
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


# Known social media domains → platform name
_SOCIAL_DOMAINS = {
    "facebook.com": "facebook",
    "fb.com": "facebook",
    "instagram.com": "instagram",
    "twitter.com": "twitter",
    "x.com": "twitter",
    "linkedin.com": "linkedin",
    "youtube.com": "youtube",
    "tiktok.com": "tiktok",
    "pinterest.com": "pinterest",
    "github.com": "github",
    "t.me": "telegram",
    "wa.me": "whatsapp",
}


class WebsiteScraper:
    """Extract profile and business data from any public website."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,es;q=0.8",
        })

    def scrape_profile(self, url: str) -> WebsiteProfile:
        """
        Scrape structured data from a website.

        Args:
            url: Full URL, e.g. "https://example.com"
        """
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        resp = self.session.get(url, timeout=15, allow_redirects=True)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "lxml")
        base_url = resp.url

        title = self._get_title(soup)
        description = self._get_description(soup)
        og_image = self._get_og_image(soup, base_url)
        language = self._get_language(soup)
        favicon = self._get_favicon(soup, base_url)
        meta_tags = self._get_meta_tags(soup)
        structured_data = self._get_json_ld(soup)
        emails = self._find_emails(resp.text)
        phones = self._find_phones(resp.text)
        social_links = self._find_social_links(soup, base_url)
        technologies = self._detect_technologies(resp.text, resp.headers)
        rss_feeds = self._find_rss(soup, base_url)

        return WebsiteProfile(
            url=base_url,
            title=title,
            description=description,
            og_image=og_image,
            language=language,
            favicon=favicon,
            emails=emails,
            phones=phones,
            social_links=social_links,
            meta_tags=meta_tags,
            structured_data=structured_data,
            technologies=technologies,
            rss_feeds=rss_feeds,
        )

    # ── Extraction helpers ───────────────────────────────────────

    @staticmethod
    def _get_title(soup: BeautifulSoup) -> str:
        og = soup.find("meta", property="og:title")
        if og and og.get("content"):
            return og["content"].strip()
        if soup.title and soup.title.string:
            return soup.title.string.strip()
        return ""

    @staticmethod
    def _get_description(soup: BeautifulSoup) -> str:
        for attr in [{"property": "og:description"}, {"name": "description"}]:
            tag = soup.find("meta", attrs=attr)
            if tag and tag.get("content"):
                return tag["content"].strip()[:1000]
        return ""

    @staticmethod
    def _get_og_image(soup: BeautifulSoup, base: str) -> str:
        tag = soup.find("meta", property="og:image")
        if tag and tag.get("content"):
            return urljoin(base, tag["content"])
        return ""

    @staticmethod
    def _get_language(soup: BeautifulSoup) -> str:
        html_tag = soup.find("html")
        if html_tag:
            return html_tag.get("lang", "").strip()
        return ""

    @staticmethod
    def _get_favicon(soup: BeautifulSoup, base: str) -> str:
        for rel in ["icon", "shortcut icon", "apple-touch-icon"]:
            link = soup.find("link", rel=lambda r: r and rel in (r if isinstance(r, list) else [r]))
            if link and link.get("href"):
                return urljoin(base, link["href"])
        return urljoin(base, "/favicon.ico")

    @staticmethod
    def _get_meta_tags(soup: BeautifulSoup) -> dict:
        tags = {}
        for meta in soup.find_all("meta"):
            key = meta.get("property") or meta.get("name")
            val = meta.get("content")
            if key and val:
                tags[key] = val[:500]
        return tags

    @staticmethod
    def _get_json_ld(soup: BeautifulSoup) -> list:
        results = []
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(script.string or "")
                if isinstance(data, list):
                    results.extend(data)
                elif isinstance(data, dict):
                    results.append(data)
            except (json.JSONDecodeError, TypeError):
                continue
        return results

    @staticmethod
    def _find_emails(text: str) -> list:
        pattern = r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}'
        emails = list(set(re.findall(pattern, text)))
        # Filter out common false positives
        skip = {"woff2", "woff", "png", "jpg", "gif", "svg", "css", "js"}
        return [e for e in emails if not any(e.endswith(f".{s}") for s in skip)][:20]

    @staticmethod
    def _find_phones(text: str) -> list:
        patterns = [
            r'\+?\d{1,3}[\s\-]?\(?\d{2,4}\)?[\s\-]?\d{3,4}[\s\-]?\d{3,4}',
            r'\(\d{2,4}\)\s?\d{3,4}[\-\s]?\d{4}',
        ]
        phones = set()
        for p in patterns:
            for match in re.findall(p, text):
                cleaned = re.sub(r'[^\d+]', '', match)
                if 7 <= len(cleaned) <= 15:
                    phones.add(match.strip())
        return list(phones)[:10]

    @staticmethod
    def _find_social_links(soup: BeautifulSoup, base: str) -> dict:
        social = {}
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            if not href.startswith("http"):
                href = urljoin(base, href)
            parsed = urlparse(href)
            domain = parsed.netloc.lower().replace("www.", "")
            for sd, name in _SOCIAL_DOMAINS.items():
                if domain == sd or domain.endswith("." + sd):
                    if name not in social:
                        social[name] = href
                    break
        return social

    @staticmethod
    def _detect_technologies(text: str, headers: dict) -> list:
        techs = []
        checks = {
            "WordPress": ["wp-content", "wp-includes"],
            "Shopify": ["cdn.shopify.com", "Shopify.theme"],
            "React": ["react", "__NEXT_DATA__", "_next/"],
            "Vue.js": ["vue.js", "__vue__"],
            "Angular": ["ng-version", "angular"],
            "Bootstrap": ["bootstrap.min.css", "bootstrap.min.js"],
            "Tailwind CSS": ["tailwindcss", "tailwind"],
            "jQuery": ["jquery.min.js", "jquery/"],
            "Google Analytics": ["google-analytics.com", "gtag("],
            "Google Tag Manager": ["googletagmanager.com"],
            "Cloudflare": ["cloudflare"],
            "Wix": ["wix.com", "parastorage.com"],
            "Squarespace": ["squarespace.com", "sqsp.net"],
        }
        server = headers.get("server", "").lower()
        if "nginx" in server:
            techs.append("Nginx")
        if "apache" in server:
            techs.append("Apache")

        text_lower = text.lower()
        for tech, indicators in checks.items():
            if any(ind.lower() in text_lower for ind in indicators):
                techs.append(tech)

        return techs

    @staticmethod
    def _find_rss(soup: BeautifulSoup, base: str) -> list:
        feeds = []
        for link in soup.find_all("link", type=re.compile(r"(rss|atom)", re.I)):
            href = link.get("href")
            if href:
                feeds.append(urljoin(base, href))
        return feeds
