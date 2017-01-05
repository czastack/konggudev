from .basehandler import require_login, BaseHandler
from . import models, forms

class DefaultHandler(BaseHandler):

	_template_dir = 'user'

	def oninit(self):
		super().oninit()
		user_id = self.get_arg('id')

		if self.user and self.user.id == int(user_id):
			return self.redirect(self.page_url('mine'))
		
		self.target = models.User.find_where(id=user_id).first()
		self.target.avatar = self.config.DEFAULT_AVATAR
		self.assign('user', self.target)
		self.assign('menu', self.config.userLeftMenu)

	def index(self):
		return self.redirect(self.action('article'))

	def article(self):
		search = self.get_arg('search', None)
		articles = models.Article.find_public().where(models.Article.author==self.target.id)
		if search:
			articles = articles.where(models.Article.title % ('%' + search + '%'))
		return self.render(articles=articles)

	def info(self):
		form = forms.PersonInfoForm(self.target._data)
		return self.render(form=form)

	def follow(self):
		users = models.Follow.find_where(follower=self.target.id)
		users = (item.target for item in users)
		return self.render(users=users)

	def fans(self):
		users = models.Follow.find_where(target=self.target.id)
		users = (item.follower for item in users)
		return self.render(users=users)

	def dofollow(self):
		if not self.followed():
			models.Follow.create(follower=self.user.id, target=self.target.id)
		return self.goback()

	def unfollow(self):
		models.Follow.delete().where(models.Follow.follower==self.user.id, models.Follow.target==self.target.id).execute()
		return self.goback()

	def action(self, name):
		return super().action(name) + '?' + self.request.query_string.decode()

	def followed(self):
		return models.Follow.find().where(models.Follow.follower==self.user.id, models.Follow.target==self.target.id).count() != 0