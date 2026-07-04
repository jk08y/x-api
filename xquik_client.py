import json
import os
from urllib import parse, request
from urllib.error import HTTPError, URLError


XQUIK_API_BASE = "https://xquik.com/api/v1"


def fetch_xquik_tweet_examples(query, limit=2):
    api_key = os.environ.get("XQUIK_API_KEY", "").strip()
    if not api_key or not query:
        return []

    base_url = os.environ.get("XQUIK_API_BASE_URL", XQUIK_API_BASE).rstrip("/")
    params = parse.urlencode({
        "q": query.strip(),
        "limit": max(1, min(int(limit), 5)),
        "queryType": "Top",
    })
    req = request.Request(
        f"{base_url}/x/tweets/search?{params}",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "x-api-flask/1.0",
        },
        method="GET",
    )

    try:
        with request.urlopen(req, timeout=15) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, OSError, ValueError, json.JSONDecodeError):
        return []

    tweets = payload.get("tweets", [])
    if not isinstance(tweets, list):
        return []

    examples = []
    for tweet in tweets:
        if not isinstance(tweet, dict):
            continue
        text = " ".join(str(tweet.get("text") or "").split())
        if not text:
            continue
        author = tweet.get("author") if isinstance(tweet.get("author"), dict) else {}
        username = str(author.get("username") or "").strip()
        examples.append(f"@{username}: {text[:180]}" if username else text[:180])
        if len(examples) >= limit:
            break
    return examples


def append_xquik_context(tweet_content, query):
    examples = fetch_xquik_tweet_examples(query)
    if not examples:
        return tweet_content
    context = " | ".join(examples)
    suffix = f"\n\nContext via Xquik: {context}"
    return f"{tweet_content}{suffix}"[:280]
