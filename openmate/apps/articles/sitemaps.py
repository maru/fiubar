from django.contrib.sitemaps import Sitemap
from articles.models import Article

class ArticleSitemap(Sitemap):
	changefreq = "never"
	priority = 0.7

	def items(self):
		return Article.objects.published()

	def lastmod(self, obj):
		return obj.publish_date