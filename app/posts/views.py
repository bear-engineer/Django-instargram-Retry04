from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404

from posts.forms import PostForm, PostCreateForm
from .models import Post, Comment

def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts':posts,
    }
    return render(request, 'posts/post_list.html', context)

@login_required(redirect_field_name='posts:post-create')
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
    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        if request.user.username:
            if post.author.username == request.user.username:
                post.delete()
            else:
                raise PermissionDenied('지울수 있는 권한이 없습니다.')
        else:
            redirect('members:sign-in')
    return redirect('posts:post-list')

def comment(request, post_pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_pk)
        content = request.POST['content']
        if not content:
            raise PermissionDenied('내용을 입력해주세요')
        if not request.user.username:
            return redirect('members:sign-in')
        Comment.objects.create(
            post=post,
            author=request.user,
            content=content,
        )

        return redirect('posts:post-list')

def comment_create(request):
    pass

def comment_delete(request, pk):
    pass
