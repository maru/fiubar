# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from articles.models import Category, Article
from articles.forms import ArticleForm, ArticlePreviewForm
from django.template.loader import render_to_string
from django.conf import settings

ARTICLES_PAGINATED_BY = getattr(settings, 'ARTICLES_PAGINATED_BY', 9)

def article_list_index(request, *args, **kwargs):
  from django.views.generic.list_detail import object_list

  queryset = Article.objects.published()
  extra_context = {}

  if kwargs.get('category', None):
	category = get_object_or_404(Category, slug=kwargs.pop('category'))
	queryset = queryset.filter(category=category)
	extra_context.update({ 'category' : category })
  kwargs.update({
	'queryset': queryset,
	'paginate_by': ARTICLES_PAGINATED_BY,
	'page': request.GET.get('page', 1),
	'allow_empty': True,
	'template_object_name': 'article',
	'extra_context' : extra_context,
  })
  return object_list(request, *args, **kwargs)

def article_detail(request, *args, **kwargs):
  from django.views.generic.date_based import object_detail
  # category = get_object_or_404(Category, slug=kwargs.pop('category'))
  kwargs.update({
	'queryset': Article.objects.published(),
	'date_field': 'publish_date',
	'slug_field': 'slug',
	'template_object_name': 'article',
	'month_format': '%m',
  })
  return object_detail(request, *args, **kwargs)

def article_draft(request, article_id):
  if not request.user.is_authenticated():
    from django.http import HttpResponseServerError
    raise Http404()
  article = get_object_or_404(Article, pk=article_id, status=Article.DRAFT)
  return render_to_response([
	'articles/article_draft.html',
	'articles/article_detail.html',
  ], {'article':article, 'is_draft': True}, context_instance=RequestContext(request))

def article_list_day(request, *args, **kwargs):
  from django.views.generic.date_based import archive_day
  return archive_day(request, *args, **kwargs)

def article_list_month(request, *args, **kwargs):
  from django.views.generic.date_based import archive_month

  queryset = Article.objects.published() # filter(publish_date__year=year)
  title = u'article año %s %s' % (month_name(kwargs.get('month')), kwargs.get('year'))
  category = None

  if kwargs.get('category', None):
	category = kwargs.pop('category')
	queryset = queryset.filter(category__slug=category)
	title = title + ' de ' + Category.objects.get(slug=category).name

  extra_context = {
	'category' : category,
	'title' : title,
  }
  kwargs.update({
	'queryset' : queryset,
	'date_field' : 'publish_date',
	'template_name' : 'articles/article_list.html',
	'template_object_name' : 'article',
	'allow_empty' : True,
	'month_format' : r'%m',
	'allow_future' : True,
	'extra_context' : extra_context,
  })
  return archive_month(request, *args, **kwargs)

def article_list_year(request, *args, **kwargs):
  from django.views.generic.date_based import archive_year

  queryset = Article.objects.published() # filter(publish_date__year=year)
  title = u'article año ' + kwargs.get('year')
  category = None

  if kwargs.get('category', None):
	category = kwargs.pop('category')
	queryset = queryset.filter(category__slug=category)
	title = title + ' de ' + Category.objects.get(slug=category).name

  extra_context = {
	'category' : category,
	'title' : title,
  }
  kwargs.update({
	'queryset' : queryset,
	'date_field' : 'publish_date',
	'template_name' : 'articles/article_list.html',
	'template_object_name' : 'article',
	'make_object_list' : True,
	'allow_future' : True,
	'extra_context' : extra_context,
  })
  return archive_year(request, *args, **kwargs)

def article_list_index_(request, *args, **kwargs):
  from django.views.generic.date_based import archive_index

  queryset = Article.objects.published()
  category = None
  if kwargs.get('category', None):
	category = kwargs.pop('category')
	queryset = queryset.filter(category__slug=category)

  extra_context = {
	'category' : category,
  }
  kwargs.update({
	'queryset' : queryset,
	'date_field' : 'publish_date',
	'template_name' : 'articles/article_list.html',
	'template_object_name' : 'article_list',
	'allow_future' : True,
	'extra_context' : extra_context,
  })
  return archive_index(request, *args, **kwargs)

def tags_list(request, *args, **kwargs):
	"""Show all tags used in articles"""
	from django.views.generic.simple import direct_to_template
	extra_content = {}
	kwargs.update({ 'template' : 'articles/tags_list.html',
	  'extra_content' : extra_content,
	})
	return direct_to_template(request, **kwargs)

def articles_by_tag(request, *args, **kwargs):
	"""Show articles matching selected tag"""
	from tagging.views import tagged_object_list
	kwargs.update({ 'template_object_name' : 'article',
	  'template_name' : 'articles/article_list.html',
	  'queryset_or_model' : Article.objects.published(),
	  'paginate_by': ARTICLES_PAGINATED_BY,
	  'page': request.GET.get('page', 1),
	})
	return tagged_object_list(request, **kwargs)

@login_required
def post_comment(request):
	# Call post comment function
	from django.contrib.comments.views import comments
	next = request.POST.get('next', '/')

	try:
		response = comments.post_comment(request, next)
	except:
		return HttpResponseRedirect('/noticias/')

	# Clean url
	url_redirect = response.get('Location', '')
	end = url_redirect.find('?')
	if end > 0:
		response['Location'] = url_redirect[:end] + '#respond'

	return response

@login_required
def article_submit(request):
	if request.method == 'POST':
		form = ArticleForm(request.POST)
		if form.is_valid():
			# Preview article
			if request.POST.get('action') == u'Vista previa':
				article = form.create_article(request.user)
				form = ArticlePreviewForm(request.POST)
				return render_to_response('articles/article_preview.html', 
					{ 'form' : form, 'article' : article }, context_instance=RequestContext(request))			
			# Edit article
			if request.POST.get('action') == u'Editar':
				return render_to_response('articles/article_submit.html', 
					{ 'form' : form }, context_instance=RequestContext(request))			
			# Submit article
			if request.POST.get('action') == u'Enviar noticia':
				article = form.save(request.user)
				from django.core.mail import send_mail
				from django.conf import settings
				from_email = '"%s" <%s>' % (request.user.get_full_name(), request.user.email)
				subject = u'Nueva noticia'
				message = render_to_string('articles/new_article_email.txt',
										   { 'article': article, })
				send_mail(subject, message, from_email, [a[1] for a in settings.MANAGERS])
				return HttpResponseRedirect('/noticias/submit/sent/')
		
	else:
		form = ArticleForm()
	return render_to_response('articles/article_submit.html', 
		{ 'form' : form },
		context_instance=RequestContext(request))

def article_submit_sent(request):
	return render_to_response('articles/article_submit.html', 
		context_instance=RequestContext(request))
