"""
全球新闻日报 — 后端构建脚本
流程: 抓取 RSS → 保存归档 → 生成前端数据 JSON → 输出静态站点
"""
import os, json, shutil
from datetime import datetime, timezone
from .fetcher import run as fetch_news
from .sources import CATEGORIES, CATEGORY_ORDER

CAT_ORDER = CATEGORY_ORDER


def _items_to_dict(items):
    """Serialize NewsItem list to JSON-safe dict list."""
    return [{
        "id": i.id, "title": i.title, "summary": i.summary,
        "url": i.url, "source_name": i.source_name, "source_url": i.source_url,
        "published": i.published, "categories": i.categories,
        "img_url": i.img_url, "language": i.language,
    } for i in items]


def _dicts_to_items(raw_list):
    """Deserialize JSON-safe dicts back to lightweight objects."""
    items = []
    for d in raw_list:
        items.append({
            "title": d["title"],
            "summary": d.get("summary", ""),
            "url": d["url"],
            "source": d["source_name"],
            "cat": d["categories"][0] if d.get("categories") else "World",
            "date": d.get("published", "")[:10],
        })
    return items


def build():
    repo_root  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    frontend   = os.path.join(repo_root, "frontend")
    output_dir = os.path.join(repo_root, "site")
    data_dir   = os.path.join(output_dir, "data")
    content_dir = os.path.join(repo_root, "content", "data")

    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(content_dir, exist_ok=True)
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # ═══════════════════════════════════════════════════
    # 1. 抓取新闻
    # ═══════════════════════════════════════════════════
    print("[*] 抓取新闻中...")
    raw_items = fetch_news()
    print(f"[+] 获取到 {len(raw_items)} 条新闻")

    if not raw_items:
        print("[!] 未获取到新闻，使用示例数据")
        from .sources import NEWS_SOURCES
        fallback = []
        for i, src in enumerate(NEWS_SOURCES[:3]):
            fallback.append(type('NewsItem',(),{
                "id": f"demo{i}", "title": f"全球新闻日报 — 来自 {src['name']} 的头条",
                "summary": "本期为示例数据。实际运行时将从50+ RSS源抓取实时新闻。",
                "url": src["url"], "source_name": src["name"], "source_url": src["url"],
                "published": date_str+"T00:00:00Z", "categories": src.get("focus",["World"])[:2],
                "img_url": "", "language": src.get("lang","en"),
            })())
        raw_items = fallback

    # ═══════════════════════════════════════════════════
    # 2. 保存归档数据到 content/data/（Git 持久化）
    # ═══════════════════════════════════════════════════
    daily_path = os.path.join(content_dir, f"{date_str}.json")
    with open(daily_path, "w", encoding="utf-8") as f:
        json.dump(_items_to_dict(raw_items), f, ensure_ascii=False, indent=2)
    print(f"[OK] 归档 content/data/{date_str}.json")

    # 加载历史 meta
    meta_path = os.path.join(content_dir, "meta.json")
    all_dates = []
    if os.path.exists(meta_path):
        with open(meta_path, "r", encoding="utf-8") as f:
            all_dates = json.load(f)
    if date_str not in all_dates:
        all_dates.append(date_str)
    all_dates = sorted(set(all_dates))
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(all_dates, f, ensure_ascii=False, indent=2)

    # ═══════════════════════════════════════════════════
    # 3. 加载历史数据（用于 archive + daily pages）
    # ═══════════════════════════════════════════════════
    all_items_by_day = {}
    for d in all_dates:
        p = os.path.join(content_dir, f"{d}.json")
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                raw = json.load(f)
                all_items_by_day[d] = _dicts_to_items(raw)

    # ═══════════════════════════════════════════════════
    # 4. 生成 site/data/news.json（当天，前端渲染用）
    # ═══════════════════════════════════════════════════
    today_items = _dicts_to_items(_items_to_dict(raw_items))
    grouped = {c: [] for c in CAT_ORDER}
    for item in today_items:
        cat = item.get("cat", "World")
        if cat in grouped:
            grouped[cat].append(item)

    news_json = {
        "date": date_str,
        "stats": {
            "total": len(today_items),
            "sources": len(set(i["source"] for i in today_items)),
        },
        "items": today_items,
        "categories": {k: v for k, v in grouped.items() if v},
    }
    with open(os.path.join(data_dir, "news.json"), "w", encoding="utf-8") as f:
        json.dump(news_json, f, ensure_ascii=False, indent=2)
    print(f"[OK] site/data/news.json")

    # ═══════════════════════════════════════════════════
    # 5. 生成 site/data/archive.json
    # ═══════════════════════════════════════════════════
    archive_json = {"dates": sorted(all_dates, reverse=True)}
    with open(os.path.join(data_dir, "archive.json"), "w", encoding="utf-8") as f:
        json.dump(archive_json, f, ensure_ascii=False, indent=2)
    print(f"[OK] site/data/archive.json ({len(all_dates)} 期)")

    # ═══════════════════════════════════════════════════
    # 6. 生成 RSS
    # ═══════════════════════════════════════════════════
    item_xml = ""
    for item in today_items[:30]:
        item_xml += (
            f"<item><title><![CDATA[{item['title']}]]></title>"
            f"<link>{item['url']}</link>"
            f"<source>{item['source']}</source>"
            f"<guid>{item['url']}</guid></item>"
        )
    rss_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
<title>全球新闻日报</title>
<link>https://AngLao.github.io/</link>
<description>每日全球新闻聚合 — 来自50+国际主流媒体的精选新闻</description>
<language>zh-CN</language>
<atom:link href="https://AngLao.github.io/rss.xml" rel="self" type="application/rss+xml"/>
{item_xml}
</channel>
</rss>"""
    with open(os.path.join(output_dir, "rss.xml"), "w", encoding="utf-8") as f:
        f.write(rss_xml)
    print(f"[OK] rss.xml")

    # ═══════════════════════════════════════════════════
    # 7. 生成每日详情页 HTML + JSON
    # ═══════════════════════════════════════════════════
    daily_dir     = os.path.join(output_dir, "daily")
    daily_data_dir = os.path.join(data_dir, "daily")
    os.makedirs(daily_dir, exist_ok=True)
    os.makedirs(daily_data_dir, exist_ok=True)

    # 为每个历史日期生成 JSON 数据文件
    for d, items in all_items_by_day.items():
        grouped_d = {c: [] for c in CAT_ORDER}
        for item in items:
            cat = item.get("cat", "World")
            if cat in grouped_d:
                grouped_d[cat].append(item)
        day_json = {
            "date": d,
            "stats": {"total": len(items), "sources": len(set(i["source"] for i in items))},
            "items": items,
            "categories": {k: v for k, v in grouped_d.items() if v},
        }
        jp = os.path.join(daily_data_dir, f"{d}.json")
        with open(jp, "w", encoding="utf-8") as f:
            json.dump(day_json, f, ensure_ascii=False, indent=2)
    print(f"[OK] data/daily/ ({len(all_items_by_day)} JSON)")
    daily_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{date_str} — 全球新闻日报</title>
<meta name="description" content="{date_str} 全球新闻日报">
<link rel="stylesheet" href="../css/style.css">
</head>
<body>
<header class="site-header">
  <div class="header-inner">
    <a href="../index.html" class="logo">
      <svg class="logo-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2Z"/><path d="M18 14h-8"/><path d="M15 18h-5"/><path d="M10 6h8v4h-8V6Z"/></svg>
      <span class="logo-text">全球新闻日报</span>
    </a>
    <nav class="main-nav"><a href="../index.html">首页</a><a href="../archive.html">归档</a><a href="../about.html">关于</a></nav>
  </div>
</header>
<main class="main-content">
  <section id="daily-hero" class="hero"><h1>全球新闻日报</h1><p>{date_str}</p><p id="daily-stats" class="hero-stats"></p></section>
  <section id="daily-top" class="top-stories"><h2 class="section-title">★ 要闻</h2><div id="daily-grid" class="top-grid"></div></section>
</main>
<footer class="site-footer">
  <div class="footer-inner"><p>全球新闻日报 — 每日自动聚合自全球50+家主流媒体</p></div>
</footer>
<script>var DAILY_DATE='{date_str}';</script>
<script src="../js/main.js"></script>
</body>
</html>"""
    for d, items in all_items_by_day.items():
        dp = os.path.join(daily_dir, f"{d}.html")
        if not os.path.exists(dp):
            with open(dp, "w", encoding="utf-8") as f:
                f.write(daily_template.format(date_str=d))
    print(f"[OK] daily/ ({len(all_items_by_day)} 页)")

    # ═══════════════════════════════════════════════════
    # 8. 复制前端文件
    # ═══════════════════════════════════════════════════
    # 清理 site/（保留 data/ rss.xml daily/）
    keep = {"data", "rss.xml", "daily"}
    for name in os.listdir(output_dir):
        if name in keep:
            continue
        p = os.path.join(output_dir, name)
        if os.path.isdir(p):
            shutil.rmtree(p)
        else:
            os.remove(p)

    for name in os.listdir(frontend):
        src = os.path.join(frontend, name)
        dst = os.path.join(output_dir, name)
        if os.path.isdir(src):
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
    print(f"[OK] frontend/ → site/")

    # ═══════════════════════════════════════════════════
    # 9. .nojekyll
    # ═══════════════════════════════════════════════════
    with open(os.path.join(output_dir, ".nojekyll"), "w") as f:
        pass

    print(f"[DONE] 站点构建完成 — {date_str}")


if __name__ == "__main__":
    build()
