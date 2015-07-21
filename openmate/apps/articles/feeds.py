from django.contrib.syndication.feeds import Feed, FeedDoesNotExist
from django.contrib.sites.models import Site
from django.db.models import permalink
from articles.models import Article, Category
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

ARTICLES_PAGINATED_BY = getattr(settings, 'ARTICLES_PAGINATED_BY', 10)

class LatestArticlesFeed(Feed):
	"An RSS feed of the latest articles."
	# TODO: More fully implement the available hooks found at:
	# http://www.djangoproject.com/documentation/syndication_feeds/#feed-class-reference
	# categories, copyright, author_name, author_email, etc.
	current_site = Site.objects.get_current()
	link = 'http://%s/' % current_site.domain

	def __init__(self, *args, **kwargs):
		self.site = Site.objects.get_current()
		super(LatestArticlesFeed, self).__init__(*args, **kwargs)

	def title(self):
		return _("%s: Latest articles") % self.site.name

	def description(self):
		return _("Latest articles from %s") % self.site.name

	#@permalink
	#def link(self):
	#	return ('article_list_index', (), {})

	def items(self):
		return Article.objects.published()[:ARTICLES_PAGINATED_BY]

	def item_pubdate(self, item):
		return item.publish_date


class LatestArticlesByCategory(Feed):
	"An RSS feed of the latest articles."
	# TODO: More fully implement the available hooks found at:
	# http://www.djangoproject.com/documentation/syndication_feeds/#feed-class-reference
	# categories, copyright, author_name, author_email, etc.

	def __init__(self, *args, **kwargs):
		self.site = Site.objects.get_current()
		super(LatestArticlesByCategory, self).__init__(*args, **kwargs)

	def title(self, obj):
		return _("%s: Latest articles for %s") % (self.site.name, obj.category)

	def description(self, obj):
		return _("Latest articles for category %s") % (obj.category)

	def link(self, obj):
		if not obj:
			raise FeedDoesNotExist
		return obj.get_absolute_url()

	def items(self, obj):
		return Article.objects.published().filter(category__id__exact=obj.id)[:ARTICLES_PAGINATED_BY]

	def item_pubdate(self, item):
		return item.publish_date

	def get_object(self, bits):
		# In case of "/rss/beats/0613/foo/bar/baz/", or other such clutter,
		# check that bits has only one member.
		if len(bits) != 1:
			raise FeedDoesNotExist
		return Article.objects.get(category__slug__exact=bits[0])

