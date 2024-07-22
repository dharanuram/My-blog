from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Like, Post, Comment
from .forms import CommentForm, PostForm, RegisterForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout

# Custom decorator to check if user is admin
def is_admin(user):
    return user.is_superuser

# Custom decorator to check if user is editor
def is_editor(user):
    return user.groups.filter(name='Editors').exists()  # Assuming 'Editors' is a group name for editors

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='login')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog-home')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})


def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    is_liked = post.likes.filter(user=request.user).exists()

    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    
    can_edit = request.user.is_superuser or request.user.groups.filter(name='Editors').exists()

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'is_liked': is_liked,
        'total_likes': post.likes.count(),
        'can_edit': can_edit,
    })

@login_required 
def like_post(request, pk):
    if request.method == 'POST' and request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            like.delete()
        return redirect('post-detail', pk=pk)
    else:
        # Handle case where user is not authenticated
        return redirect('login')
    
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post-detail', pk=pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'post_edit.html', {'form': form, 'post': post})

class CustomLoginView(LoginView):
    template_name = 'login.html'  # Specify your custom template

    def form_valid(self, form):
        next_url = self.request.GET.get('next')
        return redirect(next_url or 'blog-home')  

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('login1')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('blog-home')