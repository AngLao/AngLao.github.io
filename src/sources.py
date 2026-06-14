"""
全球前50 RSS 新闻源定义
字段: name, name_cn, region, rss, url, lang, focus
"""

NEWS_SOURCES = [
    # ══════ Global 全球 ══════
    {"name":"Reuters","name_cn":"路透社","region":"Global","rss":"https://www.rss-bridge.org/bridge01/?action=display&bridge=FilterBridge&url=https%3A%2F%2Fwww.reuters.com%2F&content_filter=Reuters&content_filter_type=text&format=Atom","url":"https://www.reuters.com","lang":"en","focus":["World","Economy"]},
    {"name":"Associated Press","name_cn":"美联社","region":"Global","rss":"https://rsshub.app/apnews/topics/apf-topnews","url":"https://apnews.com","lang":"en","focus":["World","Politics"]},
    {"name":"BBC News","name_cn":"BBC新闻","region":"Global","rss":"https://feeds.bbci.co.uk/news/world/rss.xml","url":"https://www.bbc.com/news","lang":"en","focus":["World","Politics","Technology","Science"]},
    {"name":"CNN","name_cn":"CNN","region":"Global","rss":"http://rss.cnn.com/rss/edition.rss","url":"https://www.cnn.com","lang":"en","focus":["World","Politics"]},
    {"name":"Al Jazeera","name_cn":"半岛电视台","region":"Global","rss":"https://www.aljazeera.com/xml/rss/all.xml","url":"https://www.aljazeera.com","lang":"en","focus":["World","Politics"]},
    {"name":"The Guardian","name_cn":"卫报","region":"Global","rss":"https://www.theguardian.com/world/rss","url":"https://www.theguardian.com","lang":"en","focus":["World","Politics","Environment"]},
    {"name":"France 24","name_cn":"法国24台","region":"Global","rss":"https://www.france24.com/en/rss","url":"https://www.france24.com","lang":"en","focus":["World","Politics"]},
    {"name":"Deutsche Welle","name_cn":"德国之声","region":"Global","rss":"https://rss.dw.com/rdf/rss-en-all","url":"https://www.dw.com","lang":"en","focus":["World","Politics","Culture"]},
    {"name":"Euronews","name_cn":"欧洲新闻台","region":"Global","rss":"https://www.euronews.com/rss","url":"https://www.euronews.com","lang":"en","focus":["World","Politics"]},

    # ══════ North America 北美 ══════
    {"name":"The New York Times","name_cn":"纽约时报","region":"North America","rss":"https://rss.nytimes.com/services/xml/rss/nyt/World.xml","url":"https://www.nytimes.com","lang":"en","focus":["World","Politics","Economy"]},
    {"name":"The Washington Post","name_cn":"华盛顿邮报","region":"North America","rss":"https://feeds.washingtonpost.com/rss/world","url":"https://www.washingtonpost.com","lang":"en","focus":["World","Politics"]},
    {"name":"The Wall Street Journal","name_cn":"华尔街日报","region":"North America","rss":"https://feeds.a.dj.com/rss/RSSWorldNews.xml","url":"https://www.wsj.com","lang":"en","focus":["Economy","World"]},
    {"name":"Bloomberg","name_cn":"彭博社","region":"North America","rss":"https://feeds.bloomberg.com/markets/news.rss","url":"https://www.bloomberg.com","lang":"en","focus":["Economy","Technology"]},
    {"name":"NPR","name_cn":"美国国家公共广播","region":"North America","rss":"https://feeds.npr.org/1001/rss.xml","url":"https://www.npr.org","lang":"en","focus":["World","Politics","Culture"]},
    {"name":"Los Angeles Times","name_cn":"洛杉矶时报","region":"North America","rss":"https://www.latimes.com/world/rss2.0.xml","url":"https://www.latimes.com","lang":"en","focus":["World","Politics"]},
    {"name":"USA Today","name_cn":"今日美国","region":"North America","rss":"https://rssfeeds.usatoday.com/usatoday-NewsTopStories","url":"https://www.usatoday.com","lang":"en","focus":["World"]},
    {"name":"ABC News","name_cn":"ABC新闻","region":"North America","rss":"https://abcnews.go.com/abcnews/internationalheadlines","url":"https://abcnews.go.com","lang":"en","focus":["World","Politics"]},
    {"name":"CBS News","name_cn":"CBS新闻","region":"North America","rss":"https://www.cbsnews.com/latest/rss/world","url":"https://www.cbsnews.com","lang":"en","focus":["World","Politics"]},
    {"name":"Time","name_cn":"时代周刊","region":"North America","rss":"https://time.com/rss","url":"https://time.com","lang":"en","focus":["World","Politics"]},
    {"name":"Forbes","name_cn":"福布斯","region":"North America","rss":"https://www.forbes.com/real-time/feed2/","url":"https://www.forbes.com","lang":"en","focus":["Economy","Technology"]},

    # ══════ Europe 欧洲 ══════
    {"name":"Financial Times","name_cn":"金融时报","region":"Europe","rss":"https://www.ft.com/rss/home","url":"https://www.ft.com","lang":"en","focus":["Economy","World"]},
    {"name":"The Telegraph","name_cn":"每日电讯报","region":"Europe","rss":"https://www.telegraph.co.uk/rss.xml","url":"https://www.telegraph.co.uk","lang":"en","focus":["World","Politics"]},
    {"name":"The Independent","name_cn":"独立报","region":"Europe","rss":"https://www.independent.co.uk/news/world/rss","url":"https://www.independent.co.uk","lang":"en","focus":["World","Politics"]},
    {"name":"Le Monde","name_cn":"世界报","region":"Europe","rss":"https://www.lemonde.fr/en/rss/une.xml","url":"https://www.lemonde.fr","lang":"en","focus":["World","Politics"]},
    {"name":"El Pais","name_cn":"国家报","region":"Europe","rss":"https://feeds.elpais.com/mrss-s/pages/ep/site/english.elpais.com/portada","url":"https://english.elpais.com","lang":"en","focus":["World","Politics"]},
    {"name":"Der Spiegel","name_cn":"明镜周刊","region":"Europe","rss":"https://www.spiegel.de/international/index.rss","url":"https://www.spiegel.de","lang":"en","focus":["World","Politics"]},
    {"name":"Irish Times","name_cn":"爱尔兰时报","region":"Europe","rss":"https://www.irishtimes.com/arc/outboundfeeds/v1/feed/?type=section&id=news/world","url":"https://www.irishtimes.com","lang":"en","focus":["World","Politics"]},
    {"name":"The Times","name_cn":"泰晤士报","region":"Europe","rss":"https://www.thetimes.co.uk/?service=rss","url":"https://www.thetimes.co.uk","lang":"en","focus":["World","Politics"]},

    # ══════ Asia Pacific 亚太 ══════
    {"name":"South China Morning Post","name_cn":"南华早报","region":"Asia","rss":"https://www.scmp.com/rss/4/feed","url":"https://www.scmp.com","lang":"en","focus":["World","Asia","Politics"]},
    {"name":"Nikkei Asia","name_cn":"日经亚洲","region":"Asia","rss":"https://asia.nikkei.com/rss/feed/nar","url":"https://asia.nikkei.com","lang":"en","focus":["Economy","Asia","Technology"]},
    {"name":"The Straits Times","name_cn":"海峡时报","region":"Asia","rss":"https://www.straitstimes.com/news/asia/rss.xml","url":"https://www.straitstimes.com","lang":"en","focus":["Asia","World"]},
    {"name":"The Japan Times","name_cn":"日本时报","region":"Asia","rss":"https://www.japantimes.co.jp/feed/top-stories/","url":"https://www.japantimes.co.jp","lang":"en","focus":["Asia","World"]},
    {"name":"The Hindu","name_cn":"印度教徒报","region":"Asia","rss":"https://www.thehindu.com/news/feeder/default.rss","url":"https://www.thehindu.com","lang":"en","focus":["World","Asia"]},
    {"name":"Times of India","name_cn":"印度时报","region":"Asia","rss":"https://timesofindia.indiatimes.com/rssfeeds/296589292.cms","url":"https://timesofindia.indiatimes.com","lang":"en","focus":["World","Asia"]},
    {"name":"Korea Herald","name_cn":"韩国先驱报","region":"Asia","rss":"https://www.koreaherald.com/rss/nation.xml","url":"https://www.koreaherald.com","lang":"en","focus":["Asia","World"]},
    {"name":"Sydney Morning Herald","name_cn":"悉尼先驱晨报","region":"Oceania","rss":"https://www.smh.com.au/rss/world.xml","url":"https://www.smh.com.au","lang":"en","focus":["World"]},
    {"name":"ABC Australia","name_cn":"澳洲广播公司","region":"Oceania","rss":"https://www.abc.net.au/news/feed/51120/rss.xml","url":"https://www.abc.net.au/news","lang":"en","focus":["World","Asia"]},
    {"name":"Bangkok Post","name_cn":"曼谷邮报","region":"Asia","rss":"https://www.bangkokpost.com/rss/topstories.xml","url":"https://www.bangkokpost.com","lang":"en","focus":["Asia","World"]},

    # ══════ China 中国 ══════
    {"name":"Xinhua News","name_cn":"新华社","region":"China","rss":"https://english.news.cn/rss/world.xml","url":"https://english.news.cn","lang":"en","focus":["World","China","Politics"]},
    {"name":"CGTN","name_cn":"中国国际电视台","region":"China","rss":"https://www.cgtn.com/subscribe/rss/section/world.xml","url":"https://www.cgtn.com","lang":"en","focus":["World","China"]},
    {"name":"China Daily","name_cn":"中国日报","region":"China","rss":"https://www.chinadaily.com.cn/rss/world_rss.xml","url":"https://www.chinadaily.com.cn","lang":"en","focus":["World","China"]},
    {"name":"Global Times","name_cn":"环球时报","region":"China","rss":"https://www.globaltimes.cn/rss/topstories.xml","url":"https://www.globaltimes.cn","lang":"en","focus":["World","China","Politics"]},
    {"name":"Sixth Tone","name_cn":"第六声","region":"China","rss":"https://www.sixthtone.com/rss","url":"https://www.sixthtone.com","lang":"en","focus":["China","Politics","Culture"]},

    # ══════ Middle East 中东 ══════
    {"name":"Haaretz","name_cn":"国土报","region":"Middle East","rss":"https://www.haaretz.com/rss/news","url":"https://www.haaretz.com","lang":"en","focus":["World","Politics"]},
    {"name":"Jerusalem Post","name_cn":"耶路撒冷邮报","region":"Middle East","rss":"https://www.jpost.com/rss/rssfeedsfrontpage.aspx","url":"https://www.jpost.com","lang":"en","focus":["World","Politics"]},
    {"name":"Arab News","name_cn":"阿拉伯新闻","region":"Middle East","rss":"https://www.arabnews.com/rss/top-stories","url":"https://www.arabnews.com","lang":"en","focus":["World","Politics"]},

    # ══════ Specialized 专业 ══════
    {"name":"TechCrunch","name_cn":"TechCrunch","region":"North America","rss":"https://techcrunch.com/feed/","url":"https://techcrunch.com","lang":"en","focus":["Technology"]},
    {"name":"Wired","name_cn":"连线杂志","region":"North America","rss":"https://www.wired.com/feed/rss","url":"https://www.wired.com","lang":"en","focus":["Technology","Science"]},
    {"name":"The Verge","name_cn":"The Verge","region":"North America","rss":"https://www.theverge.com/rss/index.xml","url":"https://www.theverge.com","lang":"en","focus":["Technology"]},
    {"name":"Nature","name_cn":"自然杂志","region":"Global","rss":"https://www.nature.com/nature.rss","url":"https://www.nature.com","lang":"en","focus":["Science"]},
    {"name":"Science Daily","name_cn":"每日科学","region":"Global","rss":"https://www.sciencedaily.com/rss/top/science.xml","url":"https://www.sciencedaily.com","lang":"en","focus":["Science"]},
]

CATEGORIES = {
    "World":{"label":"国际","color":"#0891b2"},
    "Politics":{"label":"政治","color":"#dc2626"},
    "Economy":{"label":"经济","color":"#059669"},
    "Technology":{"label":"科技","color":"#2563eb"},
    "Science":{"label":"科学","color":"#7c3aed"},
    "Environment":{"label":"环境","color":"#16a34a"},
    "Sports":{"label":"体育","color":"#ea580c"},
    "Culture":{"label":"文化","color":"#d946ef"},
}
CATEGORY_ORDER = ["World","Politics","Economy","Technology","Science","Environment","Sports","Culture"]

CATEGORY_KEYWORDS = {
    "Politics":["president","election","government","minister","congress","vote","sanction","白宫","总统","选举","政府","外交","峰会","war","military","nato","ukraine","gaza","israel"],
    "Economy":["market","stock","trade","inflation","gdp","economic","bank","利率","经济","股市","通胀","贸易","油价","tariff","fed","central bank","recession"],
    "Technology":["AI","artificial intelligence","chatgpt","openai","chip","quantum","space","rocket","人工智能","芯片","科技","航天","apple","google","microsoft","tesla","startup"],
    "Science":["research","study","dna","gene","cancer","vaccine","discovery","科学","研究","基因","发现","nasa","climate change"],
    "Environment":["climate","carbon","emission","renewable","solar","wind","environment","pollution","环境","气候","碳排放","环保"],
    "Sports":["olympic","world cup","championship","football","soccer","basketball","tennis","nba","体育","奥运","世界杯","冠军"],
    "Culture":["film","movie","music","art","exhibition","award","book","museum","电影","文化","艺术","音乐","展览"],
}

# 类别扩展关键词
CATEGORY_KEYWORDS["World"] = ["world","global","international","nation","border","refugee","treaty","united nations","security council","diplomat"]
