"""
全球新闻 RSS 抓取引擎
异步并发抓取 → 去重 → 分类 → 排序
"""
import asyncio, hashlib, re
from datetime import datetime, timezone
import aiohttp, feedparser
from bs4 import BeautifulSoup
from .sources import NEWS_SOURCES, CATEGORY_KEYWORDS, CATEGORY_ORDER, IMPORTANCE_MIN_KEYWORD_SCORE


class NewsItem:
    __slots__ = ("id","title","summary","url","source_name","source_url",
                 "published","categories","img_url","language")
    def __init__(self, title, summary, url, source_name, source_url,
                 published=None, categories=None, img_url="", language="en"):
        self.id = hashlib.md5(url.encode()).hexdigest()[:12]
        self.title = title.strip() if title else ""
        self.summary = _clean_html(summary) if summary else ""
        self.url = url
        self.source_name = source_name
        self.source_url = source_url
        self.published = published or datetime.now(timezone.utc).isoformat()
        self.categories = categories or ["World"]
        self.img_url = img_url
        self.language = language


def _clean_html(raw):
    """Strip HTML tags, keep plain text, max 300 chars."""
    if not raw:
        return ""
    text = BeautifulSoup(raw, "html.parser").get_text(separator=" ", strip=True)
    return text[:300]


def _norm_title(title):
    """Normalize title for dedup: lowercase alnum + whitespace, first 60 chars."""
    s = "".join(c.lower() if c.isalnum() or c.isspace() else " " for c in title)
    s = re.sub(r'\s+', ' ', s).strip()
    return s[:60]


def _classify(item):
    """Keyword-based classification + importance score.
    Returns (categories, importance_score)."""
    text = (item.title + " " + item.summary).lower()
    scores = {}
    for cat, kws in CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in kws if kw.lower() in text)
        if score > 0:
            scores[cat] = score
    if not scores:
        return ["World"], 0
    ranked = sorted(scores, key=scores.get, reverse=True)
    total_score = sum(scores.values())
    return ranked[:2], total_score


def _source_weight(source_name):
    """Get source weight for importance boost."""
    for s in NEWS_SOURCES:
        if s["name"] == source_name:
            return s.get("weight", 5)
    return 5


async def _fetch_one(source, session, timeout=15):
    """Fetch one RSS feed, return list of NewsItem."""
    rss_url = source.get("rss", "")
    if not rss_url:
        return []
    try:
        async with session.get(rss_url, timeout=aiohttp.ClientTimeout(total=timeout)) as resp:
            if resp.status != 200:
                return []
            text = await resp.text()
    except Exception:
        return []

    feed = feedparser.parse(text)
    items = []
    for entry in feed.entries[:30]:
        title = entry.get("title", "").strip()
        link  = entry.get("link", "")
        if not title or not link:
            continue
        published = entry.get("published", entry.get("updated", ""))
        summary   = entry.get("summary", "") or entry.get("description", "")
        items.append(NewsItem(
            title=title, summary=summary, url=link,
            source_name=source["name"], source_url=source["url"],
            published=published, language=source.get("lang", "en")
        ))
    return items


async def fetch_all(max_concurrent=15):
    """Fetch all sources concurrently, dedup, classify, sort by time desc."""
    connector = aiohttp.TCPConnector(limit=max_concurrent, limit_per_host=2)
    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        tasks = [_fetch_one(src, session) for src in NEWS_SOURCES]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    all_items = []
    for r in results:
        if isinstance(r, list):
            all_items.extend(r)

    # Dedup by normalized title
    seen = {}
    deduped = []
    for item in all_items:
        key = _norm_title(item.title)
        if key in seen:
            continue
        seen[key] = True
        deduped.append(item)

    # Classify + importance score
    for item in deduped:
        item.categories, item._score = _classify(item)
        item._src_weight = _source_weight(item.source_name)

    # Filter: keep only important news (keyword score >= threshold)
    important = [i for i in deduped if i._score >= IMPORTANCE_MIN_KEYWORD_SCORE]
    if len(important) < 10:
        # Fallback: include lower-scored items sorted by combined score
        deduped.sort(key=lambda x: x._score + x._src_weight, reverse=True)
        important = deduped[:50]
    else:
        deduped = important

    # Sort by published time descending
    deduped.sort(key=lambda x: x.published, reverse=True)
    return deduped


def run():
    """Synchronous entry point."""
    return asyncio.run(fetch_all())
