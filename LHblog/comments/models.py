from django.db import models
from django.contrib.auth.models import User
from blog.models import BlogArticle
from django import forms
from django.conf import settings

# Create your models here.
class Comment(models.Model):
    text = models.TextField()
    article = models.ForeignKey('blog.BlogArticle', on_delete=models.PROTECT)
    create_time = models.DateTimeField(auto_now_add=True)
    #name = models.CharField(max_length=100, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.PROTECT)
    class Meta():
        db_table = "comments"
        verbose_name = "评论"
        verbose_name_plural = "评论"
    def __str__(self):
        return self.text[:20]