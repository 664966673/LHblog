from django.shortcuts import render,get_object_or_404,redirect

from .models import BlogArticle, Comment
from .form import CommentForm

# Create your views here.

def art_comment(request, art_pk):
    article = get_object_or_404(BlogArticle, pk = art_pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)

            comment.article = article

            comment.save()
            cpk =  comment.pk

            return redirect(article)

        else:
            comment_list = article.comment_set.all()
            context = {
                'article' :article,
                'form' : form,
                'comment_list':comment_list
            }

            return render(request, 'Lblog/detail.html', context=context)

    return redirect(article)
