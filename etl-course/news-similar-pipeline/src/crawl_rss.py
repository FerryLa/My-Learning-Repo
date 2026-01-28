import time
import feedparser
from typing import List, Dict

def crawl_feeds(feeds: List[str], limit: int = 1000) -> List[Dict]:
    items = []
    for url in feeds:
        try:
            fp = feedparser.parse(url)
            for e in fp.entries[:200]:
                items.append({
                    "title": getattr(e, "title", ""),
                    "url": getattr(e, "link", ""),
                    "published": getattr(e, "published", ""),
                    "summary": getattr(e, "summary", ""),
                    "feed": url
                })
        except Exception:
            continue
        time.sleep(0.1)
        if len(items) >= limit:
            break
    # dedup by url
    seen, out = set(), []
    for x in items:
        u = x["url"]
        if u and u not in seen:
            seen.add(u)
            out.append(x)
    return out[:limit]
