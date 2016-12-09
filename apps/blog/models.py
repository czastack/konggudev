from lib.sql import *

class User(BaseModel):
	id      = Column(Integer,      primary_key=True)
	name    = Column(String(16),   doc="姓名")
	gender  = Column(db.CHAR(1),   doc="性别")
	phone   = Column(String(11),   doc="电话")
	email   = Column(String(16),   doc="邮箱")

class Article(BaseModel):
	id          = Column(Integer, primary_key=True)
	author_id   = Column(String(8), ForeignKey('user.id'))
	author      = db.relationship('User', backref=db.backref('articles', lazy='dynamic'))
	create_time = Column(db.DateTime(), doc="创建时间")
	update_time = Column(db.DateTime(), doc="更新时间")
	tags        = Column(String(200),   doc="标签")
	description = Column(String(200),   doc="摘要")
	keywords    = Column(String(50),    doc="关键词")

class ArticleTag(BaseModel):
	id   = Column(Integer, primary_key=True)
	name = Column(String(16),   doc="名称")

class Admin:
	user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)