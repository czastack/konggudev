from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import types, settings

app = Flask(__name__)
# 加载额外配置
app.config.update(settings.config)
# 初始化数据库连接
db = SQLAlchemy(app, session_options={"autoflush": False})

if __name__ == '__main__':
	import sys
	sys.modules['main'] = sys.modules[__name__]
	del sys

# 加载自定义标签拓展
from lib.taglib import TAGS
for tag in TAGS:
	app.jinja_env.add_extension(tag)
del TAGS

# 加载自定义过滤器
from lib.filters import FILTERS
for fn in FILTERS:
	app.add_template_filter(fn)
del FILTERS

from lib import handler

@app.route('/<path:url>', methods=['GET', 'POST'])
def default(url):
	# 1: app, 2: module, 3: function or class, 4: method
	route = url.split('/', 4)
	handler.prepare_route(route)
	IDX = 'index'
	index = lambda: route.append(IDX) or IDX
	len(route) == 1 and index()
	for i in range(len(route)):
		if not route[i]:
			route[i] = IDX
	# 调用对应的类或函数
	try:
		module = __import__('apps.' + route[0], fromlist=[route[1]]).__dict__[route[1]]
		# 如果路由只有2层，则调用该模块下的index函数处理
		# 3层：调用模块下route[1]同名函数处理，
		# 若未找到，调用模块下default_handler函数处理
		# 4层：调用模块下的类/方法
		if isinstance(module, types.ModuleType):
			callee = handler.get_module_handler(module, index() if len(route) == 2 else route[2], 'default')
		else:
			callee = module
		if isinstance(callee, types.FunctionType):
			result = callee(handler.BaseHandler(route))
		elif isinstance(callee, type):
			action = index() if len(route) < 4 else route[3] # 方法名
			method = getattr(callee, action, None) or getattr(callee, 'default', None)
			if method:
				ins = callee(route)
				before = getattr(ins, 'before', None)
				result = (before and before()) or method(ins)
			else:
				raise Exception('%s不存在%s方法' % (callee.__name__, action))
		else:
			raise Exception('404')
	except Exception as e:
		import traceback
		result = traceback.format_exc()
	if not (isinstance(result, str) or isinstance(result, tuple) or result.__class__.__name__ == 'Response'):
		result = str(result)
	return result

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, threaded=True)