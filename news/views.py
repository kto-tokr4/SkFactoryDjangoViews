from django.shortcuts import render, HttpResponse
from .models import Post



def news_list(request):
    posts = Post.objects.order_by('-created')
    return render(request, 'news/list.html', {'posts':posts})

def news_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'news/detail.html',{'post':post})
