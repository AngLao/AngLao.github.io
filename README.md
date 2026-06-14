# 全球新闻日报

每日自动聚合来自 **50 个高质量 RSS 源** 的中文新闻头条，生成静态网站并通过 GitHub Pages 发布。

## 架构

```
50 RSS 源 (中文为主)
       │
       ▼  aiohttp 异步并发抓取
┌──────────────┐
│  fetcher.py  │  抓取 → 去重 → 重要性评分 → 分类
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  build.py    │  编排：归档数据 → 生成 JSON → 输出站点
└──────┬───────┘
       │
  ┌────┴────┐
  ▼         ▼
content/   site/
 data/      ├── index.html  ← 从 frontend/ 复制
 (Git持久化) ├── archive.html
            ├── about.html
            ├── css/ js/   ← 前端资源
            ├── data/
            │   ├── news.json      今日新闻
            │   ├── archive.json   归档日期列表
            │   └── daily/         每日详情 JSON
            ├── daily/             每日详情 HTML
            └── rss.xml
```

## 快速开始

### 1. 创建仓库

```bash
git clone https://github.com/你的用户名/你的仓库.git
cd 你的仓库
# 复制本项目全部文件后推送
git add .
git commit -m "init: 全球新闻日报"
git push
```

### 2. 启用 GitHub Pages

仓库 Settings → Pages → Source: **GitHub Actions**

### 3. 手动触发

Actions → 每日新闻聚合与部署 → Run workflow

### 4. 访问

`https://你的用户名.github.io/`

## 项目结构

```
├── src/
│   ├── sources.py       # 50 个 RSS 源定义 + 分类关键词
│   ├── fetcher.py       # 异步抓取引擎 (aiohttp + feedparser)
│   ├── funny.py         # 搞笑无厘头新闻生成器
│   └── build.py         # 构建脚本 (归档 + 生成 JSON + 输出站点)
├── frontend/            # 前端 (前后端分离)
│   ├── index.html       # 首页 (JS 数据驱动渲染)
│   ├── archive.html     # 归档页
│   ├── about.html       # 关于页
│   ├── css/style.css    # 现代扁平化设计 + 暗色模式
│   └── js/main.js       # Vanilla JS 渲染引擎
├── content/data/        # 新闻归档 (Git 持久化)
├── .github/workflows/   # CI 自动化
└── requirements.txt
```

## 新闻源 (50家)

| 类别 | 数量 | 代表 |
|------|------|------|
| 央媒/官方 | 6 | 新华社、央视、人民日报、参考消息 |
| 商业门户 | 5 | 新浪、腾讯、网易、搜狐、凤凰 |
| 严肃媒体 | 6 | 澎湃、财新、界面、新京报、南方周末 |
| 财经 | 5 | 第一财经、华尔街见闻、36氪、虎嗅 |
| 科技 | 5 | IT之家、品玩、量子位、机器之心 |
| 中文国际 | 8 | BBC中文、NYT中文、FT中文、DW中文、日经中文 |
| 垂直领域 | 6 | 环球科学、果壳、虎扑、豆瓣、好奇心日报 |
| 全球英文 | 6 | Reuters、AP、Al Jazeera、Guardian、Bloomberg |
| 地方媒体 | 3 | 上观新闻、南方都市报、北京日报 |

## 分类体系

| 分类 | 优先级 | 颜色 |
|------|--------|------|
| 时政 | ★★★★★ | 🔴 |
| 财经 | ★★★★★ | 🟢 |
| 国际 | ★★★★★ | 🔵 |
| 科技 | ★★★★ | 🔵 |
| 科学 | ★★★★ | 🟣 |
| 军事 | ★★★★ | 🟤 |
| 体育 | ★★★ | 🟠 |
| 文化 | ★★★ | 🩷 |
| 😂 搞笑无厘头 | — | 🟡 底部彩蛋 |

### 重要性过滤

每条新闻通过关键词匹配评分（至少命中 2 个关键词才入选），同时结合来源权威度加权，确保只展示真正重要的新闻。

## 自动化

- **时间**: 每天北京时间 12:00 (UTC 04:00)
- **流程**: 抓取 → 归档提交 → 构建 → 部署
- **归档**: 每日新闻数据自动提交到 `content/data/`，永久保存

## 技术栈

| 层 | 技术 |
|----|------|
| 后端 | Python · aiohttp · feedparser · BeautifulSoup4 |
| 前端 | 纯 HTML + CSS + JS · 零框架 |
| CI/CD | GitHub Actions · GitHub Pages |
| 设计 | CSS 变量 · 暗色模式 · 响应式 |
