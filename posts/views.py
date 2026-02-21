from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from .models import Post
from .forms import PostForm
from django.core.paginator import Paginator
from django.db.models import Q

def post_list(request):
    posts_list = Post.objects.all()
    search_query = request.GET.get('q', '')

    if search_query:
        posts_list = posts_list.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        )

    paginator = Paginator(posts_list, 5)
    page_number = request.GET.get('page', 1)
    posts = paginator.get_page(page_number)

    context = {
        'posts': posts,
        'search_query': search_query,
    }

    return render(request, 'posts/post_list.html', {'posts': posts})

def deleted_posts(request):
    posts = Post.all_objects.filter(is_deleted=True)
    return render(request, 'posts/deleted_posts.html', {'posts': posts})

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'posts/post_form.html', {
        'form': form,
        'title': 'Yangi post'
    })

def post_update(request, pk):
    post = get_object_or_404(Post.all_objects, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    return render(request, 'posts/post_form.html', {
        'form': form,
        'title': 'Postni tahrirlash'
    })

def post_delete(request, pk):
    post = get_object_or_404(Post.all_objects, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'posts/post_confirm_delete.html', {'post': post})


def post_restore(request, pk):
    post = get_object_or_404(Post.all_objects, pk=pk, is_deleted=True)
    if request.method == 'POST':
        post.restore()
        return redirect('deleted_posts')
    return render(request, 'posts/post_confirm_restore.html', {'post': post})

def post_hard_delete(request, pk):
    post = get_object_or_404(Post.all_objects, pk=pk)
    if request.method == 'POST':
        title = post.title
        post.hard_delete()
        return redirect('deleted_posts')
    return render(request, 'posts/post_confirm_hard_delete.html', {'post': post})

def post_detail(request, pk):
    post = get_object_or_404(Post.all_objects, pk=pk)
    return render(request, 'posts/post_detail.html', {'post': post})
