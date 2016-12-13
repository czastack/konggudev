from flask import Flask
import settings

app = Flask(__name__)
# 加载额外配置
app.config.update(settings.config)

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
	return handler.dispatch(url)

@app.route('/')
def index():
	return default('')

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, threaded=True)