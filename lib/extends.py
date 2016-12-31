import os

# extend peewee
import peewee as pw

def create_database(self, dbname):
	self.execute_sql("CREATE DATABASE %s CHARACTER SET utf8 COLLATE utf8_general_ci;" % dbname)

pw.MySQLDatabase.create_database = create_database


# extend template_ref
from jinja2.runtime import TemplateReference

def tpldir(self):
	tpldir = getattr(self, '_tpldir', None)
	if not tpldir:
		self._tpldir = tpldir = os.path.dirname(self._TemplateReference__context.name) + '/'
	return tpldir

def brother(self, name):
	return self.tpldir + name + '.html'

TemplateReference.tpldir = property(tpldir)
TemplateReference.brother = brother