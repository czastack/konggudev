from lib.handler import AssignableHander
from . import models

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

	def oninit(self):
		super().oninit()
		self.user = models.User(**self.session['user']) if 'user' in self.session else None

	def article_url(self, item):
		return self.url('article/view?id=%d' % item.id, True)

	def user_url(self, user):
		return self.url('user/index?id=%d' % user.id, True)


class UserGetter:
	__slots__ = ('_data',)

	def __init__(self):
		self._data = {}

	def get(self, user_id):
		user = self._data.get(user_id, None)
		if not user:
			self._data[user_id] = user = models.User.select_where('id', 'username', 'nickname', id=user_id).first()
		return user

	__call__ = get