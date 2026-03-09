from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post
from .forms import PostForm

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

    return render(request, 'posts/post_list.html', {
        'posts': posts,
        'search_query': search_query
    })

def deleted_posts(request):
    posts = Post.all_objects.filter(is_deleted=True)
    return render(request, 'posts/deleted_posts.html', {'posts': posts})

@login_required
@permission_required('posts.add_post', raise_exception=True)
def post_create(request):
    if request.method == 'POST':
        # 🟢 MUHIM: request.FILES ni qo'shish kerak!
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'posts/post_form.html', {
        'form': form,
        'title': 'Yangi post'
    })

@login_required
@permission_required('posts.change_post', raise_exception=True)
def post_update(request, pk):
    post = get_object_or_404(Post.all_objects, pk=pk)
    if request.method == 'POST':
        # 🟢 MUHIM: request.FILES ni qo'shish kerak!
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/post_form.html', {
        'form': form,
        'title': 'Postni tahrirlash'
    })

@login_required
@permission_required('posts.delete_post', raise_exception=True)
def post_delete(request, pk):
    post = get_object_or_404(Post.all_objects, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'posts/post_confirm_delete.html', {'post': post})

@login_required
def post_restore(request, pk):
    post = get_object_or_404(Post.all_objects, pk=pk, is_deleted=True)
    if request.method == 'POST':
        post.restore()
        return redirect('deleted_posts')
    return render(request, 'posts/post_confirm_restore.html', {'post': post})

@login_required
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