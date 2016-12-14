import peewee as pw
import peeweedbevolve
import settings

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

class MyBaseModel(pw.Model):

	@classmethod
	def iterdocs(cls):
		for key in cls._meta.sorted_field_names:
			yield key, cls._meta.fields[key].verbose_name

	def __iter__(self):
		for key in self._meta.sorted_field_names:
			yield key, getattr(self, key)

	def iter_label_value(self):
		for key in self._meta.sorted_field_names:
			yield self._meta.fields[key].verbose_name, getattr(self, key)

	def setdata(self, data):
		self._data.update(data)