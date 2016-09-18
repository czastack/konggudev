from flask import render_template as render
from main import app
import settings

# 生成处理器名称
fn = lambda name: name + settings.handle_fn_suffix
cls = lambda name: name.title().replace('-', '') + settings.handle_class_suffix

# 尝试获取处理器
def get_module_handler(module, name, default):
	v = lambda n, f: getattr(module, f(n), None)
	return v(name, fn) or v(name, cls) or v(default, fn) or v(default, cls)

# 预处理路由
def prepare_route(route):
	last = route[-1]
	if last.endswith(settings.FILE_EXT):
		last = last[:-len(settings.FILE_EXT)]
	route[-1] = last

# 找不到控制器时尝试直接渲染路由对应的模板文件
# 要在子模块中import才有效果
# 使用: from . import direct_render as default_handler
def direct_render(handler):
	return handler.render()

class BaseHandler:
	__slots__ = ('route')
	from flask import request, session

	def __init__(self, route):
		self.route = tuple(route)

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
			url = url.replace('@', self.route[1] + '/')
		return url

	def render(self, tpl = None, **data):
		tpl = (tpl or '-'.join(self.route[1:])) + '.html'
		tpl = self.url(tpl)
		return render(tpl, handler=self, settings=settings, **data)

	def page_url(self, route):
		"""
		生成页面url
		/开头的路由表示跨应用
		"""
		route = self.url(route, True) + settings.FILE_EXT
		return route

	def static_url(self, filename, parent = ''):
		"""生成静态资源url"""
		if parent and not parent.endswith('/'):
			parent += '/'
		path = app.static_url_path + '/'
		return path + parent + filename

	def img_url(self, filename, at_root = False):
		imgdir = 'images'
		parent = imgdir if at_root else (self.appid + '/' + imgdir)
		return self.static_url(filename, parent)

	def action(self, name = '', level = 0):
		"""
		生成同级url操作
		:param level: 保留route层数，0为保留至倒数第二层
		"""
		route = list(self.route)
		if name:
			if level:
				del route[level+1:]
			route[-1] = name
		return '/' + '/'.join(route) + settings.FILE_EXT

	def refresh(self):
		return '', 200, {"Refresh": "0"}

	def get_arg(self, key, default = ''):
		"""获取参数，包括get和form"""
		return self.request.values.get(key, default)

	def get_args(self, keys):
		return {key: self.request.values.get(key, '') for key in keys}

	@property
	def appid(self):
		return self.route[0]

	@property
	def home_url(self):
		return self.page_url('index')

	@property
	def is_get(self):
		return self.request.method == 'GET'

	@property
	def is_post(self):
		return self.request.method == 'POST'

	@property
	def is_ajax(self):
		return self.request.headers.get('X-Requested-With', '') == 'XMLHttpRequest'

class AssignableHander(BaseHandler):
	__slots__ = ('variable',)

	def __init__(self, route):
		BaseHandler.__init__(self, route)
		self.variable = {}
		self.oninit()

	def oninit(self):
		pass

	def render(self, tpl = None, **data):
		for k, v in self.variable.items():
			data.setdefault(k, v)
		return BaseHandler.render(self, tpl, **data)

	def assign(self, name, value):
		self.variable[name] = value

	def unassign(self, name):
		self.variable.pop(name, None)