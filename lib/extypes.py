def astr(text):
	"""确保是字符串类型"""
	return text if isinstance(text, str) else str(text)

def is_list_or_tuple(var):
	"""是否是列表或元组"""
	return isinstance(var, list) or isinstance(var, tuple)

def list_re(li, fn):
	"""列表元素映射"""
	for i in range(len(li)):
		li[i] = fn(li[i])

def list_find(li, fn):
	"""列表查找第一个匹配的元素"""
	for x in li:
		if fn(x):
			return x;

def getif(data, name):
	return data.get(name, None)

def popif(data, key):
	return data.pop(key, None)

def puts(dst, src, keys = None):
	"""
	更新dict全部或指定字段
	dst: 模板dict, src: 来源dict
	"""
	for key in keys or src:
		dst[key] = src[key]

# 依次测试keys中的key，返回第一个存在的或者None
# def gets_or(data, keys):
# 	for key in keys:
# 		if key in data:
# 			return data[key]
# 	return None

# def method_proxy(member, key):
# 	"""方法代理"""
# 	def fn(self, *args, **kwargs):
# 		return getattr(getattr(self, member), key)(*args, **kwargs)
# 	return fn

# def add_method_proxy(cls, member, keys):
# 	"""给类添加方法代理"""
# 	for key in keys:
# 		setattr(cls, key, method_proxy(member, key))

class Map(dict):
	__slots__ = ()

	def __getattr__(self, name):
		return self.get(name, None)

	def __setattr__(self, name, value):
		self[name] = value

	def __delattr__(self, name):
		del self[name]

	__puts__ = puts

class Dict:
	"""
	data = Dict({'a': 1})
	print(data.a) # get 1
	"""
	__slots__ = ('_data',)

	def __init__(self, obj = None):
		self._attr('_data', obj)

	def _attr(self, name, value):
		object.__setattr__(self, name, value)

	def __getattr__(self, name):
		return self._data.get(name, getattr(self._data, name, None))

	def __setattr__(self, name, value):
		self._data[name] = value

	def __str__(self):
		return self._data.__str__()

	def __iter__(self):
		return self._data.__iter__()

	def __getitem__(self, key):
		if is_list_or_tuple(key):
			return key.__class__(self._data[k] for k in key)
		return self._data[key]

	def __setitem__(self, key, value):
		if is_list_or_tuple(key):
			if is_list_or_tuple(value):
				val = iter(value).__next__
			else:
				val = lambda: value
			for k in key:
				self._data[k] = val()
		else:
			self._data[key] = value

	def __delattr__(self, name):
		del self._data[name]

	def __repr__(self):
		return __class__.__name__ + '(' + self.__str__() + ')'

	def __and__(self, keys):
		if is_list_or_tuple(keys):
			return __class__({key: self.__getattr__(key) for key in keys})

	getif = getif
	popif = popif
	puts = puts

# add_method_proxy(Dict, '__dict__', ['__str__', '__iter__', '__getitem__', '__setitem__'])

class Dicts:
	"""
	接收字典列表
	datas = Dict([{'a': 1}, {'a': 2}])
	for data in datas:
	    print(data.a)
	"""
	__slots__ = ('__ref', 'data')

	def __init__(self, array):
		if is_list_or_tuple(array):
			self.__ref = None
			self.data = array
		else:
			raise TypeError('array must be a list or tuple')

	def __iter__(self):
		if not self.__ref:
			self.__ref = Dict()
		
		for item in self.data:
			self.__ref.__init__(item)
			yield self.__ref