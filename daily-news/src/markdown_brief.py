# Markdown新闻简报生成器

import os
from datetime import datetime, timezone
from typing import List

from .news_sources import NEWS_SOURCES, CATEGORIES, CATEGORY_ORDER
from .news_fetcher import NewsItem


def _make_source_dict() -> dict:
    """名称-中文名映射"""
    return {s["name"]: s.get("name_cn", s["name"]) for s in NEWS_SOURCES}


def generate_markdown(items: List[NewsItem], date_str: str = "") -> str:
    """生成Markdown格式的每日新闻简报"""
    if not date_str:
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    source_names = _make_source_dict()

    lines = []
    lines.append(f"# 全球新闻日报 | {date_str}")
    lines.append("")
    lines.append(f"> 自动聚合自全球50+家主流媒体 · 共收录 {len(items)} 条新闻")
    lines.append("")

    # 按分类分组
    grouped = {cat: [] for cat in CATEGORY_ORDER}
    grouped["Other"] = []
    for item in items:
        cat = item.categories[0] if item.categories else "Other"
        if cat in grouped:
            grouped[cat].append(item)
        else:
            grouped["Other"].append(item)

    # 今日头条
    if items:
        top = items[0]
        cn = source_names.get(top.source_name, top.source_name)
        lines.append("---")
        lines.append("")
        lines.append("## 今日头条")
        lines.append("")
        lines.append(f"### [{top.title}]({top.url})")
        lines.append("")
        if top.summary:
            lines.append(f"> {top.summary}")
            lines.append("")
        lines.append(f"来源：**{top.source_name}** ({cn}) | {top.published[:10]}")
        lines.append("")

    # 各分类
    lines.append("---")
    lines.append("")
    lines.append("## 分类新闻")
    lines.append("")

    for cat in CATEGORY_ORDER:
        cat_items = grouped[cat]
        if not cat_items:
            continue
        cat_info = CATEGORIES.get(cat, {"label": cat})
        lines.append(f"### {cat_info['label']}")
        lines.append("")

        for item in cat_items[:20]:
            cn = source_names.get(item.source_name, item.source_name)
            time_str = item.published[:16] if len(item.published) >= 16 else item.published[:10]
            lines.append(f"- **[{item.title}]({item.url})** -- _{item.source_name}_ ({cn})")
            if item.summary:
                brief = item.summary[:150] + ("..." if len(item.summary) > 150 else "")
                lines.append(f"  - {brief}")
            lines.append(f"  - {time_str}")
            lines.append("")

    # 媒体来源统计
    lines.append("---")
    lines.append("")
    lines.append("## 今日信息来源")
    lines.append("")
    source_count = {}
    for item in items:
        sn = item.source_name
        source_count[sn] = source_count.get(sn, 0) + 1
    for src, count in sorted(source_count.items(), key=lambda x: -x[1]):
        cn = source_names.get(src, src)
        lines.append(f"- **{src}** ({cn}): {count} 条")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"*自动生成于 {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}*")
    lines.append("*新闻内容版权归原始来源所有*")

    return "\n".join(lines)


def save_markdown(items: List[NewsItem], output_dir: str, date_str: str = "") -> str:
    if not date_str:
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    os.makedirs(output_dir, exist_ok=True)
    md = generate_markdown(items, date_str)
    filepath = os.path.join(output_dir, f"daily-{date_str}.md")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"[OK] Markdown brief saved: {filepath}")
    return filepath


if __name__ == "__main__":
    from .news_fetcher import run_fetch
    items = run_fetch()
    md = generate_markdown(items)
    print(md[:500])
    save_markdown(items, "../content/briefs")
