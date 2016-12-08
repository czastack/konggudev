from main import db

def index_handle(handler):
	from .forms import ApplyForm
	if handler.is_get:
		return handler.render('/form', form=ApplyForm())
	else:
		form = ApplyForm(handler.request.form)
		return form.data

def add_data_handle(handler):
	from . import models

	# Department = models.Department
	# datas = [
	# 	Department(no=1, id="admin", name="行政中心", predict=50, intro="空谷行政中心是一个集文秘、宣传、人事、财务四大功能的空谷校园网的枢纽组织。想要进一步提高自己细致认真负责的能力吗？想要亲手组织策划一场属于自己青春的活动吗？想要提高Office办公软件应用效率吗？想认识更多志同道合的朋友们并共同享受奋斗的时光吗？这里有上档次的活动等你来举办，这里有MOS大师可以亲手传授经验，这里有热情活泼可爱的学长学姐们在等着你。心动不如行动，那就快来加入我们吧，空谷行政中心尽其所能给你想要的答案。"),
	# 	Department(no=2, id="relation", name="外联中心", predict=30, intro="大学生活is coming!小鲜肉们，跟着我们去各种高大上的高校交流吧！跟着我们去各种土豪商家谈赞助吧！跟着我们去各种优秀的学生团体拉近感情吧！如果你伶牙俐齿，如果你有足够自信，如果你想改变自己，加入我们有爱又友爱的外联family吧，谱写属于你自己的乐章，奏出最美的旋律。好胆你就来，外联在这里！"),
	# 	Department(no=3, id="news", name="新闻中心", intro="能拍能写能编，我们是多面小能手；写稿修图剪片子，那些年我们熬过的夜。妙笔书写客观，镜头记录真实，时评纵论校内外事；敏感犀利，动态，专访皆入笔端。笔是我们思想的双脚，相机是我们看待社会的另一个方式。关注西大学子所关心之事，用新闻纪录西大历史。"),
	# 	Department(no=4, id="wenyu", name="文娱中心", predict=120, intro="你还在苦苦寻找你的同好者吗？快来加入空谷文娱中心吧！文娱中心是空谷校园网的一个以内容为主的部门，旗下设有文学、生活、娱乐、动漫四大子网。这里是同好者的聚集地，是创作者的天堂。如果你喜欢小说诗歌、时尚旅游、八卦影视、二次元，那么一定不要错过我们文娱中心！"),
	# 	Department(no=5, id="newmedia", name="新媒体中心", intro="我们用爪机发布校园热点微博，我们头脑风暴做出一篇篇精彩的微信。在新媒体，我们需要的不单是技术，而是每一个热爱发现的你。来不及解释了快上车！让新媒体的老司机带你飞遍西大！只要你会码字，敢吐槽，有热情。上到国家大事，下至校园热点，新媒体给你一个发出自己心声的平台。"),
	# 	Department(no=6, id="knet", name="K-NET中心", predict=24, intro="天马行空的想像，与众不同的设计，从另一个角度看生活，大开脑洞，我们需要这样的你。在这里，你可以成为一名文编，吐槽点评叙事抒情，写你所想。或者做一名图编，穿街走巷修图ps，拍你所见。变成一名美编，用HTMLS、Photoshop、epub360设计一个世界。加入我们，这是一个想像至上的时代，这是我们的时代。"),
	# 	Department(no=7, id="design", name="设计中心", intro="你是否经常灵光乍现却苦于没有设计的软件基础，不能做出想象中的设计作品而只能锤头叹息？你是否经常流连于大神做宣传展板、banner、网页、海报、宣传单却无力效仿？只要你有天马行空的想象力，只要你喜欢欣赏美，发现美，创造美，欢迎加入我们！我们愿意带你攀登英雄塔，铸造王者剑，穿越星际天空，一起打造专属我们的视觉盛宴。"),
	# 	Department(no=8, id="web", name="网络中心", predict=35, intro="想要了解网页的秘密？想把HTML/CSS/JS统统斩于马下？想成为Web前端开发的大神？想跟随WEBAPP吞噬互联网的步伐？想站上Web2.0的浪潮之巅？快来加入我们吧，与男神女神一起解密代码！我们要的是兴趣与坚持，让空谷网络带你飞。"),
	# 	Department(no=9, id="dev", name="研发中心", predict=30, intro="传说在空谷有这样一群神秘的人，他们默默守护着空谷的网站，让Bug无所遁形；他们用技术和智慧，开发新产品。现在他们开始招新啦！希望了解程序员星人的神秘世界吗？想成为技术大神却不懂如何入门？加入空谷研发，网站建设、程序开发，不再那么神秘。从现在开始，用指尖和代码改变世界！"),
	# 	Department(no=10, id="wenxue", parent="ent", name="文学网", intro="书青春妙笔生花，千里赴文学盛宴！这里汇聚着怀揣文学梦想的少年少女；这里闪耀着灵感的碰撞迸发出的灿烂火花。无论你是满怀心事的少女，还是满腔热枕的少侠，我们陪你诉闺中密事，我们与你一同仗剑天涯！文以传情，学以致意。"),
	# 	Department(no=11, id="ent", parent="ent", name="娱乐网", intro="你是否在遗憾喜欢的音乐不能分享给别人？你是否在担心喜欢的电视剧找不到知己一起讨论？你是否还在苦恼找不到好看的电影？那么加入我们娱乐网吧！只要你喜欢音乐或电影或综艺，在这里，你可以畅所欲言，你将收获许多知己。"),
	# 	Department(no=12, id="life", parent="ent", name="生活网", intro="舌尖上享受美食的你，爱分享化妆技巧的你，善于传播身边趣闻的你，乐于秀出精彩人生的你，享受生活的达人们，你们还等什么呢？赶快加入我们吧，心动不如行动，生活网是你最好的选择。hurry up ! ! !"),
	# 	Department(no=13, id="animate", parent="ent", name="动漫网", intro="你可识得此动漫网？想要投喂和被投喂吗，想要脱非入欧吗，想要撩妹搅基吗，想要围观基♂情吗？我们有能污能清新的文手角虫与一干缺粮求投喂的宝宝，我们有欧气冲天的欧皇带你单抽带你飞，我们有可爱的妹砸与呆萌的骚年，我们有【哔——】还在犹豫什么！快来加入我们！"),
	# ]

	# College = models.College
	# datas = [
	# 	College(id="sx", name="数学与信息科学学院", abbr="数信"),
	# 	College(id="wl", name="物理科学与工程技术学院", abbr="物理"),
	# 	College(id="jx", name="机械工程学院", abbr="机械"),
	# 	College(id="dq", name="电气工程学院", abbr="电气"),
	# 	College(id="tm", name="土木建筑工程学院", abbr="土木"),
	# 	College(id="hx", name="化学化工学院", abbr="化学"),
	# 	College(id="hj", name="环境学院", abbr="环境"),
	# 	College(id="hy", name="海洋学院", abbr="海洋"),
	# 	College(id="jsj", name="计算机与电子信息学院", abbr="计电"),
	# 	College(id="zy", name="资源与冶金学院", abbr="资冶"),
	# 	College(id="cl", name="材料科学与工程学院", abbr="材料"),
	# 	College(id="sm", name="生命科学与技术学院", abbr="生科"),
	# 	College(id="nx", name="农学院", abbr="农学院"),
	# 	College(id="dw", name="动物科学技术学院", abbr="动科"),
	# 	College(id="lx", name="林学院", abbr="林学院"),
	# 	College(id="wx", name="文学院", abbr="文学院"),
	# 	College(id="xw", name="新闻传播学院", abbr="新闻"),
	# 	College(id="wgy", name="外国语学院", abbr="外语"),
	# 	College(id="zj", name="中加国际学院", abbr="中加"),
	# 	College(id="sxy", name="商学院", abbr="商学院"),
	# 	College(id="gg", name="公共管理学院", abbr="公管"),
	# 	College(id="fx", name="法学院", abbr="法学院"),
	# 	College(id="jy", name="教育学院", abbr="教育"),
	# 	College(id="ys", name="艺术学院", abbr="艺术"),
	# 	College(id="ty", name="体育学院", abbr="体育"),
	# ]

	db.session.add_all(datas)
	db.session.commit()
	return "成功添加%d条数据" % len(datas)
