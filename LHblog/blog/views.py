from django.shortcuts import render,get_object_or_404
from django.http import *
from .models import BlogArticle,Category,Tag
from PIL import Image
from django.db.models import Q
import markdown
from comments.form import CommentForm
from social_django.models import UserSocialAuth
from  .models import User
# Create your views here.
from django.views.generic import ListView, DetailView
from django.core.paginator import PageNotAnInteger,EmptyPage,Paginator
#首页
class IndexView(ListView):
    model = BlogArticle
    template_name = 'Lblog/index.html'
    context_object_name = 'art_List'
    paginate_by = 5
    def get_queryset(self):
        art_List =  BlogArticle.objects.all().filter(~Q(images = '')).order_by('-views')
        for cp in art_List:
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
        return super(IndexView, self).get_queryset()
# def index(request):
#     art_lsit = BlogArticle.objects.all().filter(images = '').order_by('id')
#     img_art_list = BlogArticle.objects.all().filter(~Q(images = '')).order_by('-views')
#     #压缩上传图片
#     for cp in img_art_list:
#         image = Image.open(cp.images)  # 通过cp.images 获得图像
#         width = image.width
#         height = image.height
#         rate = 1.0  # 压缩率
#
#         # 根据图像大小设置压缩率
#         if width >= 2000 or height >= 2000:
#             rate = 0.3
#         elif width >= 1000 or height >= 1000:
#             rate = 0.5
#         elif width >= 500 or height >= 500:
#             rate = 0.9
#
#         width = int(width * rate)  # 新的宽
#         height = int(height * rate)  # 新的高
#
#         image.thumbnail((width, height), Image.ANTIALIAS)  # 生成缩略图
#         image.save('media/' + str(cp.images), 'JPEG')  # 保存到原路径
#         cp.save()
#     return render(request, "Lblog/index.html", context={'art_lsit': art_lsit, 'img_art_list':img_art_list})
#
# # def category(request, pk):
# #     category = get_object_or_404()
#

#详情页面

class DetailView(DetailView):
    model = BlogArticle
    template_name = 'Lblog/detail.html'
    context_object_name = 'article'

    def get(self, request, *args, **kwargs):
        response = super(DetailView,self).get(request, *args, **kwargs)

        self.object.increase_view()
        return response
    def get_object(self, queryset = None):
        article = super(DetailView, self).get_object(queryset=None)
        article.content = markdown.markdown(article.content, extensions=[
                                             'markdown.extensions.extra',
                                             'markdown.extensions.codehilite',
                                             'markdown.extensions.toc',
                                          ])
        return article

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all().order_by('-create_time')
        cpk = comment_list.order_by('create_time').last()
        if cpk:
            context.update({
                    'form': form,
                    'comment_list': comment_list,
                    'cpk':int(cpk.pk) +1,
                    #'userinfo':profile_image_url

                })
        else:
            context.update({
                'form': form,
                'comment_list': comment_list,
                #'cpk': int(cpk.pk) + 1,
                # 'userinfo':profile_image_url

            })
        return context

# def detail(request ,pk):
#     article = get_object_or_404(BlogArticle, pk=pk)
#     article.increase_view()
#     article.content = markdown.markdown(article.content,  extensions=[
#                                      'markdown.extensions.extra',
#                                      'markdown.extensions.codehilite',
#                                      'markdown.extensions.toc',
#                                   ])
#     form = CommentForm()
#     comment_list = article.comment_set.all()
#     cpk = comment_list.order_by('create_time').last()
#
#     # if  User.is_authenticated:
#     #     user = request.user
#     #     userinfo = UserSocialAuth.objects.get(user=user)
#     #     profile_image_url = userinfo.extra_data['profile_image_url']
#
#         # if userinfo.user_id == User.pk :
#         #     pass
#
#     context = {
#         'article': article,
#         'form': form,
#         'comment_list': comment_list,
#         'cpk':cpk,
#         #'userinfo':profile_image_url
#
#     }
#     return render(request, 'Lblog/detail.html', context=context)

#分类页面
class CategoryView(IndexView):
    template_name = 'Lblog/list.html'
    paginate_by = 10
    def get_queryset(self):
        cates = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView,self).get_queryset().filter(category=cates)

    def get_context_data(self, **kwargs):
        kwargs['cates'] = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(IndexView, self).get_context_data(**kwargs)
# def category(request, pk):
#     cates = get_object_or_404(Category, pk = pk)
#     article_list = BlogArticle.objects.filter(category=cates).order_by('-views')
#     return render(request, "Lblog/list.html", context={'article_list':article_list,
#                                                         'cates':cates
#                                                        })



#归档页面
class ArchiveView(IndexView):
    template_name = 'Lblog/list.html'
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchiveView,self).get_queryset().filter(create_time__year=year,
                                            create_time__month=month
                                            ).order_by('-create_time')
    def get_context_data(self, **kwargs):
        kwargs['year'] = self.kwargs.get('year')
        kwargs['month'] = self.kwargs.get('month')
        return super(IndexView, self).get_context_data(**kwargs)

# def archive(request, year, month):
#
#     article_list = BlogArticle.objects.filter(create_time__year=year,
#                                     create_time__month=month
#                                     ).order_by('-create_time')
#
#     return  render(request, "Lblog/list.html",context={'art_List':article_list,
#                                                        'year':year,
#                                                        'month':month
#                                                        })


