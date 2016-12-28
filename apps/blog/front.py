from lib.handler import AssignableHander
from lib import utils
from . import models, forms
import hashlib

def require_login(func):
	def _deco(handler):
		if 'user' in handler.session:
			return func(handler)
		# 记录当前路径以便登录后跳转
		handler.session['refer'] = handler.request.url
		return handler.redirect(handler.url('login', True))
	return _deco

def edit_handle(handler):
	return handler.render()

class BaseHandler(AssignableHander):
	__slots__ = ('user',)
	
	from . import config


class DefaultHandler(BaseHandler):

	_template_dir = 'front'

	def oninit(self):
		super().oninit()
		if 'user' in self.session:
			self.user = models.User(**self.session['user'])
		title = utils.get_item(self.config.topnav, self.route[-1])
		if title:
			self.assign('title', title)

	def index(self):
		return self.render()

	def hot(self):
		return self.render()

	def type(self):
		return self.render()

	def login(self):
		if self.is_get:
			return self.render()
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

	@staticmethod
	def sha1_pwd(data):
		data.password = hashlib.sha1(data.password.encode()).hexdigest()

	def test(self):
		return self.get_args_adv(('username', 'password', ('age', int, 0)))


class MineHandler(BaseHandler):

	_template_dir = 'mine'

	@require_login
	def oninit(self):
		super().oninit()
		self.user = models.User(**self.session['user'])
		self.assign('base', {
			"nickname": self.user.getname(),
			"avatar": self.config.DEFAULT_AVATAR,
			"gender": 1,
			"email": self.user.email,
			"article_num": 22,
			"attention_num": 22,
			"fans_num": 22,
		})

	def index(self):
		return self.render()

	def edit(self):
		if self.is_get:
			form = forms.PersonInfoForm(self.user._data)
			return self.render(form=form)
		else:
			form = forms.PersonInfoForm(self.request.form)
			form.data.popif('username')
			self.user.setdata(form.data)
			self.user.save()
			self.session['user'] = self.user._data
			return self.STAY

	def collection(self):
		return self.render()

	def comments(self):
		return self.render()

	def article(self):
		return self.render()

	def attention(self):
		return self.render()

	def fans(self):
		return self.render()