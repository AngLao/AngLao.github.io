import os, json, shutil
from datetime import datetime, timezone
from .news_sources import NEWS_SOURCES, CATEGORIES, CATEGORY_ORDER, CATEGORY_KEYWORDS
from .news_fetcher import run as fetch_news, NewsItem
from .markdown_brief import generate as gen_markdown

# SVG icons inline
SVG = {
    "globe": '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>',
    "newspaper": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2Zm0 0a2 2 0 0 1-2-2v-9h2"/><path d="M18 14h-8"/><path d="M15 18h-5"/><path d="M10 6h8v4h-8V6Z"/></svg>',
    "calendar": '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>',
}

def header(current="index", prefix=""):
    pages={"index":"棣栭〉","archive":"褰掓。","about":"鍏充簬"}
    nav="".join(f'<a href="{prefix}{"" if k=="index" else k+".html"}" class="nav-item{" active" if k==current else ""}">{v}</a>' for k,v in pages.items())
    return f'<header class="site-header"><div class="header-inner"><a href="{prefix}index.html" class="logo"><span class="logo-icon">{SVG["newspaper"]}</span><span class="logo-text">鍏ㄧ悆鏂伴椈鏃ユ姤</span></a><nav class="main-nav">{nav}</nav></div></header>'

def footer(prefix=""):
    return f'<footer class="site-footer"><div class="footer-inner"><p>鍏ㄧ悆鏂伴椈鏃ユ姤 - 姣忔棩鑷姩鑱氬悎鑷?0+瀹跺浗闄呬富娴佸獟浣?/p><p class="footer-links"><a href="{prefix}archive.html">鍏ㄩ儴褰掓。</a> - <a href="{prefix}rss.xml">RSS璁㈤槄</a> - <a href="{prefix}about.html">鍏充簬</a></p><p class="footer-legal">鏂伴椈鍐呭鐗堟潈褰掑師濮嬫潵婧愭墍鏈?- 鑷姩鐢熸垚浜?{datetime.now(timezone.utc).strftime("%Y-%m-%d")}</p></div></footer>'

def page(title, body, current="index", extra="", prefix=""):
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} - 鍏ㄧ悆鏂伴椈鏃ユ姤</title>
<meta name="description" content="姣忔棩鍏ㄧ悆鏂伴椈鑱氬悎 - 鏉ヨ嚜50+鍥介檯涓绘祦濯掍綋鐨勭簿閫夋柊闂?>
<link rel="stylesheet" href="{prefix}css/style.css">
<link rel="alternate" type="application/rss+xml" title="鍏ㄧ悆鏂伴椈鏃ユ姤" href="{prefix}rss.xml">
{extra}
</head>
<body>
{header(current, prefix)}
<main class="main-content">
{body}
</main>
{footer(prefix)}
<script src="{prefix}js/main.js"></script>
</body>
</html>'''

def news_card(item, large=False):
    cat_html="".join(f'<span class="cat-badge" style="--cat-color:{CATEGORIES.get(c,"color"):"#6b7280"}">{CATEGORIES.get(c,{"label":c})["label"]}</span>' for c in item.categories[:2])
    time_str=item.published[:10] if len(item.published)>=10 else ""
    src_cn=""
    for s in NEWS_SOURCES:
        if s["name"]==item.source_name: src_cn=f" ({s.get('name_cn','')})"; break
    cls="news-card large" if large else "news-card"
    summary=f'<p class="news-summary">{item.summary[:200]}{"..." if len(item.summary)>200 else ""}</p>' if item.summary and large else ""
    return f'''<article class="{cls}"><div class="news-body">
<h3 class="news-title"><a href="{item.url}" target="_blank" rel="noopener">{item.title}</a></h3>
<div class="news-meta">{cat_html}<span class="source">\u260e {item.source_name}{src_cn}</span><span class="time">{SVG["calendar"]} {time_str}</span></div>
{summary}</div></article>'''

def cat_section(cat, items):
    if not items: return ""
    info=CATEGORIES.get(cat,{"label":cat,"color":"#6b7280"})
    cards="\n".join(news_card(item) for item in items[:12])
    return f'''<section class="cat-section" data-category="{cat}">
<h2 class="cat-heading" style="--cat-color:{info["color"]}">{info["label"]}<span class="count">{len(items)}</span></h2>
<div class="news-grid">{cards}</div>
</section>'''

def gen_index(items, date_str, prefix=""):
    top=items[:5]
    top_cards="\n".join(news_card(i,True) for i in top)
    grouped={cat:[] for cat in CATEGORY_ORDER}
    for item in items:
        cat=item.categories[0] if item.categories else "World"
        if cat in grouped: grouped[cat].append(item)
    cat_html="\n".join(cat_section(cat,grouped[cat]) for cat in CATEGORY_ORDER if grouped[cat])
    stats=f"鍏?{len(items)} 鏉℃柊闂?- 鏉ヨ嚜 {len(set(i.source_name for i in items))} 瀹跺獟浣?
    body=f'''<section class="hero"><div class="hero-icon">{SVG["globe"]}</div>
<h1>鍏ㄧ悆鏂伴椈鏃ユ姤</h1><p>{date_str}</p><p style="font-size:.85rem;color:#94a3b8">{stats}</p></section>
<section class="top-stories"><h2 class="section-title">\u2605 浠婃棩瑕侀椈</h2><div class="top-grid">{top_cards}</div></section>
{cat_html}'''
    return page(date_str, body, prefix=prefix)

def gen_about():
    srcs="\n".join(f'<li><strong>{s["name"]}</strong> ({s.get("name_cn","")}) - {s.get("region","")}</li>' for s in NEWS_SOURCES)
    body=f'''<section class="about-page"><h1>鍏充簬鍏ㄧ悆鏂伴椈鏃ユ姤</h1><div class="about-content">
<p>鏈」鐩瘡鏃ヨ嚜鍔ㄨ仛鍚堟潵鑷叏鐞?0+瀹朵富娴佸獟浣撶殑鏂伴椈澶存潯锛屾兜鐩栨斂娌汇€佺粡娴庛€佺鎶€銆佺幆澧冦€佷綋鑲茬瓑澶氫釜棰嗗煙銆?/p>
<p>鐢?Python 鑴氭湰鎶撳彇 RSS feed锛岄€氳繃 GitHub Actions 姣忔棩鑷姩杩愯锛屾瀯寤洪潤鎬佺綉绔欏苟鎵樼浜?GitHub Pages銆?/p>
<h2>鎶€鏈爤</h2><ul><li>Python: feedparser, aiohttp, BeautifulSoup4</li><li>GitHub Actions - UTC 00:00 姣忔棩杩愯</li><li>GitHub Pages 闈欐€佹墭绠?/li><li>绾墠绔?HTML + CSS + JS锛岄浂渚濊禆</li></ul>
<h2>鏁版嵁鏉ユ簮锛坽len(NEWS_SOURCES)}瀹跺獟浣擄級</h2><ul class="source-list">{srcs}</ul></div></section>'''
    return page("鍏充簬",body,"about",'<meta name="robots" content="all">')

def gen_archive(items_by_day):
    months={}
    for d in sorted(items_by_day.keys(),reverse=True):
        months.setdefault(d[:7],[]).append(d)
    month_sections = []
    for ym, days in sorted(months.items(), reverse=True):
        day_links = "".join(f"<a href='daily/{d}.html' class='archive-day'>{d}</a>" for d in days)
        month_sections.append(f'<section class="archive-month"><h2>{ym}</h2><div class="archive-days">{day_links}</div></section>')
    blocks = "".join(month_sections)
    body=f'''<section class="archive-page"><h1>鏂伴椈褰掓。</h1><p class="archive-count">鍏?{len(items_by_day)} 鏈熸棩鎶?/p>{blocks}</section>'''
    return page("鏂伴椈褰掓。",body,"archive",'<meta name="robots" content="all">')

def gen_rss(items_by_day):
    latest=sorted(items_by_day.keys(),reverse=True)[0] if items_by_day else ""
    today=items_by_day.get(latest,[])
    xml_items="".join(f'<item><title><![CDATA[{item.title}]]></title><link>{item.url}</link><source>{item.source_name}</source><guid>{item.url}</guid></item>' for item in today[:30])
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel><title>鍏ㄧ悆鏂伴椈鏃ユ姤</title><link>https://AngLao.github.io/</link><description>姣忔棩鍏ㄧ悆鏂伴椈鑱氬悎</description><language>zh-CN</language>
<atom:link href="https://AngLao.github.io/rss.xml" rel="self" type="application/rss+xml"/>{xml_items}</channel></rss>'''

def save_json(items, path):
    data=[{"id":i.id,"title":i.title,"summary":i.summary,"url":i.url,"source_name":i.source_name,"published":i.published,"categories":i.categories,"img_url":i.img_url,"language":i.language} for i in items]
    with open(path,"w",encoding="utf-8") as f: json.dump(data,f,ensure_ascii=False,indent=2)

def build():
    repo_root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir=os.path.join(repo_root, "site")
    daily_dir=os.path.join(output_dir,"daily")
    data_dir=os.path.join(repo_root,"content","daily")
    briefs_dir=os.path.join(repo_root,"content","briefs")
    for d in [output_dir,daily_dir,data_dir,briefs_dir]:
        os.makedirs(d,exist_ok=True)

    date_str=datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # 鎶撳彇鏂伴椈
    print(f"[*] 鎶撳彇鏂伴椈涓?..")
    items=fetch_news()
    print(f"[+] 鑾峰彇鍒?{len(items)} 鏉℃柊闂?)

    # 淇濆瓨 JSON 鏁版嵁
    save_json(items,os.path.join(data_dir,f"{date_str}.json"))
    print(f"[OK] JSON 宸蹭繚瀛樺埌 content/daily/{date_str}.json")

    # 鐢熸垚 Markdown 绠€鎶?
    md_path=gen_markdown(items,date_str,briefs_dir)
    print(f"[OK] Markdown 绠€鎶?{md_path}")

    # 鐢熸垚绱㈠紩椤甸潰
    idx=gen_index(items,date_str)
    with open(os.path.join(output_dir,"index.html"),"w",encoding="utf-8") as f:
        f.write(idx)
    print(f"[OK] index.html - {len(items)} 鏉℃柊闂?)

    # 鐢熸垚浠婃棩璇︽儏椤?
    items_by_day={date_str:items}
    arch_data=load_meta(data_dir)
    for d in arch_data:
        p=os.path.join(data_dir,f"{d}.json")
        if os.path.exists(p) and d!=date_str:
            with open(p,"r",encoding="utf-8") as f:
                raw=json.load(f)
                items_by_day[d]=[NewsItem(**r) if isinstance(r,dict) else r for r in raw]
    arch_data.append(date_str)
    with open(os.path.join(data_dir,"meta.json"),"w",encoding="utf-8") as f:
        json.dump(sorted(set(arch_data)),f,ensure_ascii=False)

    # 鏃ユ姤鐙珛璇︽儏椤?
    daily_page=gen_index(items,date_str,prefix="../")
    with open(os.path.join(daily_dir,f"{date_str}.html"),"w",encoding="utf-8") as f:
        f.write(daily_page)
    print(f"[OK] daily/{date_str}.html")

    # 褰掓。椤?
    arch=gen_archive(items_by_day)
    with open(os.path.join(output_dir,"archive.html"),"w",encoding="utf-8") as f:
        f.write(arch)

    # 鍏充簬椤?
    about=gen_about()
    with open(os.path.join(output_dir,"about.html"),"w",encoding="utf-8") as f:
        f.write(about)

    # RSS
    rss=gen_rss(items_by_day)
    with open(os.path.join(output_dir,"rss.xml"),"w",encoding="utf-8") as f:
        f.write(rss)
    print(f"[OK] rss.xml")

    # 澶嶅埗闈欐€佽祫婧?
    for folder in ["css","js"]:
        src_dir=os.path.join(repo_root,folder)
        dst_dir=os.path.join(output_dir,folder)
        if os.path.exists(src_dir):
            if os.path.exists(dst_dir):
                shutil.rmtree(dst_dir)
            shutil.copytree(src_dir,dst_dir)
    print(f"[OK] 闈欐€佽祫婧愬凡澶嶅埗")

    # .nojekyll
    with open(os.path.join(output_dir,".nojekyll"),"w") as f:
        pass

    print(f"[DONE] 绔欑偣鏋勫缓瀹屾垚 - {date_str}")

def load_meta(data_dir):
    p=os.path.join(data_dir,"meta.json")
    if os.path.exists(p):
        with open(p,"r",encoding="utf-8") as f: return json.load(f)
    return []

if __name__=="__main__":
    build()



# trigger rebuild
