"""
全球新闻日报 — 静态站点构建器
纯 Python 标准库，零外部依赖。生成完整的静态 HTML 站点到 site/ 目录。
"""
import os, json, shutil
from datetime import datetime, timezone

# ── 站点元数据 ──────────────────────────────────────────
SITE_TITLE = "全球新闻日报"
SITE_DESC  = "每日全球新闻聚合 — 来自50+国际主流媒体的精选新闻"
SITE_URL   = "https://AngLao.github.io"

# ── 分类定义 ────────────────────────────────────────────
CATEGORIES = {
    "World":       {"label": "国际",  "color": "#0891b2"},
    "Politics":    {"label": "政治",  "color": "#dc2626"},
    "Economy":     {"label": "经济",  "color": "#059669"},
    "Technology":  {"label": "科技",  "color": "#2563eb"},
    "Science":     {"label": "科学",  "color": "#7c3aed"},
    "Environment": {"label": "环境",  "color": "#16a34a"},
    "Sports":      {"label": "体育",  "color": "#ea580c"},
    "Culture":     {"label": "文化",  "color": "#d946ef"},
}
CAT_ORDER = list(CATEGORIES.keys())

# ── 示例新闻数据 ────────────────────────────────────────
DEMO_NEWS = [
    {"title": "联合国大会通过全球人工智能治理决议", "summary": "联合国大会以压倒性多数票通过首个全球人工智能治理框架决议，旨在确保AI技术发展符合人权和可持续发展目标。", "source": "Reuters", "cat": "Technology", "url": "#"},
    {"title": "美联储维持利率不变 暗示年内可能降息", "summary": "美联储连续第三次会议维持基准利率不变，但最新点阵图显示年内仍有两次降息空间，市场反应积极。", "source": "Bloomberg", "cat": "Economy", "url": "#"},
    {"title": "巴黎气候峰会达成新减排协议", "summary": "经过两周艰苦谈判，190多个国家在巴黎气候峰会上达成新的全球减排协议，承诺在2035年前将碳排放减少60%。", "source": "BBC News", "cat": "Environment", "url": "#"},
    {"title": "SpaceX星舰第五次试飞成功回收助推器", "summary": "SpaceX星舰完成第五次轨道试飞，超重型助推器首次实现发射台机械臂精准捕获回收，人类深空探索迈出关键一步。", "source": "CNN", "cat": "Technology", "url": "#"},
    {"title": "世界杯预选赛：中国队客场逆转取胜", "summary": "亚洲区世界杯预选赛，中国队在先失一球的情况下连入两球逆转击败对手，出线形势大好转。", "source": "新华社", "cat": "Sports", "url": "#"},
    {"title": "全球贸易反弹：WTO上调今年贸易增长预期", "summary": "世界贸易组织将2024年全球货物贸易增长预期从2.6%上调至3.3%，亚洲出口表现尤为强劲。", "source": "Financial Times", "cat": "Economy", "url": "#"},
    {"title": "诺贝尔文学奖揭晓：挪威作家获奖", "summary": "瑞典文学院宣布将本年度诺贝尔文学奖授予挪威作家，表彰其以诗意的笔触探索人类存在的边界。", "source": "The Guardian", "cat": "Culture", "url": "#"},
    {"title": "科学家发现新型抗生素可杀死超级细菌", "summary": "国际研究团队利用AI技术从数百万化合物中筛选出一种全新抗生素，对多种耐药超级细菌有效。", "source": "Nature", "cat": "Science", "url": "#"},
    {"title": "美国大选：两党候选人在关键摇摆州展开最后冲刺", "summary": "距离美国大选仅剩数周，两党候选人在宾夕法尼亚、密歇根等关键摇摆州密集造势，民调差距在误差范围内。", "source": "Associated Press", "cat": "Politics", "url": "#"},
    {"title": "全球可再生能源装机容量创历史新高", "summary": "国际能源署报告显示，今年全球新增可再生能源装机容量将首次超过500GW，太阳能和风能领涨。", "source": "Al Jazeera", "cat": "Environment", "url": "#"},
    {"title": "Apple发布新一代芯片M4：AI算力提升3倍", "summary": "Apple正式发布M4芯片，采用台积电3nm工艺，神经引擎算力较M3提升3倍，率先搭载于新款MacBook Pro。", "source": "The Verge", "cat": "Technology", "url": "#"},
    {"title": "欧盟通过对华电动汽车反补贴关税", "summary": "欧盟成员国投票通过对从中国进口的电动汽车征收最高45%的反补贴关税，中方表示将采取反制措施。", "source": "South China Morning Post", "cat": "Politics", "url": "#"},
    {"title": "奥运会：巴黎2024圆满落幕 中国金牌数创境外最佳", "summary": "巴黎奥运会正式闭幕，中国代表团以42金27银23铜的成绩位列金牌榜第二，创境外参赛最佳战绩。", "source": "央视新闻", "cat": "Sports", "url": "#"},
    {"title": "全球央行数字货币竞赛加速：120国进入研发阶段", "summary": "国际清算银行报告显示，目前已有超过120个国家和地区进入央行数字货币的研发或试点阶段。", "source": "Nikkei Asia", "cat": "Economy", "url": "#"},
    {"title": "威尼斯双年展中国馆开幕 聚焦传统与当代对话", "summary": "第60届威尼斯双年展中国馆正式开幕，以'共生之境'为主题，呈现传统水墨与数字艺术的跨界融合。", "source": "澎湃新闻", "cat": "Culture", "url": "#"},
    {"title": "基因编辑疗法首次获批用于儿童遗传病治疗", "summary": "美国FDA首次批准一种基于CRISPR基因编辑技术的药物用于治疗儿童罕见遗传病，开创精准医疗新纪元。", "source": "Deutsche Welle", "cat": "Science", "url": "#"},
    {"title": "全球气候异常：多地夏季极端高温破历史记录", "summary": "今年夏季全球多地遭遇前所未有的极端高温天气，南欧和南亚部分地区气温突破50°C。", "source": "France 24", "cat": "Environment", "url": "#"},
    {"title": "中东和平谈判在挪威重启 各方释放积极信号", "summary": "经挪威斡旋，中东和平谈判在奥斯陆重启，各方代表首次就长期停火框架进行实质性讨论。", "source": "Al Jazeera", "cat": "World", "url": "#"},
    {"title": "NBA总决赛：掘金队以4-2击败热火成功卫冕", "summary": "丹佛掘金队在NBA总决赛第六场中以112-98击败迈阿密热火队，以4-2总比分成功卫冕总冠军。", "source": "ESPN", "cat": "Sports", "url": "#"},
    {"title": "全球粮食安全峰会召开 承诺100亿美元援助", "summary": "联合国粮农组织召开全球粮食安全峰会，20国集团承诺提供100亿美元援助，应对非洲和南亚粮食危机。", "source": "The New York Times", "cat": "World", "url": "#"},
]


# ── SVG 图标 ────────────────────────────────────────────
SVG_GLOBE    = '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>'
SVG_NEWSPAPER = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2Z"/><path d="M18 14h-8"/><path d="M15 18h-5"/><path d="M10 6h8v4h-8V6Z"/></svg>'
SVG_CALENDAR  = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>'


# ═══════════════════════════════════════════════════════════
#  HTML 组件
# ═══════════════════════════════════════════════════════════

def _header(current="index", prefix=""):
    pages = {"index": "首页", "archive": "归档", "about": "关于"}
    nav = ""
    for k, v in pages.items():
        href = f'{prefix}{"" if k == "index" else k + ".html"}'
        cls = ' class="active"' if k == current else ""
        nav += f'<a href="{href}"{cls}>{v}</a>'
    return (
        f'<header class="site-header">'
        f'<div class="header-inner">'
        f'<a href="{prefix}index.html" class="logo">'
        f'<span class="logo-icon">{SVG_NEWSPAPER}</span>'
        f'<span class="logo-text">{SITE_TITLE}</span>'
        f'</a>'
        f'<nav class="main-nav">{nav}</nav>'
        f'</div>'
        f'</header>'
    )


def _footer(prefix=""):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return (
        f'<footer class="site-footer">'
        f'<div class="footer-inner">'
        f'<p>{SITE_TITLE} — 每日自动聚合自全球50+家主流媒体</p>'
        f'<p class="footer-links">'
        f'<a href="{prefix}archive.html">归档</a> · '
        f'<a href="{prefix}rss.xml">RSS</a> · '
        f'<a href="{prefix}about.html">关于</a>'
        f'</p>'
        f'<p class="footer-legal">新闻内容版权归原始来源所有 · 自动生成于 {now}</p>'
        f'</div>'
        f'</footer>'
    )


def _page(title, body, current="index", prefix="", extra_head=""):
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — {SITE_TITLE}</title>
<meta name="description" content="{SITE_DESC}">
<link rel="stylesheet" href="{prefix}css/style.css">
<link rel="alternate" type="application/rss+xml" title="{SITE_TITLE}" href="{prefix}rss.xml">
{extra_head}
</head>
<body>
{_header(current, prefix)}
<main class="main-content">
{body}
</main>
{_footer(prefix)}
<script src="{prefix}js/main.js"></script>
</body>
</html>"""


def _news_card(item, large=False):
    cat_info = CATEGORIES.get(item["cat"], {"label": item["cat"], "color": "#6b7280"})
    cat_html = f'<span class="cat-badge" style="--cat-color:{cat_info["color"]}">{cat_info["label"]}</span>'
    time_str = item.get("date", "")[:10]
    src     = item["source"]
    title   = item["title"]
    url     = item["url"]
    summary = item.get("summary", "")

    cls = "news-card large" if large else "news-card"
    summary_html = ""
    if summary and large:
        short = summary[:200] + ("..." if len(summary) > 200 else "")
        summary_html = f'<p class="news-summary">{short}</p>'

    return f"""<article class="{cls}">
<div class="news-body">
<h3 class="news-title"><a href="{url}" target="_blank" rel="noopener">{title}</a></h3>
<div class="news-meta">
{cat_html}<span class="source">&#9742; {src}</span><span class="time">{SVG_CALENDAR} {time_str}</span>
</div>
{summary_html}
</div>
</article>"""


def _cat_section(cat, items):
    if not items:
        return ""
    info = CATEGORIES.get(cat, {"label": cat, "color": "#6b7280"})
    cards = "\n".join(_news_card(i) for i in items[:12])
    return f"""<section class="cat-section" data-category="{cat}">
<h2 class="cat-heading" style="--cat-color:{info['color']}">{info['label']}<span class="count">{len(items)}</span></h2>
<div class="news-grid">{cards}</div>
</section>"""


# ═══════════════════════════════════════════════════════════
#  页面生成
# ═══════════════════════════════════════════════════════════

def gen_index(items, date_str, prefix=""):
    top       = items[:5]
    top_cards = "\n".join(_news_card(i, large=True) for i in top)

    grouped = {c: [] for c in CAT_ORDER}
    for item in items:
        cat = item.get("cat", "World")
        if cat in grouped:
            grouped[cat].append(item)

    cat_html = "\n".join(_cat_section(c, grouped[c]) for c in CAT_ORDER if grouped[c])

    stats = f"共 {len(items)} 条新闻 · 来自 {len(set(i['source'] for i in items))} 家媒体"

    body = f"""<section class="hero">
<div class="hero-icon">{SVG_GLOBE}</div>
<h1>{SITE_TITLE}</h1>
<p>{date_str}</p>
<p style="font-size:.85rem;color:#94a3b8">{stats}</p>
</section>
<section class="top-stories">
<h2 class="section-title">★ 今日要闻</h2>
<div class="top-grid">{top_cards}</div>
</section>
{cat_html}"""

    return _page(date_str, body, current="index", prefix=prefix)


def gen_archive(items_by_day):
    months = {}
    for d in sorted(items_by_day, reverse=True):
        months.setdefault(d[:7], []).append(d)

    sections = []
    for ym in sorted(months, reverse=True):
        links = "".join(
            f"<a href='daily/{d}.html' class='archive-day'>{d}</a>"
            for d in months[ym]
        )
        sections.append(
            f'<section class="archive-month"><h2>{ym}</h2>'
            f'<div class="archive-days">{links}</div></section>'
        )

    body = f"""<section class="archive-page">
<h1>新闻归档</h1>
<p class="archive-count">共 {len(items_by_day)} 期日报</p>
{"".join(sections)}
</section>"""

    return _page("新闻归档", body, current="archive",
                 extra_head='<meta name="robots" content="all">')


def gen_about():
    cat_tags = "".join(
        f'<span style="display:inline-block;padding:2px 10px;margin:2px;'
        f'border-radius:12px;background:{c["color"]};color:#fff;font-size:.85rem">'
        f'{c["label"]}</span>'
        for c in CATEGORIES.values()
    )
    body = f"""<section class="about-page">
<h1>关于{SITE_TITLE}</h1>
<div class="about-content">
<p>本项目每日自动聚合来自全球50+家主流媒体的头条新闻，涵盖政治、经济、科技、环境、体育等多个领域。</p>
<p>由 Python 脚本抓取 RSS feed，通过 GitHub Actions 每日自动运行，构建静态网站并托管于 GitHub Pages。</p>
<h2>技术栈</h2>
<ul>
<li>Python 标准库构建 · 零外部依赖</li>
<li>GitHub Actions — UTC 00:00 每日运行</li>
<li>GitHub Pages 静态托管</li>
<li>纯前端 HTML + CSS + JS，零依赖</li>
</ul>
<h2>新闻分类</h2>
<div style="margin-top:8px">{cat_tags}</div>
</div>
</section>"""
    return _page("关于", body, current="about",
                 extra_head='<meta name="robots" content="all">')


def gen_rss(items, date_str):
    item_xml = ""
    for item in items[:30]:
        item_xml += (
            f"<item><title><![CDATA[{item['title']}]]></title>"
            f"<link>{item['url']}</link>"
            f"<source>{item['source']}</source>"
            f"<guid>{item['url']}</guid></item>"
        )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
<title>{SITE_TITLE}</title>
<link>{SITE_URL}/</link>
<description>{SITE_DESC}</description>
<language>zh-CN</language>
<atom:link href="{SITE_URL}/rss.xml" rel="self" type="application/rss+xml"/>
{item_xml}
</channel>
</rss>"""


# ═══════════════════════════════════════════════════════════
#  构建主函数
# ═══════════════════════════════════════════════════════════

def build():
    repo_root  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(repo_root, "site")
    daily_dir  = os.path.join(output_dir, "daily")

    for d in [output_dir, daily_dir]:
        os.makedirs(d, exist_ok=True)

    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # 为每条新闻注入当天日期
    items = []
    for n in DEMO_NEWS:
        item = dict(n)
        item["date"] = date_str
        items.append(item)

    # ── 首页 ──
    html = gen_index(items, date_str)
    with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] index.html")

    # ── 今日详情页 ──
    daily_html = gen_index(items, date_str, prefix="../")
    with open(os.path.join(daily_dir, f"{date_str}.html"), "w", encoding="utf-8") as f:
        f.write(daily_html)
    print(f"[OK] daily/{date_str}.html")

    # ── 归档页 ──
    archive = gen_archive({date_str: items})
    with open(os.path.join(output_dir, "archive.html"), "w", encoding="utf-8") as f:
        f.write(archive)
    print(f"[OK] archive.html")

    # ── 关于页 ──
    about = gen_about()
    with open(os.path.join(output_dir, "about.html"), "w", encoding="utf-8") as f:
        f.write(about)
    print(f"[OK] about.html")

    # ── RSS ──
    rss = gen_rss(items, date_str)
    with open(os.path.join(output_dir, "rss.xml"), "w", encoding="utf-8") as f:
        f.write(rss)
    print(f"[OK] rss.xml")

    # ── 复制静态资源 ──
    for folder in ["css", "js"]:
        src = os.path.join(repo_root, folder)
        dst = os.path.join(output_dir, folder)
        if os.path.exists(src):
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
    print(f"[OK] css/ + js/")

    # ── .nojekyll ──
    with open(os.path.join(output_dir, ".nojekyll"), "w") as f:
        pass

    print(f"[DONE] 站点构建完成 — {date_str}")


if __name__ == "__main__":
    build()
