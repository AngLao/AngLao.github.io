"""
全球新闻日报 — 后端构建脚本
仅负责: 生成数据 JSON + RSS + 复制前端文件到 site/
"""
import os, json, shutil
from datetime import datetime, timezone

# ── 示例新闻数据 ────────────────────────────────────────
DEMO_NEWS = [
    {"title":"联合国大会通过全球人工智能治理决议","summary":"联合国大会以压倒性多数票通过首个全球人工智能治理框架决议，旨在确保AI技术发展符合人权和可持续发展目标。","source":"Reuters","cat":"Technology","url":"#"},
    {"title":"美联储维持利率不变 暗示年内可能降息","summary":"美联储连续第三次会议维持基准利率不变，但最新点阵图显示年内仍有两次降息空间，市场反应积极。","source":"Bloomberg","cat":"Economy","url":"#"},
    {"title":"巴黎气候峰会达成新减排协议","summary":"经过两周艰苦谈判，190多个国家在巴黎气候峰会上达成新的全球减排协议，承诺在2035年前将碳排放减少60%。","source":"BBC News","cat":"Environment","url":"#"},
    {"title":"SpaceX星舰第五次试飞成功回收助推器","summary":"SpaceX星舰完成第五次轨道试飞，超重型助推器首次实现发射台机械臂精准捕获回收。","source":"CNN","cat":"Technology","url":"#"},
    {"title":"世界杯预选赛：中国队客场逆转取胜","summary":"亚洲区世界杯预选赛，中国队在先失一球的情况下连入两球逆转击败对手，出线形势大好转。","source":"新华社","cat":"Sports","url":"#"},
    {"title":"全球贸易反弹：WTO上调今年贸易增长预期","summary":"世界贸易组织将2024年全球货物贸易增长预期从2.6%上调至3.3%，亚洲出口表现尤为强劲。","source":"Financial Times","cat":"Economy","url":"#"},
    {"title":"诺贝尔文学奖揭晓：挪威作家获奖","summary":"瑞典文学院宣布将本年度诺贝尔文学奖授予挪威作家，表彰其以诗意的笔触探索人类存在的边界。","source":"The Guardian","cat":"Culture","url":"#"},
    {"title":"科学家发现新型抗生素可杀死超级细菌","summary":"国际研究团队利用AI技术从数百万化合物中筛选出一种全新抗生素，对多种耐药超级细菌有效。","source":"Nature","cat":"Science","url":"#"},
    {"title":"美国大选：两党候选人在关键摇摆州展开最后冲刺","summary":"距离美国大选仅剩数周，两党候选人在宾夕法尼亚、密歇根等关键摇摆州密集造势。","source":"Associated Press","cat":"Politics","url":"#"},
    {"title":"全球可再生能源装机容量创历史新高","summary":"国际能源署报告显示，今年全球新增可再生能源装机容量将首次超过500GW。","source":"Al Jazeera","cat":"Environment","url":"#"},
    {"title":"Apple发布新一代芯片M4：AI算力提升3倍","summary":"Apple正式发布M4芯片，采用台积电3nm工艺，神经引擎算力较M3提升3倍。","source":"The Verge","cat":"Technology","url":"#"},
    {"title":"欧盟通过对华电动汽车反补贴关税","summary":"欧盟成员国投票通过对从中国进口的电动汽车征收最高45%的反补贴关税。","source":"South China Morning Post","cat":"Politics","url":"#"},
    {"title":"奥运会：巴黎2024圆满落幕 中国金牌数创境外最佳","summary":"巴黎奥运会正式闭幕，中国代表团以42金27银23铜的成绩位列金牌榜第二。","source":"央视新闻","cat":"Sports","url":"#"},
    {"title":"全球央行数字货币竞赛加速：120国进入研发阶段","summary":"国际清算银行报告显示，目前已有超过120个国家和地区进入央行数字货币的研发或试点阶段。","source":"Nikkei Asia","cat":"Economy","url":"#"},
    {"title":"威尼斯双年展中国馆开幕 聚焦传统与当代对话","summary":"第60届威尼斯双年展中国馆正式开幕，呈现传统水墨与数字艺术的跨界融合。","source":"澎湃新闻","cat":"Culture","url":"#"},
    {"title":"基因编辑疗法首次获批用于儿童遗传病治疗","summary":"美国FDA首次批准一种基于CRISPR基因编辑技术的药物用于治疗儿童罕见遗传病。","source":"Deutsche Welle","cat":"Science","url":"#"},
    {"title":"全球气候异常：多地夏季极端高温破历史记录","summary":"今年夏季全球多地遭遇前所未有的极端高温天气，南欧和南亚部分地区气温突破50°C。","source":"France 24","cat":"Environment","url":"#"},
    {"title":"中东和平谈判在挪威重启 各方释放积极信号","summary":"经挪威斡旋，中东和平谈判在奥斯陆重启，各方代表首次就长期停火框架进行实质性讨论。","source":"Al Jazeera","cat":"World","url":"#"},
    {"title":"NBA总决赛：掘金队以4-2击败热火成功卫冕","summary":"丹佛掘金队在NBA总决赛第六场中以112-98击败迈阿密热火队，以4-2总比分成功卫冕总冠军。","source":"ESPN","cat":"Sports","url":"#"},
    {"title":"全球粮食安全峰会召开 承诺100亿美元援助","summary":"联合国粮农组织召开全球粮食安全峰会，20国集团承诺提供100亿美元援助。","source":"The New York Times","cat":"World","url":"#"},
]

CAT_ORDER = ["World","Politics","Economy","Technology","Science","Environment","Sports","Culture"]


def build():
    repo_root  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    frontend   = os.path.join(repo_root, "frontend")
    output_dir = os.path.join(repo_root, "site")
    data_dir   = os.path.join(output_dir, "data")

    os.makedirs(data_dir, exist_ok=True)
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # 注入日期
    items = []
    for n in DEMO_NEWS:
        item = dict(n)
        item["date"] = date_str
        items.append(item)

    # ── news.json ───────────────────────────────────
    grouped = {c: [] for c in CAT_ORDER}
    for item in items:
        cat = item.get("cat", "World")
        if cat in grouped:
            grouped[cat].append(item)

    news_json = {
        "date": date_str,
        "stats": {
            "total": len(items),
            "sources": len(set(i["source"] for i in items))
        },
        "items": items,
        "categories": {k: v for k, v in grouped.items() if v}
    }
    with open(os.path.join(data_dir, "news.json"), "w", encoding="utf-8") as f:
        json.dump(news_json, f, ensure_ascii=False, indent=2)
    print(f"[OK] data/news.json")

    # ── archive.json ────────────────────────────────
    archive_json = {"dates": [date_str]}
    with open(os.path.join(data_dir, "archive.json"), "w", encoding="utf-8") as f:
        json.dump(archive_json, f, ensure_ascii=False, indent=2)
    print(f"[OK] data/archive.json")

    # ── rss.xml ─────────────────────────────────────
    item_xml = ""
    for item in items[:30]:
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

    # ── 复制前端文件 ────────────────────────────────
    if os.path.exists(output_dir):
        # 清理 site/（保留刚生成的 data/ 和 rss.xml）
        for name in os.listdir(output_dir):
            p = os.path.join(output_dir, name)
            if name == "data" or name == "rss.xml":
                continue
            if os.path.isdir(p):
                shutil.rmtree(p)
            else:
                os.remove(p)

    for name in os.listdir(frontend):
        src = os.path.join(frontend, name)
        dst = os.path.join(output_dir, name)
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
    print(f"[OK] frontend/ → site/")

    # ── .nojekyll ───────────────────────────────────
    with open(os.path.join(output_dir, ".nojekyll"), "w") as f:
        pass

    print(f"[DONE] 站点构建完成 — {date_str}")


if __name__ == "__main__":
    build()
