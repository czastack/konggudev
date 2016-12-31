from .front import require_login, BaseHandler
from . import models

class DefaultHandler(BaseHandler):
	_template_dir = 'article'

	def view(self):
		article = models.Article.find_where(id=self.get_arg('id'))
		if not article:
			return '文章不存在'
		article = article.first()
		article.author = models.User.find_where(id=article.author).first()
		article.content = article.content.replace('\r\n', '\\n')
		return self.render(article=article)