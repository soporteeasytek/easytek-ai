---
name: social-scraper
description: Scrape public profile data from Instagram, Facebook, Google Business Profile, and any website. Use when the user asks to get info about a business or person's social media presence, check a competitor's profile, audit social media accounts, extract contact info from websites, or analyze a business online presence. Triggers on phrases like "check their Instagram", "get info from Facebook", "look up this business on Google", "scrape their website", "social media audit", "profile data", "competitor analysis", "extract contact info".
---

# Social Media Profile Scraper

Extract public data from social media profiles and websites **without a browser**. Works in restricted environments (OpenClaw sandbox, NemoClaw, headless servers).

## Setup

The tool lives at `skills/social-scraper/` with its own Python virtualenv.

**Activate before use:**
```bash
source ~/.openclaw/workspace/skills/social-scraper/venv/bin/activate
```

**Base command:**
```bash
python ~/.openclaw/workspace/skills/social-scraper/scraper.py
```

## Commands

### Instagram (public profiles)

```bash
source ~/.openclaw/workspace/skills/social-scraper/venv/bin/activate && \
python ~/.openclaw/workspace/skills/social-scraper/scraper.py instagram {username}
```

Returns: username, full_name, biography, followers, following, posts_count, is_private, is_verified, profile_pic_url, external_url, recent_posts (caption, likes, comments, date, url).

### Facebook (public pages)

```bash
source ~/.openclaw/workspace/skills/social-scraper/venv/bin/activate && \
python ~/.openclaw/workspace/skills/social-scraper/scraper.py facebook {page_slug_or_id}
```

Returns: name, category, description, about, followers, likes, website, phone, email, address, is_verified, recent_posts.

**With Graph API (more complete data):** Set `FACEBOOK_ACCESS_TOKEN` env var.

### Google Business Profile

```bash
source ~/.openclaw/workspace/skills/social-scraper/venv/bin/activate && \
python ~/.openclaw/workspace/skills/social-scraper/scraper.py google "{business_name} {city}"
```

Returns: name, address, phone, website, rating, reviews_count, category, hours, coordinates, reviews_sample.

**With Places API (more complete data):** Set `GOOGLE_PLACES_API_KEY` env var.

### Website (any URL)

```bash
source ~/.openclaw/workspace/skills/social-scraper/venv/bin/activate && \
python ~/.openclaw/workspace/skills/social-scraper/scraper.py website {url}
```

Returns: title, description, og_image, language, emails, phones, social_links (auto-detected Facebook/Instagram/Twitter/LinkedIn/YouTube/TikTok links), meta_tags, structured_data (JSON-LD), technologies (WordPress, Shopify, React, etc.), rss_feeds.

### All Platforms at Once

```bash
source ~/.openclaw/workspace/skills/social-scraper/venv/bin/activate && \
python ~/.openclaw/workspace/skills/social-scraper/scraper.py all \
  --ig {instagram_user} \
  --fb {facebook_page} \
  --gbp "{google_business_query}" \
  --web {website_url}
```

Any flag can be omitted if not needed.

## Options

| Flag | Description |
|------|-------------|
| `-o FILE` | Save JSON output to file instead of stdout |
| `-v` | Verbose/debug logging |
| `--max-posts N` | Max posts/reviews to fetch (default: 12) |

## Output Format

All commands output JSON to stdout. Example:

```json
{
  "platform": "instagram",
  "data": {
    "username": "cocacola",
    "full_name": "Coca-Cola",
    "biography": "...",
    "followers": 2900000,
    "following": 50,
    "posts_count": 1200,
    "is_private": false,
    "is_verified": true,
    "recent_posts": [...]
  }
}
```

## Save Results

```bash
source ~/.openclaw/workspace/skills/social-scraper/venv/bin/activate && \
python ~/.openclaw/workspace/skills/social-scraper/scraper.py instagram cocacola -o /tmp/ig-result.json
```

## Tips

1. **Match usernames:** When the user says "their Instagram", figure out the username first
2. **Combine platforms:** Use the `all` command for comprehensive audits
3. **Private profiles:** Instagram private profiles only return basic info (no posts)
4. **Facebook:** Works best with public Pages (businesses, creators). Personal profiles are restricted
5. **Google Business:** Use "business name + city" for best results
6. **Website:** Great for extracting contact info, social links, and tech stack from any URL
7. **Rate limits:** Don't scrape the same profile repeatedly in short succession
8. **Errors are JSON:** Failed scrapes return `{"error": "..."}` — check the message
