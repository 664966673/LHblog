from django.shortcuts import render,get_object_or_404
from django.http import *
from .models import BlogArticle,Category,Tag
from PIL import Image
from django.db.models import Q
import markdown
# Create your views here.

def index(request):
    art_lsit = BlogArticle.objects.all().filter(images = '').order_by('id')
    img_art_list = BlogArticle.objects.all().filter(~Q(images = '')).order_by('-views')
    #压缩上传图片
    for cp in img_art_list:
        image = Image.open(cp.images)  # 通过cp.images 获得图像
        width = image.width
        height = image.height
        rate = 1.0  # 压缩率

        # 根据图像大小设置压缩率
        if width >= 2000 or height >= 2000:
            rate = 0.3
        elif width >= 1000 or height >= 1000:
            rate = 0.5
        elif width >= 500 or height >= 500:
            rate = 0.9

        width = int(width * rate)  # 新的宽
        height = int(height * rate)  # 新的高

        image.thumbnail((width, height), Image.ANTIALIAS)  # 生成缩略图
        image.save('media/' + str(cp.images), 'JPEG')  # 保存到原路径
        cp.save()
    return render(request, "Lblog/index.html", context={'art_lsit': art_lsit, 'img_art_list':img_art_list})

# def category(request, pk):
#     category = get_object_or_404()

def detail(request ,pk):
    article = get_object_or_404(BlogArticle, pk=pk)
    article.increase_view()
    article.content = markdown.markdown(article.content,  extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                  ])
    return render(request, "Lblog/detail.html", context={'article': article})

def category(request, pk):
    cates = get_object_or_404(Category, pk = pk)
    article_list = BlogArticle.objects.filter(category=cates).order_by('-views')
    return render(request, "Lblog/list.html", context={'article_list':article_list,
                                                        'cates':cates
                                                       })

def archive(request, year, month):

    article_list = BlogArticle.objects.filter(create_time__year=year,
                                    create_time__month=month
                                    ).order_by('-create_time')

    return  render(request, "Lblog/list.html",context={'article_list':article_list,
                                                       'year':year,
                                                       'month':month
                                                       })