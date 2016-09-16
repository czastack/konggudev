def exit(handler):
	from flask import request
	func = request.environ.get('werkzeug.server.shutdown')
	if func is None:
		raise RuntimeError('Not running')
	func()
	return '退出系统'

def reload(handler):
	import uwsgi
	uwsgi.reload()
	return '重启uwsgi'