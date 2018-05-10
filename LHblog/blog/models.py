from django.db import models
from django.contrib.auth.models import User
from  django.urls import reverse
import markdown
from django.utils.html import strip_tags
from django.conf import settings
# Create your models here.
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    class Meta():
        db_table = "category"
        verbose_name = "栏目"
        verbose_name_plural = "栏目"
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta():
        db_table = "Tag"
        verbose_name = "标签"
        verbose_name_plural = "标签"
class BlogArticle(models.Model):

    title = models.CharField(max_length=100, verbose_name="文章列表")
    excerpt = models.CharField(max_length=200, blank=True, verbose_name="摘要")
    content = models.TextField()
    create_time = models.DateTimeField(verbose_name="创建时间")
    update_time = models.DateTimeField(null=True,blank=True)
    author = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="作者")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="类别")
    url_height = models.PositiveIntegerField(default=225)
    url_width = models.PositiveIntegerField(default=300)
    images = models.ImageField(upload_to = 'art_img',  height_field='url_height', width_field='url_width', null=True,blank=True)
    tags = models.ManyToManyField(Tag)
    views = models.PositiveIntegerField(default=0,verbose_name="阅读量")
    show_img = models.BooleanField(default=False)

    def increase_view(self):
        self.views += 1
        self.save(update_fields=['views'])
    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={'pk':self.pk})
    #自动生成摘要
    def save(self, *args, **kwargs):
        # 如果没有填写摘要
        if not self.excerpt:
            # 首先实例化一个 Markdown 类，用于渲染 body 的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
            self.excerpt = strip_tags(md.convert(self.content))[:154]

        # 调用父类的 save 方法将数据保存到数据库中
        super(BlogArticle, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta():
        db_table = "blogarticle"
        verbose_name = "文章列表"
        verbose_name_plural = "文章列表"
#拓展user类
