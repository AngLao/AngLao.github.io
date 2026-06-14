"""
中文新闻源定义 — 50个高质量RSS源
侧重: 要闻/时政/财经/科技/国际
"""
NEWS_SOURCES = [
    # ══════ 央媒 / 官方 ══════
    {"name":"新华社","name_cn":"新华社","region":"中国","rss":"https://rsshub.app/xinhua/news","url":"https://www.xinhuanet.com","lang":"zh","weight":10},
    {"name":"央视新闻","name_cn":"央视新闻","region":"中国","rss":"https://rsshub.app/cctv/world","url":"https://news.cctv.com","lang":"zh","weight":10},
    {"name":"人民日报","name_cn":"人民日报","region":"中国","rss":"https://rsshub.app/people/xw","url":"https://www.people.com.cn","lang":"zh","weight":9},
    {"name":"参考消息","name_cn":"参考消息","region":"中国","rss":"https://rsshub.app/cankaoxiaoxi/yaowen","url":"https://www.cankaoxiaoxi.com","lang":"zh","weight":9},
    {"name":"中国新闻网","name_cn":"中国新闻网","region":"中国","rss":"https://rsshub.app/chinanews/scroll","url":"https://www.chinanews.com.cn","lang":"zh","weight":8},
    {"name":"解放军报","name_cn":"解放军报","region":"中国","rss":"https://rsshub.app/81/81rc","url":"https://www.81.cn","lang":"zh","weight":6},

    # ══════ 商业门户 ══════
    {"name":"新浪新闻","name_cn":"新浪新闻","region":"中国","rss":"https://rsshub.app/sina/rollnews","url":"https://news.sina.com.cn","lang":"zh","weight":8},
    {"name":"腾讯新闻","name_cn":"腾讯新闻","region":"中国","rss":"https://rsshub.app/tencent/news/rank/0","url":"https://news.qq.com","lang":"zh","weight":8},
    {"name":"网易新闻","name_cn":"网易新闻","region":"中国","rss":"https://rsshub.app/163/news/rank/whole","url":"https://news.163.com","lang":"zh","weight":7},
    {"name":"搜狐新闻","name_cn":"搜狐新闻","region":"中国","rss":"https://rsshub.app/sohu/mp/1","url":"https://news.sohu.com","lang":"zh","weight":7},
    {"name":"凤凰网","name_cn":"凤凰网","region":"中国","rss":"https://rsshub.app/ifeng/news","url":"https://news.ifeng.com","lang":"zh","weight":8},

    # ══════ 严肃媒体 ══════
    {"name":"澎湃新闻","name_cn":"澎湃新闻","region":"中国","rss":"https://rsshub.app/thepaper/featured","url":"https://www.thepaper.cn","lang":"zh","weight":9},
    {"name":"财新网","name_cn":"财新网","region":"中国","rss":"https://rsshub.app/caixin/latest","url":"https://www.caixin.com","lang":"zh","weight":9},
    {"name":"界面新闻","name_cn":"界面新闻","region":"中国","rss":"https://rsshub.app/jiemian/lists/65","url":"https://www.jiemian.com","lang":"zh","weight":8},
    {"name":"新京报","name_cn":"新京报","region":"中国","rss":"https://rsshub.app/bjnews/recommend","url":"https://www.bjnews.com.cn","lang":"zh","weight":8},
    {"name":"南方周末","name_cn":"南方周末","region":"中国","rss":"https://rsshub.app/infzm/hot","url":"https://www.infzm.com","lang":"zh","weight":8},
    {"name":"三联生活周刊","name_cn":"三联生活周刊","region":"中国","rss":"https://rsshub.app/lifeweek/channel/recommend","url":"https://www.lifeweek.com.cn","lang":"zh","weight":6},

    # ══════ 财经 ══════
    {"name":"第一财经","name_cn":"第一财经","region":"中国","rss":"https://rsshub.app/yicai/brief","url":"https://www.yicai.com","lang":"zh","weight":8},
    {"name":"每日经济新闻","name_cn":"每日经济新闻","region":"中国","rss":"https://rsshub.app/nbd/daily","url":"https://www.nbd.com.cn","lang":"zh","weight":7},
    {"name":"华尔街见闻","name_cn":"华尔街见闻","region":"中国","rss":"https://rsshub.app/wallstreetcn/hot","url":"https://wallstreetcn.com","lang":"zh","weight":8},
    {"name":"36氪","name_cn":"36氪","region":"中国","rss":"https://36kr.com/feed","url":"https://36kr.com","lang":"zh","weight":6},
    {"name":"虎嗅","name_cn":"虎嗅","region":"中国","rss":"https://www.huxiu.com/rss/0.xml","url":"https://www.huxiu.com","lang":"zh","weight":6},

    # ══════ 科技 ══════
    {"name":"IT之家","name_cn":"IT之家","region":"中国","rss":"https://rsshub.app/ithome","url":"https://www.ithome.com","lang":"zh","weight":6},
    {"name":"品玩","name_cn":"品玩","region":"中国","rss":"https://rsshub.app/pingwest/status","url":"https://www.pingwest.com","lang":"zh","weight":5},
    {"name":"量子位","name_cn":"量子位","region":"中国","rss":"https://rsshub.app/qbitai/latest","url":"https://www.qbitai.com","lang":"zh","weight":6},
    {"name":"机器之心","name_cn":"机器之心","region":"中国","rss":"https://rsshub.app/jiqizhixin/latest","url":"https://www.jiqizhixin.com","lang":"zh","weight":6},
    {"name":"InfoQ中国","name_cn":"InfoQ","region":"中国","rss":"https://rsshub.app/infoq/topic/1","url":"https://www.infoq.cn","lang":"zh","weight":5},

    # ══════ 中文国际 ══════
    {"name":"BBC中文","name_cn":"BBC中文","region":"国际","rss":"https://feeds.bbci.co.uk/zhongwen/simp/rss.xml","url":"https://www.bbc.com/zhongwen/simp","lang":"zh","weight":8},
    {"name":"纽约时报中文","name_cn":"纽约时报中文","region":"国际","rss":"https://rsshub.app/nytimes/dual","url":"https://cn.nytimes.com","lang":"zh","weight":8},
    {"name":"FT中文网","name_cn":"FT中文网","region":"国际","rss":"https://rsshub.app/ftchinese/latest","url":"https://www.ftchinese.com","lang":"zh","weight":8},
    {"name":"DW中文","name_cn":"德国之声中文","region":"国际","rss":"https://rss.dw.com/rdf/rss-cn-all","url":"https://www.dw.com/zh","lang":"zh","weight":7},
    {"name":"法广中文","name_cn":"法广中文","region":"国际","rss":"https://rsshub.app/rfi/cn","url":"https://www.rfi.fr/cn","lang":"zh","weight":7},
    {"name":"VOA中文","name_cn":"美国之音中文","region":"国际","rss":"https://rsshub.app/voa/chinese","url":"https://www.voachinese.com","lang":"zh","weight":7},
    {"name":"日经中文网","name_cn":"日经中文网","region":"国际","rss":"https://rsshub.app/nikkei/cn","url":"https://cn.nikkei.com","lang":"zh","weight":7},
    {"name":"韩联社中文","name_cn":"韩联社中文","region":"国际","rss":"https://rsshub.app/yonhap/cn","url":"https://cn.yna.co.kr","lang":"zh","weight":6},

    # ══════ 垂直领域 ══════
    {"name":"环球科学","name_cn":"环球科学","region":"中国","rss":"https://rsshub.app/huanqiukexue","url":"https://www.huanqiukexue.com","lang":"zh","weight":6},
    {"name":"果壳","name_cn":"果壳","region":"中国","rss":"https://rsshub.app/guokr/scientific","url":"https://www.guokr.com","lang":"zh","weight":5},
    {"name":"虎扑体育","name_cn":"虎扑","region":"中国","rss":"https://rsshub.app/hupu/all","url":"https://www.hupu.com","lang":"zh","weight":5},
    {"name":"懂球帝","name_cn":"懂球帝","region":"中国","rss":"https://rsshub.app/dongqiudi/daily","url":"https://www.dongqiudi.com","lang":"zh","weight":5},
    {"name":"豆瓣电影","name_cn":"豆瓣电影","region":"中国","rss":"https://rsshub.app/douban/movie/playing","url":"https://movie.douban.com","lang":"zh","weight":4},
    {"name":"好奇心日报","name_cn":"好奇心日报","region":"中国","rss":"https://rsshub.app/qdaily/index","url":"https://www.qdaily.com","lang":"zh","weight":5},

    # ══════ 地方/区域 ══════
    {"name":"上观新闻","name_cn":"上观新闻","region":"中国","rss":"https://rsshub.app/shobserver/news","url":"https://www.shobserver.com","lang":"zh","weight":5},
    {"name":"南方都市报","name_cn":"南方都市报","region":"中国","rss":"https://rsshub.app/nandu/hot","url":"https://www.nandu.com","lang":"zh","weight":5},
    {"name":"北京日报","name_cn":"北京日报","region":"中国","rss":"https://rsshub.app/bjd/news","url":"https://www.bjd.com.cn","lang":"zh","weight":5},
    {"name":"深圳新闻网","name_cn":"深圳新闻网","region":"中国","rss":"https://rsshub.app/sznews/index","url":"https://www.sznews.com","lang":"zh","weight":4},

    # ══════ 全球英文（辅助） ══════
    {"name":"Reuters","name_cn":"路透社","region":"国际","rss":"https://rsshub.app/reuters/world","url":"https://www.reuters.com","lang":"en","weight":9},
    {"name":"AP News","name_cn":"美联社","region":"国际","rss":"https://rsshub.app/apnews/topics/apf-topnews","url":"https://apnews.com","lang":"en","weight":9},
    {"name":"Al Jazeera","name_cn":"半岛电视台","region":"国际","rss":"https://www.aljazeera.com/xml/rss/all.xml","url":"https://www.aljazeera.com","lang":"en","weight":8},
    {"name":"The Guardian","name_cn":"卫报","region":"国际","rss":"https://www.theguardian.com/world/rss","url":"https://www.theguardian.com","lang":"en","weight":8},
    {"name":"Bloomberg","name_cn":"彭博社","region":"国际","rss":"https://feeds.bloomberg.com/markets/news.rss","url":"https://www.bloomberg.com","lang":"en","weight":8},
    {"name":"Nikkei Asia","name_cn":"日经亚洲","region":"国际","rss":"https://asia.nikkei.com/rss/feed/nar","url":"https://asia.nikkei.com","lang":"en","weight":8},
]

# ── 分类定义 ──────────────────────────────────────────
CATEGORIES = {
    "Politics":    {"label":"时政","color":"#dc2626","weight":10},
    "Economy":     {"label":"财经","color":"#059669","weight":9},
    "World":       {"label":"国际","color":"#0891b2","weight":9},
    "Technology":  {"label":"科技","color":"#2563eb","weight":8},
    "Science":     {"label":"科学","color":"#7c3aed","weight":7},
    "Military":    {"label":"军事","color":"#b45309","weight":7},
    "Sports":      {"label":"体育","color":"#ea580c","weight":5},
    "Culture":     {"label":"文化","color":"#d946ef","weight":5},
}
CATEGORY_ORDER = ["Politics","Economy","World","Technology","Science","Military","Sports","Culture"]

# ── 中文关键词分类 ────────────────────────────────────
CATEGORY_KEYWORDS = {
    "Politics": [
        "国家主席","总书记","国务院","政治局","人大","政协","中纪委",
        "外交部","国防部","白宫","总统","选举","政府","国会","议会",
        "制裁","峰会","访问","会谈","声明","抗议","主权","领土",
        "两岸","台湾","香港","南海","钓鱼岛","西藏",
        "两会","改革","法治","反腐","党建",
        "president","election","government","congress","vote","sanction",
        "war","military","nato","ukraine","gaza","israel","putin","biden",
    ],
    "Economy": [
        "GDP","经济","增长","通胀","利率","央行","美联储","人民币","汇率",
        "股市","A股","沪指","深指","港股","美股","基金","期货",
        "房价","楼市","房企","GDP","就业","消费","出口","进口",
        "制造业","芯片","新能源","光伏","锂电","电动车",
        "华为","比亚迪","腾讯","阿里","字节","小米",
        "market","stock","trade","inflation","fed","tariff","tesla","nvidia",
    ],
    "World": [
        "联合国","世卫","北约","欧盟","G20","G7","金砖",
        "冲突","战争","轰炸","袭击","导弹","核","难民",
        "中东","加沙","以色列","巴勒斯坦","伊朗","乌克兰","俄罗斯",
        "朝鲜","韩国","日本","印度","东盟",
        "地震","洪水","台风","火灾","空难",
    ],
    "Technology": [
        "AI","人工智能","大模型","ChatGPT","GPT","OpenAI","DeepSeek","文心一言",
        "芯片","半导体","光刻机","5G","6G","量子","航天","火箭","卫星",
        "华为","苹果","iPhone","特斯拉","小米","比亚迪","宁德",
        "互联网","算法","数据","隐私","网络安全",
        "apple","google","microsoft","meta","amazon","nvidia","spacex",
    ],
    "Science": [
        "研究","发现","论文","科学","实验","基因","DNA","细胞","疫苗",
        "航天","空间站","火星","月球","探测器","望远镜",
        "气候","环境","生态","物种","考古","化石",
        "诺贝尔","nature","science",
    ],
    "Military": [
        "解放军","海军","空军","陆军","火箭军","航母","驱逐舰","战机",
        "演习","威慑","巡航","部署","征兵","退伍",
        "武器","导弹","雷达","无人机","坦克","潜艇",
    ],
    "Sports": [
        "奥运","世界杯","亚运","世锦赛","中超","CBA","NBA","欧冠","英超",
        "足球","篮球","排球","网球","乒乓","羽毛","游泳","田径",
        "国足","中国女排","谷爱凌","苏炳添","梅西","C罗",
    ],
    "Culture": [
        "电影","票房","导演","戛纳","威尼斯","奥斯卡",
        "音乐","演唱会","专辑","展览","博物馆","文物",
        "春晚","综艺","明星","艺人","网红",
        "文学","小说","诗歌","出版","教育","高考","大学",
    ],
}

# ── 重要性阈值 ────────────────────────────────────────
IMPORTANCE_MIN_KEYWORD_SCORE = 2  # 至少命中2个关键词才算重要新闻
