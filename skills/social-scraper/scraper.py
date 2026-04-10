#!/usr/bin/env python3
"""
Social Scraper CLI — browser-free profile data extraction.

Supported platforms:
  - Instagram (public profiles)
  - Facebook  (public pages)
  - Google Business Profile
  - Any website (meta/structured data)

Usage:
  python scraper.py instagram <username>
  python scraper.py facebook <page_slug_or_id>
  python scraper.py google "<business name + location>"
  python scraper.py website <url>
  python scraper.py all <instagram_user> <fb_page> "<gbp_query>" <website_url>

Output: JSON to stdout. Use --output <file> to save to file.

Environment variables (optional, for API access):
  FACEBOOK_ACCESS_TOKEN   — Facebook Graph API token
  GOOGLE_PLACES_API_KEY   — Google Places API key
"""

import argparse
import json
import logging
import sys

from platforms import ssl_fix
ssl_fix.apply()

from platforms import (
    InstagramScraper,
    FacebookScraper,
    GoogleBusinessScraper,
    WebsiteScraper,
)


def setup_logging(verbose: bool):
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stderr,
    )


def scrape_instagram(username: str, max_posts: int) -> dict:
    scraper = InstagramScraper(max_posts=max_posts)
    profile = scraper.scrape_profile(username)
    return {"platform": "instagram", "data": profile.to_dict()}


def scrape_facebook(page: str, max_posts: int) -> dict:
    scraper = FacebookScraper(max_posts=max_posts)
    profile = scraper.scrape_profile(page)
    return {"platform": "facebook", "data": profile.to_dict()}


def scrape_google(query: str, max_reviews: int) -> dict:
    scraper = GoogleBusinessScraper(max_reviews=max_reviews)
    profile = scraper.scrape_profile(query)
    return {"platform": "google_business", "data": profile.to_dict()}


def scrape_website(url: str) -> dict:
    scraper = WebsiteScraper()
    profile = scraper.scrape_profile(url)
    return {"platform": "website", "data": profile.to_dict()}


def output_result(result, output_file: str = None):
    text = json.dumps(result, indent=2, ensure_ascii=False)
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[OK] Saved to {output_file}", file=sys.stderr)
    else:
        print(text)


def main():
    parser = argparse.ArgumentParser(
        description="Social Scraper — browser-free profile data extraction",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging")
    parser.add_argument("-o", "--output", type=str, default=None, help="Save JSON output to file")
    parser.add_argument("--max-posts", type=int, default=12, help="Max posts/reviews to fetch (default: 12)")

    sub = parser.add_subparsers(dest="platform", required=True)

    # Instagram
    p_ig = sub.add_parser("instagram", aliases=["ig"], help="Scrape Instagram profile")
    p_ig.add_argument("username", help="Instagram username (without @)")

    # Facebook
    p_fb = sub.add_parser("facebook", aliases=["fb"], help="Scrape Facebook page")
    p_fb.add_argument("page", help="Facebook page slug or numeric ID")

    # Google Business
    p_gb = sub.add_parser("google", aliases=["gbp"], help="Scrape Google Business Profile")
    p_gb.add_argument("query", help='Business name + location, e.g. "Starbucks Times Square NYC"')

    # Website
    p_ws = sub.add_parser("website", aliases=["web"], help="Scrape any website")
    p_ws.add_argument("url", help="Website URL, e.g. https://example.com")

    # All platforms at once
    p_all = sub.add_parser("all", help="Scrape all platforms for a business")
    p_all.add_argument("--ig", dest="ig_user", help="Instagram username")
    p_all.add_argument("--fb", dest="fb_page", help="Facebook page slug")
    p_all.add_argument("--gbp", dest="gbp_query", help="Google Business search query")
    p_all.add_argument("--web", dest="web_url", help="Website URL")

    args = parser.parse_args()
    setup_logging(args.verbose)

    platform = args.platform
    results = []

    try:
        if platform in ("instagram", "ig"):
            results.append(scrape_instagram(args.username, args.max_posts))

        elif platform in ("facebook", "fb"):
            results.append(scrape_facebook(args.page, args.max_posts))

        elif platform in ("google", "gbp"):
            results.append(scrape_google(args.query, args.max_posts))

        elif platform in ("website", "web"):
            results.append(scrape_website(args.url))

        elif platform == "all":
            if args.ig_user:
                try:
                    results.append(scrape_instagram(args.ig_user, args.max_posts))
                except Exception as e:
                    results.append({"platform": "instagram", "error": str(e)})

            if args.fb_page:
                try:
                    results.append(scrape_facebook(args.fb_page, args.max_posts))
                except Exception as e:
                    results.append({"platform": "facebook", "error": str(e)})

            if args.gbp_query:
                try:
                    results.append(scrape_google(args.gbp_query, args.max_posts))
                except Exception as e:
                    results.append({"platform": "google_business", "error": str(e)})

            if args.web_url:
                try:
                    results.append(scrape_website(args.web_url))
                except Exception as e:
                    results.append({"platform": "website", "error": str(e)})

            if not results:
                parser.error("Provide at least one platform flag: --ig, --fb, --gbp, --web")

    except Exception as e:
        logging.error("Scraping failed: %s", e)
        output_result({"error": str(e), "platform": platform}, args.output)
        sys.exit(1)

    final = results[0] if len(results) == 1 else {"results": results}
    output_result(final, args.output)


if __name__ == "__main__":
    main()
