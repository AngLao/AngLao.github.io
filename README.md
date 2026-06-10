# 全球新闻日报

每日自动聚合自全球 **50+ 家主流媒体** 的头条新闻，生成结构化的 **Markdown 简报** 和 **HTML 静态网站**，通过 GitHub Pages 发布。

## 架构概览

```
                    ┌──────────────┐
                    │  50+ RSS源   │
                    │ (全球媒体)   │
                    └──────┬───────┘
                           │ feedparser + aiohttp
                    ┌──────▼───────┐
                    │  news_fetcher │  抓取 → 去重 → 分类
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
      ┌───────────┐ ┌──────────┐ ┌──────────┐
      │ Markdown  │ │  HTML    │ │  JSON    │
      │ 简报      │ │ 静态站   │ │ 结构化   │
      └───────────┘ └────┬─────┘ └──────────┘
                         │ GitHub Pages
                    ┌────▼─────┐
                    │ 网站访问  │
                    └──────────┘
```

## 已收录的媒体源 (50家)

涵盖 **Global (路透/AP/BBC/CNN/半岛/法广/德声/欧洲台)** · **北美 (NYT/WP/WSJ/Bloomberg/NPR/LA Times/USA Today/ABC/CBS/Guardian US/Economist/Time/Forbes)** · **欧洲 (Guardian UK/Telegraph/Independent/FT/Le Monde/El Pais/Spiegel/Irish Times/The Times)** · **亚太 (SCMP/Straits Times/Japan Times/Nikkei/The Hindu/Times of India/Korea Herald/Asahi)** · **中国 (新华社/央视/环球网/澎湃/观察者/新浪/腾讯/参考消息)** · **大洋洲 (SMH)**

## 快速开始

### 1. 创建 GitHub 仓库

访问 https://github.com/new 新建一个仓库，例如 `daily-news`，然后：

```bash
# 克隆到本地
git clone https://github.com/你的用户名/daily-news.git
cd daily-news

# 复制本项目所有文件到这个目录
# 然后推送
git add .
git commit -m "init: 全球新闻日报项目"
git push
```

### 2. 启用 GitHub Pages

1. 在仓库 Settings → Pages 中：
   - Source: **GitHub Actions**
2. 本项目自带 Actions workflow，首次运行后会自动部署

### 3. 首次手动触发

在仓库 Actions 页面找到 **每日新闻聚合与部署**，点击 `Run workflow` 手动触发一次

### 4. 访问网站

部署完成后访问：`https://你的用户名.github.io/daily-news/`

### 5. 查看 Markdown 简报

每次运行后，Markdown 文件会保存在 `content/briefs/` 目录下

## 项目结构

```
├── .github/workflows/
│   └── daily-news.yml      # GitHub Actions 自动化
├── src/
│   ├── news_sources.py      # 50家媒体源定义 + 分类系统
│   ├── news_fetcher.py      # RSS 抓取引擎
│   ├── markdown_brief.py    # Markdown 简报生成
│   └── build_site.py        # HTML 站点构建器
├── site/                    # 生成的静态网站
│   ├── index.html           # 首页
│   ├── archive.html         # 归档页
│   ├── about.html           # 关于页
│   ├── rss.xml              # RSS feed
│   ├── css/style.css        # 样式
│   ├── js/main.js           # 交互脚本
│   └── daily/               # 每日详情页
├── content/                 # 数据
│   ├── briefs/              # Markdown 简报
│   └── daily/               # JSON 结构化数据
└── requirements.txt         # Python 依赖
```

## 自定义

- **修改新闻源**: 编辑 `src/news_sources.py` 中的 `NEWS_SOURCES` 列表
- **调整分类**: 编辑 `CATEGORY_KEYWORDS` 和 `CATEGORY_ORDER`
- **修改更新频率**: 编辑 `.github/workflows/daily-news.yml` 中的 cron 表达式

## 技术栈

- Python: feedparser, aiohttp, BeautifulSoup4
- GitHub Actions: 每日定时运行
- GitHub Pages: 静态托管
- 前端: 纯 HTML + CSS + JS，零依赖
