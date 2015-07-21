from django.contrib import admin
from articles.models import Category, Article

class CategoryAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)

class ArticleAdmin(admin.ModelAdmin):
  fieldsets = (
    ('Article content', {
      'fields': ('title', 'body', 'category', 'tags', 'author', 'orig_link', 'image')
    }),
    ('Publication info', {
      #'classes': ('collapse',),
      'fields': ('status', 'publish_date')
    }),
    ('Advanced', {
      #'classes': ('collapse',),
      'fields': ('featured', 'allow_comments', 'summary', 'snippet', 'slug',)
    }),
  )

  radio_fields = {'status': admin.VERTICAL}
  prepopulated_fields = {'slug': ('title',)}

  list_display = ('title', 'tags', 'author', 'publish_date', 'get_absolute_url', 'status')
  list_filter = ('publish_date', 'status', 'category',)
  date_hierarchy = 'publish_date'
  search_fields = ('tags', 'title', 'body')

admin.site.register(Article, ArticleAdmin)
