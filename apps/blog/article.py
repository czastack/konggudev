from .basehandler import require_login, BaseHandler, UserGetter
from . import models

Article = models.Article

class DefaultHandler(BaseHandler):
	_template_dir = 'article'

	def view(self):
		article_id = self.get_arg('id')
		article = Article.filter(id=article_id)
		if not article:
			return '文章不存在'

		# 更新访问量
		Article.update(view_count=Article.view_count+1).where(Article.id==article_id).execute()
		
		article = article.first()
		hot = self._hot().where(Article.id != article_id)

		return self.render(
			article=article,
			hot=hot,
			author_other=hot.where(Article.author_id == article.author_id),
			comments=models.ArticleComment.find_where(article=article_id),
			getuser=UserGetter(),
			id=id
		)

	@require_login
	def comment(self):
		if self.is_post:
			article_id = self.get_arg('id')
			body = self.get_arg('body')
			models.ArticleComment.create(article=article_id, body=body, user=self.user.id, time=Article.NOW)
			return self.redirect(self.action('view') + "?id=" + article_id)
		else:
			return self.goback()

	def _hot(self):
		"""热门文章"""
		return Article.find_public().select(Article.id, Article.title).limit(10).order_by(Article.view_count.desc())