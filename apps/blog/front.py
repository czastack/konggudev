from lib.handler import AssignableHander

# def edit_handle(handler):
# 	return handler.render()

# def test_handle(handler):
# 	return handler.json({"task": "上学/go"})

def require_login(func):
	def _deco(handler):
		if 'user' in handler.session:
			handler.user = handler.session['user']
			return func(handler)
		# 记录当前路径以便登录后跳转
		handler.session['refer'] = handler.request.url
		return handler.redirect(handler.url('login', True))
	return _deco

class DefaultHandler(AssignableHander):
	__slots__ = ('user',)
	
	from . import config

	def template_name(self):
		return self.template_on_dir('front')

	def index(self):
		return self.render()

	def hot(self):
		return self.render()

	def type(self):
		return self.render()

	@require_login
	def mine(self):
		return self.render()

	def login(self):
		if self.is_get:
			return self.render() # (form = forms.LoginForm())
		else:
			pass

	def test(self):
		return self.get_args_adv(('username', 'password', ('age', int, 0)))