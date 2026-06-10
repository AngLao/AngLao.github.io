import os, json, shutil
from datetime import datetime, timezone
from typing import List, Dict

from .news_sources import NEWS_SOURCES, CATEGORIES, CATEGORY_ORDER
from .news_fetcher import NewsItem
from .markdown_brief import save_markdown

SITE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "news")
CONTENT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "content")
DAILY_HTML_DIR = os.path.join(SITE_DIR, "daily")
BRIEFS_DIR = os.path.join(CONTENT_DIR, "briefs")
CONTENT_DAILY_DIR = os.path.join(CONTENT_DIR, "daily")
META_FILE = os.path.join(SITE_DIR, "meta.json")

def load_meta() -> Dict:
    if os.path.exists(META_FILE):
        with open(META_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"days": []}

def save_meta(meta: Dict):
    os.makedirs(os.path.dirname(META_FILE), exist_ok=True)
    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

def source_name_cn(name: str) -> str:
    for s in NEWS_SOURCES:
        if s["name"] == name:
            return s.get("name_cn", name)
    return name
def svg_icon(name: str, size: int = 20) -> str:
    icons = {
        "globe": '<svg xmlns="http://www.w3.org/2000/svg" width="'+str(size)+'" height="'+str(size)+'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>',
        "newspaper": '<svg xmlns="http://www.w3.org/2000/svg" width="'+str(size)+'" height="'+str(size)+'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2Zm0 0a2 2 0 0 1-2-2v-9h2"/><path d="M18 14h-8"/><path d="M15 18h-5"/><path d="M10 6h8v4h-8V6Z"/></svg>',
        "calendar": '<svg xmlns="http://www.w3.org/2000/svg" width="'+str(size)+'" height="'+str(size)+'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>',
        "clock": '<svg xmlns="http://www.w3.org/2000/svg" width="'+str(size)+'" height="'+str(size)+'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
        "arrow-up-right": '<svg xmlns="http://www.w3.org/2000/svg" width="'+str(size)+'" height="'+str(size)+'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="7" y1="17" x2="17" y2="7"/><polyline points="7 7 17 7 17 17"/></svg>',
        "archive": '<svg xmlns="http://www.w3.org/2000/svg" width="'+str(size)+'" height="'+str(size)+'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="5" rx="1"/><path d="M4 8v11a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8"/><path d="M10 12h4"/></svg>',
        "tag": '<svg xmlns="http://www.w3.org/2000/svg" width="'+str(size)+'" height="'+str(size)+'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/></svg>',
        "rss": '<svg xmlns="http://www.w3.org/2000/svg" width="'+str(size)+'" height="'+str(size)+'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 11a9 9 0 0 1 9 9"/><path d="M4 4a16 16 0 0 1 16 16"/><circle cx="5" cy="19" r="1"/></svg>',
        "menu": '<svg xmlns="http://www.w3.org/2000/svg" width="'+str(size)+'" height="'+str(size)+'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="4" y1="6" x2="20" y2="6"/><line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="18" x2="20" y2="18"/></svg>',
        "x": '<svg xmlns="http://www.w3.org/2000/svg" width="'+str(size)+'" height="'+str(size)+'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>',
        "search": '<svg xmlns="http://www.w3.org/2000/svg" width="'+str(size)+'" height="'+str(size)+'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',
    }
    return icons.get(name, "")
def category_badge(cat: str) -> str:
    info = CATEGORIES.get(cat, {"label": cat, "color": "#6b7280"})
    return f'<span class="cat-badge" style="--cat-color:{info["color"]}">{info["label"]}</span>'

def news_card(item: NewsItem, large: bool = False) -> str:
    cn = source_name_cn(item.source_name)
    cat_badges = " ".join(category_badge(c) for c in item.categories[:2])
    time_str = item.published[:16] if len(item.published) >= 16 else item.published[:10]
    img_html = ""
    if item.img_url and large:
        img_html = f"<a href=\"{item.url}\" target=\"_blank\" rel=\"noopener\"><img class=\"news-img\" src=\"{item.img_url}\" alt=\"\" loading=\"lazy\" onerror=\"this.style.display='none'\"></a>"
    cls = "news-card large" if large else "news-card"
    return f'''<article class="{cls}">
{img_html}<div class="news-body">
<h3 class="news-title"><a href="{item.url}" target="_blank" rel="noopener">{item.title}</a></h3>
<div class="news-meta">{cat_badges} <span class="source">{svg_icon("tag", 12)} {item.source_name} ({cn})</span> <span class="time">{svg_icon("clock", 12)} {time_str}</span></div>
{f"<p class=\"news-summary\">{item.summary[:200]}{'...' if len(item.summary) > 200 else ''}</p>" if item.summary and large else ""}
</div></article>'''

def category_section(cat: str, items: List[NewsItem]) -> str:
    if not items:
        return ""
    info = CATEGORIES.get(cat, {"label": cat, "color": "#6b7280"})
    cards = "\n".join(news_card(item) for item in items[:15])
    return f'''<section class="cat-section" data-category="{cat}">
<h2 class="cat-heading" style="--cat-color:{info["color"]}">{info["label"]} <span class="count">{len(items)}</span></h2>
<div class="news-grid">{cards}</div>
</section>'''

def filter_bar() -> str:
    buttons = "<button class=\"filter-btn active\" data-cat=\"all\">全部</button>"
    for cat in CATEGORY_ORDER:
        info = CATEGORIES.get(cat, {"label": cat, "color": "#0891b2"})
        href = f"#cat-{cat}"
        buttons += f"<button class=\"filter-btn\" data-cat=\"{cat}\" style=\"--cat-color:{info['color']}\">{info['label']}</button>"
    return f"<div class=\"filter-bar\">{buttons}</div>"

def date_nav(date_str: str, meta: Dict) -> str:
    days = sorted(meta.get("days", []))
    if not days or date_str not in days:
        return ""
    idx = days.index(date_str)
    prev_link = f"<a href=\"daily/{days[idx-1]}.html\" class=\"nav-arrow\">&larr; {days[idx-1]}</a>" if idx > 0 else ""
    next_link = f"<a href=\"daily/{days[idx+1]}.html\" class=\"nav-arrow\">{days[idx+1]} &rarr;</a>" if 0 <= idx < len(days)-1 else ""
    return f"<div class=\"date-nav\"><a href=\"archive.html\" class=\"nav-link\">{svg_icon('calendar', 14)} 归档</a>{prev_link}<span class=\"current-date\">{date_str}</span>{next_link}</div>"
def site_header(current: str = "index") -> str:
    pages = {"index": "今日", "archive": "归档", "about": "关于"}
    nav_html = "".join(f"<a href=\"{'' if k=='index' else k+'.html'}\" class=\"nav-item{' active' if k==current else ''}\">{v}</a>" for k,v in pages.items())
    return f'''<header class="site-header">
<div class="header-inner">
<a href="index.html" class="logo"><span class="logo-icon">{svg_icon("newspaper", 24)}</span><span class="logo-text">全球新闻日报</span></a>
<nav class="main-nav">{nav_html}</nav>
<button class="mobile-menu-btn" onclick="toggleMenu()">{svg_icon("menu", 22)}</button>
</div>
</header>'''

def site_footer() -> str:
    from datetime import datetime, timezone
    return f'''<footer class="site-footer">
<div class="footer-inner">
<p>全球新闻日报 &middot; 每日自动聚合自50+家国际主流媒体</p>
<p class="footer-links"><a href="archive.html">全部归档</a> &middot; <a href="rss.xml">RSS订阅</a> &middot; <a href="index.html">今日</a></p>
<p class="footer-legal">新闻内容版权归原始来源所有 &middot; 自动生成于 {datetime.now(timezone.utc).strftime("%Y-%m-%d")}</p>
</div>
</footer>'''

def html_page(title: str, body: str, current: str = "index", extra_head: str = "", date_str: str = "", meta: dict = None) -> str:
    dn = date_nav(date_str, meta) if date_str and meta else ""
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} - 全球新闻日报</title>
<meta name="description" content="每日全球新闻聚合 - 来自50+国际主流媒体的精选新闻">
<link rel="stylesheet" href="css/style.css">
<link rel="alternate" type="application/rss+xml" title="全球新闻日报" href="rss.xml">
{extra_head}
</head>
<body>
{site_header(current)}
<main class="main-content">
{dn}
{body}
</main>
{site_footer()}
<script src="js/main.js"></script>
</body>
</html>'''
def generate_index(items: List[NewsItem], date_str: str, meta: dict) -> str:
    top_stories = items[:5] if items else []
    top_cards = "\n".join(news_card(item, large=True) for item in top_stories)
    grouped = {cat: [] for cat in CATEGORY_ORDER}
    for item in items:
        cat = item.categories[0] if item.categories else "World"
        if cat in grouped:
            grouped[cat].append(item)
        else:
            grouped.setdefault("World", []).append(item)
    cat_sections = "\n".join(category_section(cat, grouped[cat]) for cat in CATEGORY_ORDER if grouped[cat])
    stats = f"共 {len(items)} 条新闻 &middot; 来自 {len(set(i.source_name for i in items))} 家媒体"
    body = f'''<section class="hero">
<div class="hero-header">
<h1 class="hero-title">{svg_icon("globe", 28)} 全球新闻日报</h1>
<p class="hero-date">{date_str}</p>
<p class="hero-stats">{stats}</p>
</div>
{filter_bar()}
</section>
<section class="top-stories"><h2 class="section-title">头条聚焦</h2><div class="top-grid">{top_cards}</div></section>
{cat_sections}'''
    return html_page(date_str, body, "index", date_str=date_str, meta=meta)

def generate_daily_page(items: List[NewsItem], date_str: str, meta: dict) -> str:
    grouped = {cat: [] for cat in CATEGORY_ORDER}
    for item in items:
        cat = item.categories[0] if item.categories else "World"
        if cat in grouped:
            grouped[cat].append(item)
    cat_sections = "\n".join(category_section(cat, grouped[cat]) for cat in CATEGORY_ORDER if grouped[cat])
    src_count = {}
    for item in items:
        src_count[item.source_name] = src_count.get(item.source_name, 0) + 1
    src_table = "".join(f"<tr><td>{s}</td><td>{source_name_cn(s)}</td><td>{c}</td></tr>" for s,c in sorted(src_count.items(), key=lambda x: -x[1]))
    body = f'''<section class="daily-hero">
<h1>{date_str} 全球新闻日报</h1>
<p class="stats">共 {len(items)} 条新闻 &middot; {len(src_count)} 家媒体来源</p>
<div class="source-table-wrap">
<table class="source-table"><thead><tr><th>媒体</th><th>中文名</th><th>条数</th></tr></thead><tbody>{src_table}</tbody></table>
</div>
</section>
{cat_sections}'''
    return html_page(f"{date_str} 日报", body, "archive", date_str=date_str, meta=meta)
def generate_archive(items_by_day: dict, meta: dict) -> str:
    months = {}
    for date_str in sorted(items_by_day.keys(), reverse=True):
        ym = date_str[:7]
        months.setdefault(ym, []).append(date_str)
    month_blocks = ""
    for ym in sorted(months.keys(), reverse=True):
        day_links = "".join(f"<a href=\"daily/{d}.html\" class=\"archive-day\">{d}</a>" for d in months[ym])
        month_blocks += f"<section class=\"archive-month\"><h2>{ym}</h2><div class=\"archive-days\">{day_links}</div></section>"
    body = f'''<section class="archive-page">
<h1>全部归档</h1>
<p class="archive-count">共 {len(meta.get("days", []))} 期日报</p>
{month_blocks}
</section>'''
    return html_page("新闻归档", body, "archive", extra_head="<meta name=\"robots\" content=\"all\">")

def generate_about() -> str:
    from datetime import datetime, timezone
    body = '''<section class="about-page">
<h1>关于全球新闻日报</h1>
<div class="about-content">
<p>本项目每日自动聚合来自全球50+家主流媒体的新闻头条，涵盖政治、经济、科技、环境、体育等多个领域。</p>
<h2>数据来源</h2>
<ul class="source-list">
''' + "\n".join(f"<li><strong>{s['name']}</strong> ({s.get('name_cn','')}) - {s['region']} - <a href=\"{s['url']}\" target=\"_blank\">{s['url']}</a></li>" for s in NEWS_SOURCES) + '''
</ul>
<h2>技术栈</h2>
<ul>
<li>Python + feedparser + aiohttp 抓取新闻</li>
<li>GitHub Actions 每日自动运行</li>
<li>GitHub Pages 静态托管</li>
<li>纯前端 HTML + CSS + JS，无外部依赖</li>
</ul>
</div>
</section>'''
    return html_page("关于", body, "about",
                     extra_head="<meta name=\"robots\" content=\"all\">")

def generate_rss(items_by_day: dict, meta: dict) -> str:
    latest = sorted(items_by_day.keys(), reverse=True)[0] if items_by_day else ""
    latest_items = items_by_day.get(latest, []) if latest else []
    items_xml = ""
    for item in latest_items[:30]:
        desc = item["summary"][:300] if isinstance(item, dict) and item.get("summary") else (item.summary[:300] if hasattr(item, "summary") and item.summary else item["title"] if isinstance(item, dict) else item.title)
        link = item["url"] if isinstance(item, dict) else item.url
        title = item["title"] if isinstance(item, dict) else item.title
        src = item["source_name"] if isinstance(item, dict) else item.source_name
        pub = item["published"] if isinstance(item, dict) else item.published
        items_xml += f'''  <item>
    <title><![CDATA[{title}]]></title>
    <link>{link}</link>
    <description><![CDATA[{desc}]]></description>
    <source>{src}</source>
    <pubDate>{pub}</pubDate>
    <guid>{link}</guid>
  </item>'''
    from datetime import datetime, timezone
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
<title>全球新闻日报</title>
<link>https://github.com/USERNAME/daily-news/</link>
<description>每日自动聚合自全球50+家主流媒体的新闻精选</description>
<language>zh-CN</language>
<lastBuildDate>{datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")}</lastBuildDate>
<atom:link href="https://USERNAME.github.io/daily-news/rss.xml" rel="self" type="application/rss+xml"/>
{items_xml}
</channel>
</rss>'''
def build_site(items: list, date_str: str = ""):
    if not date_str:
        from datetime import datetime, timezone
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    for d in [SITE_DIR, DAILY_HTML_DIR, BRIEFS_DIR, CONTENT_DAILY_DIR]:
        os.makedirs(d, exist_ok=True)

    meta = load_meta()
    if date_str not in meta["days"]:
        meta["days"].append(date_str)
        meta["days"] = sorted(meta["days"])
    meta["last_update"] = datetime.now(timezone.utc).isoformat()

    items_by_day = {}
    for d in meta["days"]:
        if d == date_str:
            items_by_day[d] = items
        else:
            daily_path = os.path.join(CONTENT_DAILY_DIR, f"{d}.json")
            if os.path.exists(daily_path):
                with open(daily_path, "r", encoding="utf-8") as f:
                    items_by_day[d] = json.load(f)
            else:
                items_by_day[d] = []

    items_data = [{"id": i.id, "title": i.title, "summary": i.summary,
                    "url": i.url, "source_name": i.source_name,
                    "published": i.published, "categories": i.categories,
                    "img_url": i.img_url, "language": i.language} for i in items]
    with open(os.path.join(CONTENT_DAILY_DIR, f"{date_str}.json"), "w", encoding="utf-8") as f:
        json.dump(items_data, f, ensure_ascii=False, indent=2)
    items_by_day[date_str] = items_data

    save_markdown(items, BRIEFS_DIR, date_str)

    index_html = generate_index(items, date_str, meta)
    with open(os.path.join(SITE_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    print(f"[OK] Index page generated")

    daily_html = generate_daily_page(items, date_str, meta)
    with open(os.path.join(DAILY_HTML_DIR, f"{date_str}.html"), "w", encoding="utf-8") as f:
        f.write(daily_html)
    print(f"[OK] Daily page generated: {date_str}.html")

    archive_html = generate_archive(items_by_day, meta)
    with open(os.path.join(SITE_DIR, "archive.html"), "w", encoding="utf-8") as f:
        f.write(archive_html)
    print("[OK] Archive page generated")

    about_html = generate_about()
    with open(os.path.join(SITE_DIR, "about.html"), "w", encoding="utf-8") as f:
        f.write(about_html)
    print("[OK] About page generated")

    rss_xml = generate_rss(items_by_day, meta)
    with open(os.path.join(SITE_DIR, "rss.xml"), "w", encoding="utf-8") as f:
        f.write(rss_xml)
    print("[OK] RSS feed generated")

    save_meta(meta)
    print(f"\n[DONE] Site built for {date_str}")

if __name__ == "__main__":
    pass

