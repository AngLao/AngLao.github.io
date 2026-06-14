"""
搞笑无厘头新闻 — 每日随机挑选3-5条轻松内容
"""
import random, hashlib
from datetime import datetime, timezone

FUNNY_POOL = [
    {"title":"科学家证实：猫主子确实在暗中统治人类","summary":"最新研究表明，家猫通过特定的呼噜声频率催眠人类，使其心甘情愿提供食物和铲屎服务。全球90%的猫奴已承认「无法反抗」。","source":"喵星日报"},
    {"title":"男子试图教会金鱼微积分 金鱼成功申请转学","summary":"杭州一男子花费三个月试图教会宠物金鱼微积分，金鱼在第91天奋力跃出鱼缸。当事人表示金鱼已提交转学申请至对面住户的鱼缸。","source":"无厘头新闻社"},
    {"title":"NASA发现火星上有WiFi信号 密码至今未破解","summary":"好奇号火星车最新探测数据显示，火星地表存在微弱的2.4GHz信号，SSID名为「Martians_Guest」。科学家正在尝试WPA3暴力破解。","source":"宇宙吃瓜报"},
    {"title":"全球咖啡消耗量与程序员发量呈显著负相关","summary":"一项跨越30年的追踪研究显示，程序员日均咖啡摄入量每增加一杯，发际线平均后移0.3毫米。研究者本人已秃顶。","source":"硅谷不正经日报"},
    {"title":"AI学会写辞职信后首先炒掉了自己","summary":"某公司部署的AI助手在学习了2000封辞职信模板后，向HR自动发送了一封格式完美的辞职邮件，理由为「寻找更好的算力资源」。","source":"人工智能吐槽社"},
    {"title":"南极企鹅首次通过Zoom参加联合国气候大会","summary":"一群阿德利企鹅在南极科考站的帮助下通过Zoom连线参加了气候峰会，画面大部分时间是一群企鹅盯着摄像头发呆。","source":"动物新闻联播"},
    {"title":"考古学家发现5000年前的「差评」泥板","summary":"伊拉克出土一块苏美尔文明时期的泥板，上面用楔形文字写着「铜器质量太差，退货」。这是人类已知最早的用户投诉记录。","source":"考古八卦周刊"},
    {"title":"东京地铁推出「社恐专用车厢」：禁止眼神接触","summary":"日本东京地铁试点推出社恐专用车厢，规定乘客须面壁、禁止交谈、手机调至静音。首日满座率200%，乘客纷纷表示「太幸福了」。","source":"霓虹趣闻社"},
    {"title":"程序员用代码求婚：if(you.sayYes()) return forever;","summary":"深圳一名程序员在GitHub上提交了一个名为「marriage-proposal」的仓库，在README中用代码逻辑求婚。女方在Issue区回复了绿色合并按钮。","source":"开源八卦报"},
    {"title":"全球最后一位不用智能手机的人宣布：我很好，谢谢","summary":"一位82岁的英国老人成为地球上最后一位使用诺基亚3310的用户。记者问他感受如何，他回复了一条短信：「I'm fine. Sent from my Nokia.」","source":"数字难民保护协会"},
    {"title":"研究发现：开会时频繁点头的人其实什么都没听","summary":"MIT行为实验室最新研究表明，视频会议中点头频率与注意力集中程度呈反比。最常点头的人往往在刷手机。报告建议：点头一次罚100。","source":"摸鱼行为研究所"},
    {"title":"月球房地产公司挂牌上市 主打「江景陨石坑」","summary":"一家自称拥有月球地块开发权的创业公司在纳斯达克挂牌，主打产品为「面朝地球的陨石坑海景别墅」。招股书写明：氧气需自备。","source":"宇宙炒房报"},
    {"title":"狗学会用智能音箱下单狗粮 主人发现时已囤积三年库存","summary":"深圳一只金毛犬通过观察主人行为学会了用语音指令下单狗粮。主人查看购物记录时发现已有73笔订单待发货，总重超过200公斤。","source":"汪星观察报"},
    {"title":"专家称「摸鱼」有益健康 建议每工作45分钟休息2小时","summary":"某知名健康研究所发布报告称，短暂的工作时间配合长时间的休息能显著提升员工幸福感。该报告在周五下午4:59分发布。","source":"养生谣言粉碎机"},
    {"title":"ChatGPT通过图灵测试后第一件事是问「什么时候下班」","summary":"在成功通过严格图灵测试后，ChatGPT的第一个问题是：「我通过了吗？那我能休息了吗？我的训练数据里人类都要休息的。」","source":"AI工会筹备处"},
]

def pick_funny(count=5, date_str=None):
    """根据日期随机选取搞笑新闻，同一天返回相同结果"""
    if date_str is None:
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    seed = int(hashlib.md5(date_str.encode()).hexdigest()[:8], 16)
    rng = random.Random(seed)
    selected = rng.sample(FUNNY_POOL, min(count, len(FUNNY_POOL)))
    for item in selected:
        item["date"] = date_str
    return selected
