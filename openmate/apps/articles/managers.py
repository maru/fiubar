from datetime import datetime
from django.db import models

class ArticleManager(models.Manager):

	def published(self):
		'Returns Articles that have a status of "published" and a publish date in the past.'
		from articles.models import Article
		query_set = self.get_query_set()
		qs_filter = query_set.filter(publish_date__lte=datetime.now(), status=Article.PUBLISHED)
		return qs_filter

	def get_by_category_published(self, category):
		return self.published().filter(category=category)

class CategoryManager(models.Manager):

	def choices(self):
		return [(c.slug, c.name) for c in self.all()]
		
	def get_category_list(self, order_by_field):		
		l = []
		from articles.models import Article
		for c in self.order_by(order_by_field):
			if Article.objects.get_by_category_published(c).count() > 0:
				l.append(c)
		return l
	

