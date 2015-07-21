import xmlrpclib, urllib2
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.contrib.sitemaps import ping_google

# http://help.yahoo.com/l/us/yahoo/search/siteexplorer/manage/siteexplorer-45.html
# http://developer.yahoo.com/search/siteexplorer/V1/ping.html

YAHOO = 'http://search.yahooapis.com/SiteExplorerService/V1/ping?sitemap=%s'

PING_SERVICES = [
		'http://rpc.technorati.com/rpc/ping',
		'http://blogsearch.google.com/ping/RPC2',
		'http://rpc.weblogs.com/RPC2',
		'http://rpc.pingomatic.com',
	]

def send_pings(article, site_url=None, sitemap_url=None, article_url=None, feed_url=None):
	# TODO: Implement more robust logging and exception handling.
	if getattr(settings, 'PING', False):
		site = Site.objects.get_current()
		if site_url is None:
			site_url = u'http://%s' % site.domain
		if sitemap_url is None:
			sitemap_url = u'%s/%s' % (site_url, reverse('sitemap'))
		if article_url is None:
			article_url = u'%s/%s' % (site_url, article.get_absolute_url())
		if feed_url is None:
			feed_url = u'%s/%s' % (site_url, reverse('feed', kwargs={'url':'articles'}))
		for url in PING_SERVICES:
			try:
				s = xmlrpclib.Server(url)
				try:
					reply = s.weblogUpdates.extendedPing(
						site.name,
						site_url,
						article_url,
						feed_url)
				except Exception, e:
					reply =  s.weblogUpdates.ping(site.name, site_url)
			except:
				pass
		urllib2.urlopen(YAHOO % site_url)
		urllib2.urlopen(YAHOO % sitemap_url)
		urllib2.urlopen(YAHOO % feed_url)
		ping_google(sitemap_url)