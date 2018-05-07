from ..models import Category,Tag,BlogArticle
from  django import template


register = template.Library()

@register.simple_tag
def get_cates():
    return  Category.objects.all()

@register.simple_tag
def get_tags():
    return Tag.objects.all()

@register.simple_tag
def get_archive():
    return BlogArticle.objects.dates('create_time', 'month', order='ASC')


