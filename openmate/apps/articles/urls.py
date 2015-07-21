# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from articles.models import Article
from articles.feeds import LatestArticlesFeed, LatestArticlesByCategory

feeds = {
    'latest': LatestArticlesFeed,
    'categories': LatestArticlesByCategory,
}

urlpatterns = patterns('',
    # url(r'^feed/$',
    #    'django.contrib.syndication.views.feed', {'feed_dict': feeds, 'url' : 'latest' }, name='articles-feed'),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)

urlpatterns += patterns('articles.views',

    url(r'^tags/$',
        'tags_list',           name='article-tags_list'),

    url(r'^tags/(?P<tag>.*)/$',# [-\w]+)/$',
        'articles_by_tag',    name='article-tags'),

    url(r'^comments/post/$',
        'post_comment',       name='articles-post_comment'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$',
        'article_detail',     name='article_detail'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\w{1,2})/$',
        'article_list_day',   name='article_list_day'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
        'article_list_month', name='article_list_month'),

    url(r'^(?P<year>\d{4})/$',
        'article_list_year',  name='article_list_year'),

    url(r'^$',
        'article_list_index', name='article_list_index'),

    url(r'^submit/$',
        'article_submit',      name='articles-submit'),

    url(r'^submit/sent/$',
        'article_submit_sent',      name='articles-submit-sent'),
        
    url(r'^(?P<category>[-\w]+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\w{1,2})/$',
        'article_list_day',   name='cat_article_list_day'),

    url(r'^(?P<category>[-\w]+)/(?P<year>\d{4})/(?P<month>\d{2})/$',
        'article_list_month', name='cat_article_list_month'),

    url(r'^(?P<category>[-\w]+)/(?P<year>\d{4})/$',
        'article_list_year',  name='cat_article_list_year'),

    url(r'^(?P<category>[-\w]+)/$',
        'article_list_index', name='cat_article_list_index'),

    url(r'^drafts/(?P<article_id>\d+)/$',
        'article_draft',      name='article_draft'),

)

