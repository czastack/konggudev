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

	def getname(self):
		return self.nickname or self.username

class Article(BaseModel):
	id          = pw.PrimaryKeyField()
	author      = pw.ForeignKeyField(User, related_name='articles')
	create_time = pw.DateTimeField(verbose_name="创建时间")
	update_time = pw.DateTimeField(verbose_name="更新时间")
	tags        = pw.CharField(200, verbose_name="标签")
	description = pw.CharField(200, verbose_name="摘要")
	keywords    = pw.CharField(50, verbose_name="关键词")


class ArticleTag(BaseModel):
	id   = pw.PrimaryKeyField()
	name = pw.CharField(16, verbose_name="名称")


class Admin:
	user_id = pw.ForeignKeyField(User, primary_key=True)


class Attention:
	fromid = pw.ForeignKeyField(User, primary_key=True)
	toid   = pw.ForeignKeyField(User)