import os
import json
from lib.extypes import Dict

def load(handler, name):
	"""加载首选项"""
	import apps
	Path = os.path
	filedir = Path.join(Path.dirname(apps.__file__), handler.appid, 'preference')
	filepath = Path.join(filedir, name + '.json')
	if not Path.isdir(filedir):
		os.mkdir(filedir)
	return Preference(filepath)

class Preference(Dict):
	"""首选项"""

	__slots__ = ('_file')
	
	def __init__(self, file):
		"""
		:param name: preference目录下的文件主名
		"""
		if os.path.isfile(file):
			with open(file, 'r') as fp:
				data = json.load(fp)
		else:
			data = {}
		Dict.__init__(self, data)
		self._attr('_file', file)

	def save(self):
		with open(self._file, 'w') as fp:
			json.dump(self._data, fp)
