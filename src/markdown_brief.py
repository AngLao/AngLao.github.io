import os
from datetime import datetime, timezone
from .news_sources import NEWS_SOURCES, CATEGORIES, CATEGORY_ORDER, CATEGORY_KEYWORDS


def generate(items, date_str=None, output_dir=None):
    """Generate a structured Markdown brief from news items.

    Args:
        items: list of NewsItem objects
        date_str: date string like '2025-01-15' (defaults to today UTC)
        output_dir: directory to write the .md file (defaults to content/briefs/)

    Returns:
        path to the generated .md file
    """
    if date_str is None:
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if output_dir is None:
        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_dir = os.path.join(repo_root, "content", "briefs")

    os.makedirs(output_dir, exist_ok=True)

    # Group by category
    grouped = {cat: [] for cat in CATEGORY_ORDER}
    for item in items:
        cat = item.categories[0] if item.categories else "World"
        if cat in grouped:
            grouped[cat].append(item)

    source_count = len(set(i.source_name for i in items))

    lines = []
    lines.append(f"# 全球新闻日报 — {date_str}")
    lines.append("")
    lines.append(f"> 共 {len(items)} 条新闻 · 来自 {source_count} 家媒体")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Top 5 headline stories
    lines.append("## ★ 今日要闻")
    lines.append("")
    for idx, item in enumerate(items[:5], 1):
        time_str = item.published[:10] if len(item.published) >= 10 else ""
        lines.append(f"{idx}. **[{item.title}]({item.url})**")
        lines.append(f"   - 来源: {item.source_name} · {time_str}")
        if item.summary:
            lines.append(f"   - {item.summary[:150]}{'...' if len(item.summary) > 150 else ''}")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Table of contents
    lines.append("## 目录")
    lines.append("")
    for cat in CATEGORY_ORDER:
        if grouped[cat]:
            info = CATEGORIES.get(cat, {"label": cat})
            lines.append(f"- [{info['label']}](#{cat.lower()}) ({len(grouped[cat])} 条)")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Sections by category
    for cat in CATEGORY_ORDER:
        cat_items = grouped[cat]
        if not cat_items:
            continue
        info = CATEGORIES.get(cat, {"label": cat})
        lines.append(f"## {info['label']}")
        lines.append("")
        lines.append(f"| # | 标题 | 来源 | 时间 |")
        lines.append(f"|---|------|------|------|")
        for idx, item in enumerate(cat_items[:20], 1):
            time_str = item.published[:10] if len(item.published) >= 10 else ""
            title_escaped = item.title.replace("|", "\\|")
            lines.append(f"| {idx} | [{title_escaped}]({item.url}) | {item.source_name} | {time_str} |")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(f"*自动生成于 {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} · 全球新闻日报*")
    lines.append("")

    path = os.path.join(output_dir, f"{date_str}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return path
