# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from tagging.fields import TagField
from articles.managers import ArticleManager, CategoryManager
from django.conf import settings
from openmate.core.storage import RescaleImageSystemStorage as storage

ARTICLES_IMG_WIDTH = getattr(settings, 'ARTICLES_IMG_WIDTH', 220)
ARTICLES_IMG_HEIGHT = getattr(settings, 'ARTICLES_IMG_HEIGHT', 100)

def upload_dir_image(article, file_name):
	return 'articles/%04d/%02d/%s' % (article.publish_date.year, article.publish_date.month, file_name)

class Category(models.Model):
	name = models.CharField(max_length=100)
	description = models.CharField(blank=True, max_length=500)
	slug = models.SlugField(max_length=100, unique=True)

	objects = CategoryManager()
	
	def __unicode__(self):
		return self.name

	@models.permalink
	def get_absolute_url(self):
		return ('cat_article_list_index', (), {'category':self.slug})

	class Meta:
		verbose_name_plural = 'categories'
		ordering = ('name',)


class Article(models.Model):

	DRAFT = 'draft'
	MODERATED = 'moderated'
	PUBLISHED = 'published'

	objects = ArticleManager()

	# TODO: Add ``Location`` model
	category = models.ForeignKey(Category)
	title = models.CharField(max_length=200)
	body = models.TextField()
	tags = TagField(max_length=100, blank=True)
	publish_date = models.DateTimeField(default=datetime.now,
				help_text=u'You may future-date articles to enable scheduled publishing.')
	status = models.CharField(max_length=100, choices=((DRAFT, 'Draft'),(PUBLISHED, 'Published'),(MODERATED, 'Moderated')),
				default=DRAFT, help_text=u'Only articles with "Published" status will be shown on site.')
	author = models.ForeignKey(User)
	featured = models.BooleanField(default=False)
	related_articles = models.ManyToManyField('Article', blank=True, null=True)
	slug = models.SlugField(max_length=200, unique=True,
				help_text=u'It is recommended to use the default slug.')
	allow_comments = models.BooleanField(default=True)
	summary = models.CharField(blank=True, max_length=500)
	snippet = models.TextField(blank=True)
	orig_link = models.URLField(verify_exists=False, blank=True, null=True)
	image = models.ImageField(upload_to=upload_dir_image, storage=storage(width=ARTICLES_IMG_WIDTH, height=ARTICLES_IMG_HEIGHT, canvas='rel'), blank=True, null=True, help_text=u'Max dimensions: %dpx, %dpx' % (ARTICLES_IMG_WIDTH, ARTICLES_IMG_HEIGHT))

	def __unicode__(self):
		return self.title

	def save(self):
		self.save_snippet()
		super(Article, self).save()
		if self.is_published():
			from articles.pings import send_pings
			send_pings(self)

	def update(self, user, d):
		self.title = d.get('title')
		self.body = d.get('body')
		self.category = Category.objects.get(slug=d.get('category'))
		self.tags = d.get('tags', None)
		self.author = User.objects.get(username=user.username)
		self.orig_link = d.get('orig_link', None)
		self.image = d.get('image', None)

		self.publish_date = d.get('publish_date', datetime.now())
		self.snippet = d.get('snippet', self.save_snippet())
		self.status = d.get('status', self.DRAFT)
		self.slug = d.get('slug', datetime.now())
		
		# self.featured = d.get('featured', None)
		# self.related_articles = d.get('related_articles', None)
		# self.allow_comments = d.get('allow_comments', None)
		# self.summary = d.get('summary', None)

	def save_snippet(self):
		if self.snippet and len(self.snippet) > 0:
			return
		body_p = self.body.splitlines()
		# Count lines in body_p
		p0_lines = body_p[0].split('.')
		if len(p0_lines) - 1 > 3:
			snippet = p0_lines[0] + '.' + p0_lines[1] + '.' + p0_lines[2] + '.'
		else:
			snippet = body_p[0]
		self.snippet = snippet

	def is_published(self):
		return self.status == Article.PUBLISHED and self.publish_date <= datetime.now()

	def description(self):
		return self.snippet

	@models.permalink
	def get_absolute_url(self):
		if self.is_published():
			return ('article_detail', (), {
			'year': self.publish_date.strftime('%Y'),
			'month': self.publish_date.strftime('%m'),
			'day': self.publish_date.strftime('%d'),
			'slug': self.slug
			})
		else:
			return ('article_draft', (), {
			'article_id': self.id
			})

	def get_edit_url(self):
		return u'/admin/articles/article/%d' % self.id

	def get_image_url(self):
		if self.image:
			return self.image.url
		return ''

	def approved_comments(self):
		try:
			from django.contrib.comments.models import Comment
			return Comment.objects.approved_for_object(self)
		except ImportError:
			return []

	def get_published_prev(self):
		try:
			a = self.get_previous_by_publish_date(publish_date__lte=datetime.now(), status=Article.PUBLISHED)
		except:
			return None
		return a

	def get_published_next(self):
		try:
			a = self.get_next_by_publish_date(publish_date__lte=datetime.now(), status=Article.PUBLISHED)
		except:
			return None
		return a

	class Meta:
		ordering = ('-publish_date', '-id')
