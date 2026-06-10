# 新闻抓取引擎 - 基于RSS

import asyncio
import hashlib
from datetime import datetime, timezone
from typing import Optional

import aiohttp
from bs4 import BeautifulSoup
import feedparser

from .news_sources import NEWS_SOURCES, CATEGORY_KEYWORDS


class NewsItem:
    """一条新闻"""
    __slots__ = ("id", "title", "summary", "url", "source_name", "source_url",
                 "published", "categories", "img_url", "language")

    def __init__(self, title: str, summary: str, url: str,
                 source_name: str, source_url: str, published: Optional[str] = None,
                 categories=None, img_url: str = "", language: str = "en"):
        self.id = hashlib.md5(url.encode()).hexdigest()[:12]
        self.title = title.strip() if title else ""
        self.summary = self._clean_summary(summary)
        self.url = url
        self.source_name = source_name
        self.source_url = source_url
        self.published = published or datetime.now(timezone.utc).isoformat()
        self.categories = categories or []
        self.img_url = img_url
        self.language = language

    @staticmethod
    def _clean_summary(raw: str) -> str:
        if not raw:
            return ""
        soup = BeautifulSoup(raw, "html.parser")
        return soup.get_text(separator=" ", strip=True)[:300]


async def fetch_rss_feed(source: dict, session: aiohttp.ClientSession,
                         timeout: int = 15) -> list[NewsItem]:
    """抓取一个RSS源"""
    try:
        async with session.get(source["rss"], timeout=aiohttp.ClientTimeout(total=timeout),
                               headers={"User-Agent": "NewsDailyBot/1.0"}) as resp:
            if resp.status != 200:
                return []
            text = await resp.text()
    except Exception:
        return []

    feed = feedparser.parse(text)
    items = []
    for entry in feed.entries[:30]:  # 每个源取前30条
        title = entry.get("title", "").strip()
        if not title:
            continue
        summary = entry.get("summary", "") or entry.get("description", "")
        link = entry.get("link", "")
        if not link:
            continue
        pub = entry.get("published", entry.get("updated", ""))
        img_url = ""
        media_content = entry.get("media_content") or entry.get("enclosures") or []
        for mc in media_content:
            url = mc.get("url") if isinstance(mc, dict) else getattr(mc, "href", None) or getattr(mc, "url", None)
            if url:
                img_url = url
                break
        # 尝试从 content 或 summary 中提取图片
        if not img_url and "media:content" in entry:
            mc = entry["media:content"]
            if isinstance(mc, list):
                img_url = mc[0].get("url", "")
            elif isinstance(mc, dict):
                img_url = mc.get("url", "")

        items.append(NewsItem(
            title=title, summary=summary, url=link,
            source_name=source["name"], source_url=source["url"],
            published=pub, img_url=img_url,
            language=source["lang"]
        ))
    return items


def classify_news(item: NewsItem) -> list[str]:
    """基于标题和摘要自动分类"""
    text = (item.title + " " + item.summary).lower()
    scores = {}
    for cat, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw.lower() in text)
        if score > 0:
            scores[cat] = score
    if not scores:
        return ["World"]
    sorted_cats = sorted(scores, key=scores.get, reverse=True)
    return sorted_cats[:2]  # 最多两个分类


def deduplicate(items: list[NewsItem]) -> list[NewsItem]:
    """基于标题相似度去重"""
    def normalize(t: str) -> str:
        return "".join(c.lower() for c in t if c.isalnum() or c.isspace())

    seen = {}
    result = []
    for item in items:
        key = normalize(item.title)[:60]
        if key in seen:
            continue
        # 检查相似度
        dup = False
        for existing in seen:
            if len(set(key.split()) & set(existing.split())) / max(1, len(set(key.split()) | set(existing.split()))) > 0.7:
                dup = True
                break
        if not dup:
            seen[key] = True
            result.append(item)
    return result


async def fetch_all_news(max_concurrent: int = 10) -> list[NewsItem]:
    """并发抓取所有新闻源"""
    connector = aiohttp.TCPConnector(limit=max_concurrent, limit_per_host=3)
    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        tasks = [fetch_rss_feed(src, session) for src in NEWS_SOURCES]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    all_items = []
    for items in results:
        if isinstance(items, list):
            all_items.extend(items)

    # 去重
    all_items = deduplicate(all_items)

    # 分类
    for item in all_items:
        cats = classify_news(item)
        item.categories = cats

    # 按发布时间排序
    all_items.sort(key=lambda x: x.published, reverse=True)
    return all_items


def run_fetch() -> list[NewsItem]:
    """同步入口（方便脚本调用）"""
    return asyncio.run(fetch_all_news())


if __name__ == "__main__":
    items = run_fetch()
    print(f"Fetched {len(items)} news items")
    for item in items[:5]:
        print(f"  [{', '.join(item.categories)}] {item.title[:60]} - {item.source_name}")
