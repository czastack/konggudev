from .basehandler import require_login, BaseHandler
from . import models, forms
import re

class DefaultHandler(BaseHandler):

	_template_dir = 'mine'

	@require_login
	def oninit(self):
		super().oninit()

		if self.is_get:
			num_data = models.User.select_one(
				'article_count', 'follow_count', 'fans_count', id=self.user.id)

			# 检测是否有变化
			for key, val in num_data.items():
				if val != self.user._data[key]:
					self.user._data[key] = self.session['user'][key] = val

			self.user.avatar = self.config.DEFAULT_AVATAR

			self.assign('user', self.user)
			self.assign('menu', self.config.mineLeftMenu)

	def index(self):
		return self._show()

	def setting(self):
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
		search = self.get_arg('search', None)
		articles = models.Article.find_where(author=self.user.id)
		if search:
			articles = articles.where(models.Article.title % ('%' + search + '%'))
		return self.render(articles=articles)

	def follow(self):
		users = models.Follow.find_where(follower=self.user.id)
		users = (item.target for item in users)
		return self.render(users=users)

	def fans(self):
		users = models.Follow.find_where(target=self.user.id)
		users = (item.follower for item in users)
		return self.render(users=users)

	def publish(self):
		if self.is_get:
			return self.render()
		else:
			data = self._get_article_args()
			data.author = self.user.id
			data.create_time = data.update_time = models.Article.NOW

			models.Article.create(**data)
			return self._show()

	def article_edit(self):
		article_id = self.get_arg('id')
		if self.is_get:
			article = models.Article.find_where(id=article_id)
			if not article:
				return '文章不存在'
			data = article.first()._data
			return self.render(**data)
		else:
			data = self._get_article_args()
			data.update_time = models.Article.NOW
			models.Article.update(**data).where(models.Article.id==article_id).execute()
			return self._show()

	def article_del(self):
		article_id = self.get_arg('id')
		if article_id:
			models.Article.delete().where(models.Article.id==article_id).execute()
			return self._show()

	def _get_article_args(self):
		data = self.get_args(('title', 'tags', 'content', 'description', 'status'))
		data.title = data.title.strip()
		data.tags = re.sub(' *, *', ',', data.tags)
		if data.tags:
			models.ArticleTag.insert_many(({'name': tag} for tag in data.tags.split(','))).upsert(True).execute()
		return data

	def _show(self):
		return self.redirect(self.action('article'))