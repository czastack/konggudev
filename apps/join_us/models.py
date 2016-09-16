from lib.sql import *

class Department(BaseModel):
	id      = Column(String(8),    primary_key=True)
	no      = Column(db.SmallInteger, doc="序号", unique=True)
	name    = Column(String(8),    doc="部门名称", unique=True)
	parent  = Column(String(8),    ForeignKey('department.id'), doc="上级部门")
	intro   = Column(String(255),  doc="部门介绍")
	direct  = Column(String(32),   doc="招收方向")
	predict = Column(Integer,      doc="预计招收")

	@classmethod
	def getname(cls, id):
		return cls.find(id=id).with_entities(cls.name)[0][0]

	@classmethod
	def on_cache_data(cls):
		cls.cache_data(lambda c,q:q.order_by(c.no))

Department.on_cache_data()

class User(BaseModel):
	id      = Column(Integer,      primary_key=True)
	name    = Column(String(16),   doc="姓名")
	sex     = Column(db.CHAR(1),   doc="性别")
	college = Column(String(4),    doc="学院")
	major   = Column(String(16),   doc="专业")
	phone   = Column(String(11),   doc="电话", unique=True)
	qq      = Column(String(16),   doc="QQ",   unique=True)
	depart  = Column(String(8),    ForeignKey('department.id'), doc="部门")

class Applicant(BaseModel):
	id      = Column(Integer,      primary_key=True)
	status  = Column(db.SmallInteger, doc="状态", server_default="0")
	name    = User.copy_column('name')
	sex     = User.copy_column('sex')
	age     = Column(Integer,      doc="年龄")
	college = User.copy_column('college')
	major   = User.copy_column('major')
	home    = Column(String(16),   doc="籍贯")
	phone   = User.copy_column('phone')
	qq      = User.copy_column('qq')
	hobby   = Column(String(64),   doc="特长兴趣爱好")
	reason  = Column(String(64),   doc="加入原因")
	first   = Column(String(8),    ForeignKey('department.id'), doc="首选部门")
	second  = Column(String(8),    ForeignKey('department.id'), doc="备选部门")

	def to_read(self, detail = False):
		"""使更易阅读"""
		college = self.college_obj
		self.college = detail and college.name or college.abbr
		self.first = Department.getname(self.first)
		self.second = Department.getname(self.second)

	@property
	def college_obj(self):
		return College.query.get(self.college)

	@property
	def college_abbr(self):
		return self.college_obj.abbr

class College(BaseModel):
	id      = Column(String(8),    primary_key=True)
	name    = Column(String(16),   doc="学院名称", unique=True)
	abbr    = Column(String(16),   doc="缩写", unique=True)

class Major(BaseModel):
	id      = Column(Integer,      primary_key=True)
	name    = Column(String(32),   doc="专业名称", unique=True)
	college_id = Column(String(8), ForeignKey('college.id'))
	college = db.relationship('College', backref=db.backref('majors', lazy='dynamic'))