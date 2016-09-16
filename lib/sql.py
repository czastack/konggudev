from main import db

Column       = db.Column
String       = db.String
Integer      = db.Integer
ForeignKey   = db.ForeignKey

class BaseModel(db.Model):
	__abstract__ = True

	@classmethod
	def find_one(cls, **kwargs):
		return cls.find(**kwargs).first()

	@classmethod
	def find(cls, **kwargs):
		return cls.query.filter_by(**kwargs)

	@classmethod
	def cache_data(cls, fn = None):
		cls.cache = (fn(cls, cls.query) if fn else cls.query).all()

	@classmethod
	def copy_column(cls, name):
		return cls.__table__.c[name].copy()

	@classmethod
	def iterdocs(cls):
		for key, column in cls.__table__.c.items():
			yield key, column.doc
	
	@staticmethod
	def dbcommit():
		"""提交数据库改动"""
		db.session.commit()

	def __init__(self, data = None):
		db.Model.__init__(self)
		if data:
			self.setdata(data)

	def __repr__(self):
		return '<%s:%s>' % (self.__class__.__name__, self.name)

	def __iter__(self):
		for key in self.__table__.c.keys():
			yield key, getattr(self, key)

	def iter_label_value(self):
		for key, column in self.__table__.c.items():
			yield column.doc, getattr(self, key)

	def setdata(self, data):
		for key in data:
			setattr(self, key, data[key])

	def add_self(self):
		"""添加自身到数据库修改队列(insert)"""
		db.session.add(self)
		return self

	def update_self(self):
		"""添加自身到数据库修改队列(insert)"""
		db.session.merge(self)
		return self