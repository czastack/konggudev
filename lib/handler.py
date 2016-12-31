from flask import render_template as render, redirect, jsonify
from main import app
from lib import extypes
import settings, types


ROUTE_MODULE = 1
ROUTE_FUNC   = 2
ROUTE_METHOD = 4


# 生成处理器名称
fn_hname = lambda name: name + settings.handle_fn_suffix
cls_hname = lambda name: name.title().replace('-', '') + settings.handle_class_suffix


# 尝试获取处理器
# def get_module_handler(module, name, default):
# 	v = lambda n, f: getattr(module, f(n), None)
# 	return v(name, fn_handler) or v(name, cls_handler) or v(default, fn_handler) or v(default, cls_handler)

# 预处理路由
def prepare_route(route):
	last = route[-1]
	if last.endswith(settings.FILE_EXT):
		last = last[:-len(settings.FILE_EXT)]
	route[-1] = last

def dispatch(url):
	# 1: app, 2: module, 3: function or class, 4: method
	route = url.split('/', 4)
	prepare_route(route)
	IDX = 'index'
	index = lambda: route.append(IDX) or IDX
	len(route) == 1 and index()
	for i in range(len(route)):
		if not route[i]:
			route[i] = IDX
	# 调用对应的类或函数
	try:
		route_type = 0
		module = __import__('apps.' + route[0], fromlist=[route[1]])
		submodule = getattr(module, route[1], None)
		if isinstance(submodule, types.ModuleType):
			route_type |= ROUTE_MODULE
			module = submodule
		# 如果路由只有2层，则调用该模块下的index函数处理
		# 3层：调用模块下route[1]同名函数处理，
		# 若未找到，调用模块下default_handler函数处理
		# 4层：调用模块下的类/方法
		lv_module = 1 + (route_type & ROUTE_MODULE) # 模块最低层级
		lv_class  = 1 + lv_module # 类最低层级

		name = index() if len(route) == lv_module else route[lv_module]
		v = lambda n: getattr(module, n, None)
		callee = v(fn_hname(name)) or v(cls_hname(name)) or v(
			settings.handle_fn_default) or v(settings.handle_class_default)
		
		if isinstance(callee, types.FunctionType):
			route_type |= ROUTE_FUNC
			result = callee(BaseHandler(route, route_type))
		elif isinstance(callee, type):
			if callee.__name__ == settings.handle_class_default:
				lv_class -= 1
			action = index() if len(route) <= lv_class else route[lv_class] # 方法名
			method = getattr(callee, action, None) or getattr(callee, 'default', None)
			if method:
				route_type |= ROUTE_METHOD
				ins = callee(route, route_type)
				# 调用类的before方法
				# before = getattr(ins, 'before', None)
				result = ins.oninit() or method(ins)
			else:
				result = '%s不存在%s方法' % (callee.__name__, action)
		else:
			result = '404'
	except Exception as e:
		import traceback
		result = traceback.format_exc()
	if not (isinstance(result, str) or isinstance(result, tuple) or result.__class__.__name__ == 'Response'):
		result = str(result)
	return result

# 找不到控制器时尝试直接渲染路由对应的模板文件
# 要在子模块中import才有效果
# 使用: from . import direct_render as default_handler
def direct_render(handler):
	return handler.render()

class BaseHandler:
	"""
	_template_dir: 见 template_name 的代码
	"""

	__slots__ = ('route', 'route_type')
	from flask import request, session
	json = staticmethod(jsonify)
	redirect = staticmethod(redirect)

	STAY = '', 204
	REFRESH = '', 200, {"Refresh": "0"}

	def __init__(self, route, route_type):
		self.route = tuple(route)
		self.route_type = route_type
		self.oninit()

	# 在url调用其他方法前执行，如果有返回值则直接返回，不调用其他方法
	# 可用于在整个类的验证登录
	def oninit(self):
		pass

	def url(self, url, start_with_sep = False):
		"""
		@会替换成模块名（同一个父级）
		:param start_with_sep: 是否要以/开头
		"""
		if not url.startswith('/'):
			url = self.appid + '/' + url
			if start_with_sep:
				url = '/' + url
		elif not start_with_sep:
			url = url[1:]
		if '@' in url:
			url = url.replace('@', (self.route[1] + '/') if len(self.route) > 2 else '')
		return url

	def render(self, tpl = None, **data):
		tpl = (tpl or self.template_name()) + '.html'
		tpl = self.url(tpl)
		return render(tpl, handler=self, settings=settings, **data)

	def template_name(self):
		if hasattr(self, '_template_dir'):
			return self.template_on_dir(self._template_dir)
		elif self.route_type & ROUTE_MODULE:
			return self.route[1] + '/' + '-'.join(self.route[2:])
		else:
			return '-'.join(self.route[1:])

	def template_on_dir(self, dirname):
		"""
		通常在子类重写的template_name中调用
		"""
		return dirname + '/' + self.route[-1]

	def page_url(self, route):
		"""
		生成页面url
		/开头的路由表示跨应用
		"""
		route = self.url(route, True) + settings.FILE_EXT
		return route

	def static_url(self, filename, parent=''):
		"""生成静态资源url"""
		if parent and not parent.endswith('/'):
			parent += '/'
		path = app.static_url_path + '/'
		return path + parent + filename

	def img_url(self, filename, parent=True):
		imgdir = 'images'
		if parent is True:
			parent = self.appid
		parent = (parent + '/' + imgdir) if parent else imgdir
		return self.static_url(filename, parent)

	def action(self, name = '', level = 0):
		"""
		生成同级url操作
		:param level: 保留route层数，0为保留至倒数第二层
		"""
		route = list(self.route)
		if level:
			del route[level+1:]
		route[-1] = name
		url = '/' + '/'.join(route)
		if name:
			url += settings.FILE_EXT
		return url

	def get_arg(self, key, default = ''):
		"""获取参数，包括get和form"""
		return self.request.values.get(key, default)

	def get_args(self, keys):
		return extypes.Map({key: self.request.values.get(key, '') for key in keys})

	def get_args_adv(self, keys):
		args = extypes.Dict({})
		for key in keys:
			if extypes.is_list_or_tuple(key):
				key, value_t, default = key
				value = self.request.values.get(key, None)
				if value is not None:
					value = value_t(value)
				else:
					value = default
			else:
				value = self.request.values.get(key, '')
			args[key] = value
		return args

	@property
	def appid(self):
		return self.route[0]

	@property
	def is_get(self):
		return self.request.method == 'GET'

	@property
	def is_post(self):
		return self.request.method == 'POST'

	@property
	def is_ajax(self):
		# return self.request.headers.get('X-Requested-With', '') == 'XMLHttpRequest'
		return self.request.is_xhr

	@property
	def tpl_dir(self):
		"""当前类渲染模板的路径，便于include"""
		return

class AssignableHander(BaseHandler):
	__slots__ = ('variable',)

	def oninit(self):
		self.variable = {}

	def render(self, tpl = None, **data):
		for k, v in self.variable.items():
			data.setdefault(k, v)
		return BaseHandler.render(self, tpl, **data)

	def assign(self, name, value):
		self.variable[name] = value

	def unassign(self, name):
		self.variable.pop(name, None)