import peewee as pw
import peeweedbevolve
import settings

def base_model(dbname):
	"""创建peewee Mysql Model基类"""
	db = pw.MySQLDatabase(dbname, charset='utf8', **settings.DB)
	# db.execute_sql("SET NAMES utf8 COLLATE utf8_unicode_ci;")

	class BaseModel(MyBaseModel):
		class Meta:
			database = db

	return BaseModel

class MyBaseModel(pw.Model):

	@classmethod
	def iterdocs(cls):
		for key, field in cls._meta.fields.items():
			yield key, field.verbose_name

	def __iter__(self):
		for key in self._meta.fields.keys():
			yield key, getattr(self, key)

	def iter_label_value(self):
		for key, field in self._meta.fields.items():
			yield field.verbose_name, getattr(self, key)

	def setdata(self, data):
		self._data.update(data)