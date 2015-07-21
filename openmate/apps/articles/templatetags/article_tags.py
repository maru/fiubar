from django import template
from articles.models import Category, Article

register = template.Library()

class ArticlesNode(template.Node):
  
  def __init__(self, num, varname, filters=None, single_article=False):
    self.num = num
    self.varname = varname
    self.filters = filters
    self.single_article = single_article
    
  def render(self, context):
    articles = Article.objects.published()[:self.num]
    if self.filters:
      articles = articles.filter(**filters)
    if self.single_article:
      try:
        articles = articles[0]
      except IndexError:
        context[self.varname] = None
    context[self.varname] = articles
    return u''
    
@register.tag
def get_articles(parser, token):
  """
  {% get_articles <num> as <varname> %}
  """
  bits = token.split_contents()
  return ArticlesNode(bits[1], bits[3])
  
@register.tag
def get_latest_article(parser, token):
  """
  {% get_latest_article as latest %}
  """
  bits = token.split_contents()
  return ArticleNode(1, bits[2], single_article=True)
  
def category_menu_box(context):
    context.update({
      'category_list' : Category.objects.get_category_list('name'),
    })
    return context
register.inclusion_tag('articles/category_menu_box.html', takes_context=True)(category_menu_box)
  
def tags_menu_box(context):
    # print context['block']) 'add_parent', 'context', 'get_nodes_by_type', 'must_be_first', 'name', 'nodelist', 'parent', 'render', 'source', 'super']
    return context
register.inclusion_tag('articles/tags_menu_box.html', takes_context=True)(tags_menu_box)

@register.tag
def tag_article_cloud(parser, token):
	from tagging.templatetags.tagging_tags import do_tag_cloud_for_model
	from datetime import datetime
	token_copy = token.contents.split()
	token_copy.insert(1, 'articles.Article')
	l = len(token_copy) - 1	
	for i in range(0, l):
		token_copy.insert(i*2+1, ' ')
	token.contents = ''.join(token_copy)
	filters = { 'status' : 'published', 'publish_date__lte' : datetime.now()}
	TagsForModelNode = do_tag_cloud_for_model(parser, token, filters)
	return TagsForModelNode
