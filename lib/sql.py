import peewee as pw
import peeweedbevolve
import settings
import time

def base_model(dbname=''):
	"""创建peewee Mysql Model基类"""
	db = pw.MySQLDatabase(dbname, charset='utf8', **settings.DB)

	class BaseModel(MyBaseModel):
		class Meta:
			database = db

	return BaseModel


def _extend_peewee():
	def create_database(self, dbname):
		self.execute_sql("CREATE DATABASE %s CHARACTER SET utf8 COLLATE utf8_general_ci;" % dbname)
	pw.MySQLDatabase.create_database = create_database

_extend_peewee()
del _extend_peewee

def cache(cache_time):
	"""
	缓存查询结果装饰器
	传入 delete=True删除缓存
	"""
	def _deco(fn):
		def __deco(self, *args, **kwargs):
			time_key = "_cache_%s_endtime" % fn.__name__
			data_key = "_cache_" + fn.__name__
			if (kwargs.get('delete', False)):
				setattr(self, time_key, 0)
				setattr(self, data_key, None)
				return
			if time.time() < getattr(self, time_key, 0):
				return getattr(self, data_key)
			else:
				data = fn(self, *args, **kwargs)
				setattr(self, data_key, data)
				setattr(self, time_key, time.time() + cache_time)
				return data
		return __deco
	return _deco

class MyBaseModel(pw.Model):

	@classmethod
	def db(cls):
		return cls._meta.database

	@classmethod
	def find(cls):
		return cls.select(pw.SQL('*'))

	@classmethod
	def get_label(cls, key):
		return cls._meta.fields[key].verbose_name

	@classmethod
	def iterdocs(cls):
		for key in cls._meta.sorted_field_names:
			yield key, cls.get_label(key)

	def __iter__(self):
		for key in self._meta.sorted_field_names:
			yield key, getattr(self, key)

	def iter_label_value(self):
		for key in self._meta.sorted_field_names:
			yield self.get_label(key), getattr(self, key)

	def setdata(self, data):
		self._data.update(data)

	def __delete__(self, key):
		del self._data[key]