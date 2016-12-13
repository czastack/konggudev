from lib.sql import base_model, pw

BaseModel = base_model('blog')

class User(BaseModel):
	id      = pw.IntegerField(primary_key=True)
	name    = pw.CharField(16, verbose_name="用户名")
	nickname = pw.CharField(16, verbose_name="昵称")
	gender  = pw.FixedCharField(1, verbose_name="性别")
	phone   = pw.CharField(11, verbose_name="电话")
	email   = pw.CharField(16, verbose_name="邮箱")

class Article(BaseModel):
	id          = pw.IntegerField(primary_key=True)
	author      = pw.ForeignKeyField(User, related_name='articles')
	create_time = pw.DateTimeField(verbose_name="创建时间")
	update_time = pw.DateTimeField(verbose_name="更新时间")
	tags        = pw.CharField(200, verbose_name="标签")
	description = pw.CharField(200, verbose_name="摘要")
	keywords    = pw.CharField(50, verbose_name="关键词")


class ArticleTag(BaseModel):
	id   = pw.IntegerField(primary_key=True)
	name = pw.CharField(16, verbose_name="名称")


class Admin:
	user_id = pw.ForeignKeyField(User, primary_key=True)