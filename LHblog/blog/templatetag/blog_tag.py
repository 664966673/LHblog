from ..models import Category,Tag,BlogArticle
from  django import template
from django.db.models.aggregates import Count

register = template.Library()

@register.simple_tag
def get_cates():
    return Category.objects.annotate(num_posts=Count('blogarticle')).filter(num_posts__gt=0)

@register.simple_tag
def get_tags():
    return Tag.objects.all()

@register.simple_tag
def get_archive():
    return BlogArticle.objects.dates('create_time', 'month', order='ASC')

