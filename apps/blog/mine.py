from .front import require_login, BaseHandler
from . import models, forms
import re

class DefaultHandler(BaseHandler):

	_template_dir = 'mine'

	@require_login
	def oninit(self):
		super().oninit()
		self.assign('base', {
			"nickname": self.user.getname(),
			"avatar": self.config.DEFAULT_AVATAR,
			"gender": 1,
			"email": self.user.email,
			"article_num": 22,
			"follow_num": 22,
			"fans_num": 22,
		})

	def index(self):
		return self.render()

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
		articles = models.Article.find_where(author=self.user.id)
		return self.render(articles=articles)

	def follow(self):
		return self.render()

	def fans(self):
		return self.render()

	def publish(self):
		if self.is_get:
			return self.render()
		else:
			data = self._get_article_args()
			data.author = self.user.id
			data.create_time = data.update_time = models.Article.NOW

			models.Article.create(**data)
			return self.redirect(self.action('article'))

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
			return self.redirect(self.action('article'))

	def _get_article_args(self):
		data = self.get_args(('title', 'tags', 'content', 'status'))
		data.title = data.title.strip()
		data.tags = re.sub(' *, *', ',', data.tags)
		return data