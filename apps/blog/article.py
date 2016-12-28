from .front import require_login, BaseHandler

class DefaultHandler(BaseHandler):
	_template_dir = 'article'

	@require_login
	def publish(self):
		if self.is_get():
			return self.render()
		else:
			pass