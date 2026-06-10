NEWS_SOURCES = [
    {"name":"Reuters","name_cn":"路透社","region":"Global","rss":"","url":"https://www.reuters.com","lang":"en","focus":["World","Economy"]},
    {"name":"Associated Press","name_cn":"美联社","region":"Global","rss":"","url":"https://apnews.com","lang":"en","focus":["World","Politics"]},
    {"name":"BBC News","name_cn":"BBC新闻","region":"Global","rss":"https://feeds.bbci.co.uk/news/world/rss.xml","url":"https://www.bbc.com/news","lang":"en","focus":["World","Politics","Technology","Science"]},
    {"name":"CNN","name_cn":"CNN","region":"Global","rss":"http://rss.cnn.com/rss/edition.rss","url":"https://www.cnn.com","lang":"en","focus":["World","Politics"]},
    {"name":"Al Jazeera","name_cn":"半岛电视台","region":"Global","rss":"https://www.aljazeera.com/xml/rss/all.xml","url":"https://www.aljazeera.com","lang":"en","focus":["World","Politics"]},
    {"name":"The New York Times","name_cn":"纽约时报","region":"North America","rss":"https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml","url":"https://www.nytimes.com","lang":"en","focus":["World","Politics","Economy"]},
    {"name":"The Guardian","name_cn":"卫报","region":"Europe","rss":"https://www.theguardian.com/world/rss","url":"https://www.theguardian.com","lang":"en","focus":["World","Politics","Environment"]},
    {"name":"Bloomberg","name_cn":"彭博社","region":"North America","rss":"https://feeds.bloomberg.com/markets/news.rss","url":"https://www.bloomberg.com","lang":"en","focus":["Economy","Technology"]},
    {"name":"Reuters","name_cn":"路透社","region":"Global","rss":"https://www.reuters.com/tools/rss","url":"https://www.reuters.com","lang":"en","focus":["World","Economy","Politics"]},
    {"name":"The Wall Street Journal","name_cn":"华尔街日报","region":"North America","rss":"https://feeds.a.dj.com/rss/RSSWorldNews.xml","url":"https://www.wsj.com","lang":"en","focus":["Economy","World"]},
    {"name":"NPR","name_cn":"美国国家公共广播","region":"North America","rss":"https://feeds.npr.org/1001/rss.xml","url":"https://www.npr.org","lang":"en","focus":["World","Politics","Culture"]},
    {"name":"South China Morning Post","name_cn":"南华早报","region":"Asia","rss":"https://www.scmp.com/rss/4/feed","url":"https://www.scmp.com","lang":"en","focus":["World","Asia","Politics"]},
    {"name":"Nikkei Asia","name_cn":"日经亚洲","region":"Asia","rss":"https://asia.nikkei.com/rss/feed","url":"https://asia.nikkei.com","lang":"en","focus":["Economy","Asia","Technology"]},
    {"name":"Xinhua News","name_cn":"新华社","region":"China","rss":"https://english.news.cn/rss/world.xml","url":"https://english.news.cn","lang":"en","focus":["World","China","Politics"]},
    {"name":"环球网","name_cn":"环球网","region":"China","rss":"https://www.huanqiu.com/rss/world.xml","url":"https://www.huanqiu.com","lang":"zh","focus":["World","China","Politics"]},
    {"name":"澎湃新闻","name_cn":"澎湃新闻","region":"China","rss":"https://www.thepaper.cn/rss/world.xml","url":"https://www.thepaper.cn","lang":"zh","focus":["World","China","Politics"]},
    {"name":"The Economist","name_cn":"经济学人","region":"North America","rss":"https://www.economist.com/feeds/print-sections/77/international.xml","url":"https://www.economist.com","lang":"en","focus":["Economy","World"]},
    {"name":"Financial Times","name_cn":"金融时报","region":"Europe","rss":"https://www.ft.com/rss/home","url":"https://www.ft.com","lang":"en","focus":["Economy","World"]},
    {"name":"France 24","name_cn":"法国24台","region":"Global","rss":"https://www.france24.com/en/rss","url":"https://www.france24.com","lang":"en","focus":["World","Politics"]},
    {"name":"Deutsche Welle","name_cn":"德国之声","region":"Global","rss":"https://rss.dw.com/rdf/rss-en-all","url":"https://www.dw.com","lang":"en","focus":["World","Politics","Culture"]},
]
CATEGORIES = {"World":{"label":"国际","color":"#0891b2"},"Politics":{"label":"政治","color":"#dc2626"},"Economy":{"label":"经济","color":"#059669"},"Technology":{"label":"科技","color":"#2563eb"},"Science":{"label":"科学","color":"#7c3aed"},"Environment":{"label":"环境","color":"#16a34a"},"Sports":{"label":"体育","color":"#ea580c"},"Culture":{"label":"文化","color":"#d946ef"}}
CATEGORY_ORDER = ["World","Politics","Economy","Technology","Science","Environment","Sports","Culture"]
CATEGORY_KEYWORDS = {
    "Politics":["president","election","government","minister","congress","vote","sanction","白宫","总统","选举","政府","外交","峰会"],
    "Economy":["market","stock","trade","inflation","gdp","economic","bank","利率","经济","股市","通胀","贸易","油价"],
    "Technology":["AI","artificial intelligence","chatgpt","openai","chip","quantum","space","rocket","人工智能","芯片","科技","航天"],
    "Science":["research","study","dna","gene","cancer","vaccine","discovery","科学","研究","基因","发现"],
    "Environment":["climate","carbon","emission","renewable","solar","wind","environment","pollution","环境","气候","碳排放","环保"],
    "Sports":["olympic","world cup","championship","football","soccer","basketball","tennis","nba","体育","奥运","世界杯","冠军"],
    "Culture":["film","movie","music","art","exhibition","award","book","museum","电影","文化","艺术","音乐","展览"],
}
