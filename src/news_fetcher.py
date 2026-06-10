import asyncio, hashlib
from datetime import datetime, timezone
import aiohttp, feedparser
from bs4 import BeautifulSoup
from .news_sources import NEWS_SOURCES, CATEGORY_KEYWORDS

class NewsItem:
    __slots__ = ("id","title","summary","url","source_name","source_url","published","categories","img_url","language")
    def __init__(self,title,summary,url,source_name,source_url,published=None,categories=None,img_url="",language="en"):
        self.id=hashlib.md5(url.encode()).hexdigest()[:12]
        self.title=title.strip() if title else ""
        self.summary=self._clean(summary)
        self.url=url; self.source_name=source_name; self.source_url=source_url
        self.published=published or datetime.now(timezone.utc).isoformat()
        self.categories=categories or []; self.img_url=img_url; self.language=language
    @staticmethod
    def _clean(raw):
        if not raw: return ""
        return BeautifulSoup(raw,"html.parser").get_text(separator=" ",strip=True)[:300]

async def fetch_rss(source,session,timeout=15):
    try:
        if not source.get("rss"): return []
        async with session.get(source["rss"],timeout=aiohttp.ClientTimeout(total=timeout)) as resp:
            if resp.status!=200: return []
            text=await resp.text()
    except: return []
    feed=feedparser.parse(text); items=[]
    for entry in feed.entries[:30]:
        title=entry.get("title","").strip()
        if not title: continue
        link=entry.get("link","")
        if not link: continue
        items.append(NewsItem(title=title,summary=entry.get("summary","") or entry.get("description",""),
            url=link,source_name=source["name"],source_url=source["url"],
            published=entry.get("published",entry.get("updated","")),language=source["lang"]))
    return items

def classify(item):
    text=(item.title+" "+item.summary).lower(); scores={}
    for cat,kws in CATEGORY_KEYWORDS.items():
        score=sum(1 for kw in kws if kw.lower() in text)
        if score>0: scores[cat]=score
    return sorted(scores,key=scores.get,reverse=True)[:2] if scores else ["World"]

def dedup(items):
    seen={}; result=[]
    for item in items:
        key="".join(c.lower() for c in item.title if c.isalnum() or c.isspace())[:60]
        if key in seen: continue
        seen[key]=True; result.append(item)
    return result

async def fetch_all(max_concurrent=10):
    connector=aiohttp.TCPConnector(limit=max_concurrent,limit_per_host=3)
    async with aiohttp.ClientSession(connector=connector,timeout=aiohttp.ClientTimeout(total=30)) as session:
        tasks=[fetch_rss(src,session) for src in NEWS_SOURCES]
        results=await asyncio.gather(*tasks,return_exceptions=True)
    all_items=[]
    for items in results:
        if isinstance(items,list): all_items.extend(items)
    all_items=dedup(all_items)
    for item in all_items: item.categories=classify(item)
    all_items.sort(key=lambda x:x.published,reverse=True)
    return all_items

def run(): return asyncio.run(fetch_all())
