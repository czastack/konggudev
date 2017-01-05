from .basehandler import require_login, BaseHandler
from . import models
from lib import utils
import hashlib

class DefaultHandler(BaseHandler):

	_template_dir = 'front'

	def oninit(self):
		super().oninit()
		title = utils.get_item(self.config.topnav, self.route[-1])
		if title:
			self.assign('title', title)

	def index(self):
		search = self.get_arg('search', None)
		articles = self.list_articles_desc('update_time')
		if search:
			articles = articles.where(models.Article.title % ('%' + search + '%'))
		return self.render(articles=articles)

	def hot(self):
		search = self.get_arg('search', None)
		articles = self.list_articles_desc('view_count')
		if search:
			articles = articles.where(models.Article.title % ('%' + search + '%'))
		return self.render(articles=articles)

	def type(self):
		data = self.get_args(('tag',))
		data.tags = (tag.name for tag in models.ArticleTag.find())
		if data.tag:
			data.articles = self.list_articles_desc('create_time').where(models.Article.tags % ('%' + data.tag + '%'))
		return self.render(**data)

	def login(self):
		if self.is_get:
			_next = self.get_arg('next', None)
			if _next == '':
				_next = self.request.headers.get('referer', None)
			if _next:
				self.session.setdefault('refer', _next)
			return self.render()
		else:
			data = self.get_args(('username', 'password'))
			self.sha1_pwd(data)
			user = models.User.find_where(**data).first()
			if user:
				self.session['user'] = user._data
				return self.redirect(self.session.pop('refer', self.action('index')))
			else:
				return self.render(username=data['username'], err='用户名或密码错误')

	def logout(self):
		self.session.pop('user', None)
		return self.redirect(self.action('login'))

	def register(self):
		if self.is_get:
			return self.render()
		else:
			data = self.get_args(('username', 'password', 'email'))
			if models.User.find_where(username=data.username).count():
				data.err='用户名已被注册'
			elif models.User.find_where(email=data.email).count():
				data.err='邮箱已被注册'
			if data.err:
				del data.password
				return self.render(**data)
			
			self.sha1_pwd(data)
			models.User.create(**data)
			return self.redirect(self.action('login'))

	def list_articles_desc(self, order_by):
		return models.Article.find_public().limit(10).order_by(getattr(models.Article, order_by).desc())

	@staticmethod
	def sha1_pwd(data):
		data.password = hashlib.sha1(data.password.encode()).hexdigest()