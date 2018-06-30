from django.shortcuts import render, redirect

from posts.forms import PostForm, PostCreateForm
from .models import Post, Comment

def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts':posts,
    }
    return render(request, 'posts/post_list.html', context)

def post_create(request):
    form = PostCreateForm()
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:post-list')

    context = {
        'form':form,
    }

    return render(request, 'posts/post_create.html', context)

def post_delete(request, pk):
    pass

def comment_list(request):
    pass

def comment_create(request):
    pass

def comment_delete(request, pk):
    pass
