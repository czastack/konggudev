from lib.handler import AssignableHander
from . import models
import hashlib

# def edit_handle(handler):
# 	return handler.render()

# def test_handle(handler):
# 	return handler.json({"task": "上学/go"})

def require_login(func):
	def _deco(handler):
		if handler.user:
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

	def oninit(self):
		super().oninit()
		if 'user' in self.session:
			self.user = models.User(**self.session['user'])

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
			data = self.get_args(('username', 'password'))
			self.sha1_pwd(data)
			user = models.User.find().filter(**data).first()
			if user:
				self.session['user'] = user._data
				return self.redirect(self.session.pop('refer', self.action('index')))
			else:
				return self.render(err='用户名或密码错误')

	def logout(self):
		self.session.pop('user', None)
		return self.redirect(self.action('login'))

	def register(self):
		if self.is_get:
			return self.render()
		else:
			data = self.get_args(('username', 'password', 'email'))
			if models.User.find().filter(username=data.username).count():
				return self.render(err='用户名已被注册')
			if models.User.find().filter(email=data.email).count():
				return self.render(err='邮箱已被注册')
			
			self.sha1_pwd(data)
			models.User.create(**data)
			return self.redirect(self.action('login'))

	def sha1_pwd(self, data):
		data.password = hashlib.sha1(data.password.encode()).hexdigest()

	def test(self):
		return self.get_args_adv(('username', 'password', ('age', int, 0)))