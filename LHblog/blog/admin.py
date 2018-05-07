from django.contrib import admin
from .models import *

class BlogArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'excerpt', 'author', 'views', 'category', 'create_time']
    list_per_page = 10
    list_display_links = ('title', 'author')
    list_filter = ( 'author', 'category')
    #search_fields = ()
    date_hierarchy = 'create_time'



class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

class TagAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(BlogArticle,BlogArticleAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Tag,TagAdmin)

admin.site.site_header = '李恒博客站点'
admin.site.site_title = '李恒博客'

