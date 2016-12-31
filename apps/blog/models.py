from lib.sql import base_model, pw

BaseModel = base_model('blog')

class User(BaseModel):
	id       = pw.PrimaryKeyField()
	username = pw.CharField(16, verbose_name="用户名")
	password = pw.FixedCharField(40)
	email    = pw.CharField(32, verbose_name="邮箱")
	nickname = pw.CharField(16, verbose_name="昵称", null=True)
	phone    = pw.FixedCharField(11, verbose_name="电话", null=True)
	gender   = pw.FixedCharField(1, verbose_name="性别", null=True)
	article_count = pw.IntegerField(default=0)
	follow_count  = pw.IntegerField(default=0)
	fans_count    = pw.IntegerField(default=0)

	def getname(self):
		return self.nickname or self.username


class Article(BaseModel):

	# status
	DRAFT     = 0
	PUBLISHED = 1

	id            = pw.PrimaryKeyField()
	author        = pw.ForeignKeyField(User, related_name='articles')
	title         = pw.CharField(32, verbose_name="标题")
	tags          = pw.CharField(64, verbose_name="标签")
	content       = pw.CharField(255, verbose_name="内容")
	create_time   = pw.DateTimeField(verbose_name="创建时间")
	update_time   = pw.DateTimeField(verbose_name="更新时间")
	status        = pw.SmallIntegerField(verbose_name="状态", default=DRAFT)
	comment_count = pw.IntegerField(default=0)


class ArticleTag(BaseModel):
	id   = pw.PrimaryKeyField()
	name = pw.CharField(16, verbose_name="名称")


class ArticleComment(BaseModel):
	article = pw.ForeignKeyField(Article)
	user    = pw.ForeignKeyField(User)
	time    = pw.DateTimeField(verbose_name="创建时间")
	body    = pw.DateTimeField(verbose_name="评论内容")


# class Admin(BaseModel):
# 	user_id = pw.ForeignKeyField(User, primary_key=True)


class Follow(BaseModel):
	follower = pw.ForeignKeyField(User, primary_key=True, related_name='followers')
	target   = pw.ForeignKeyField(User)