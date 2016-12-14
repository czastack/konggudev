from lib.sql import base_model, pw

BaseModel = base_model('joinus')

class Department(BaseModel):
	id      = pw.CharField(8,    primary_key=True)
	no      = pw.SmallIntegerField(verbose_name="序号", unique=True)
	name    = pw.CharField(8,    verbose_name="部门名称", unique=True)
	parent  = pw.ForeignKeyField('self', verbose_name="上级部门")
	intro   = pw.CharField(255,  verbose_name="部门介绍")
	direct  = pw.CharField(32,   verbose_name="招收方向")
	predict = pw.IntegerField(verbose_name="预计招收")

	@classmethod
	def getname(cls, id):
		return cls.select(cls.name).get(id=id).name

	@classmethod
	def on_cache_data(cls):
		cls.cache_data(lambda c,q:q.order_by(c.no))

# Department.on_cache_data()

class User(BaseModel):
	id      = pw.PrimaryKeyField
	name    = pw.CharField(16,   verbose_name="姓名")
	sex     = pw.FixedCharField(1,  verbose_name="性别")
	college = pw.CharField(4,    verbose_name="学院")
	major   = pw.CharField(16,   verbose_name="专业")
	phone   = pw.CharField(11,   verbose_name="电话")
	qq      = pw.CharField(16,   verbose_name="QQ")
	depart  = pw.ForeignKeyField(Department, verbose_name="部门")

class Applicant(BaseModel):
	id      = pw.PrimaryKeyField
	status  = pw.SmallIntegerField(verbose_name="状态", default="0")
	name    = User.name
	sex     = User.sex
	age     = pw.IntegerField(verbose_name="年龄")
	college = User.college
	major   = User.major
	home    = pw.CharField(16,   verbose_name="籍贯")
	phone   = User.phone
	qq      = User.qq
	hobby   = pw.CharField(64,   verbose_name="特长兴趣爱好")
	reason  = pw.CharField(255,  verbose_name="加入原因")
	first   = pw.ForeignKeyField(Department, related_name='applicants', verbose_name="首选部门")
	second  = pw.ForeignKeyField(Department, verbose_name="备选部门")

	def to_read(self, detail = False):
		"""使更易阅读"""
		college = self.college_obj
		self.college = detail and college.name or college.abbr
		self.first = Department.getname(self.first)
		if self.second:
			self.second = Department.getname(self.second)

	@property
	def college_obj(self):
		return College.get(id=self.college)

	@property
	def college_abbr(self):
		return self.college_obj.abbr

class College(BaseModel):
	id      = pw.CharField(8,    primary_key=True)
	name    = pw.CharField(16,   verbose_name="学院名称", unique=True)
	abbr    = pw.CharField(16,   verbose_name="缩写", unique=True)

class Major(BaseModel):
	id      = pw.PrimaryKeyField
	name    = pw.CharField(32,   verbose_name="专业名称", unique=True)
	college = pw.ForeignKeyField(College, related_name='majors')