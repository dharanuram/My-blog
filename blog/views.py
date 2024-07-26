from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import Like, Post, Comment
from .forms import CommentForm, CustomLoginForm, PostForm, RegisterForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import render, redirect


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

@login_required
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(reply_to=None)  # Fetch only top-level comments
    is_liked = post.likes.filter(user=request.user).exists()

    if request.method == 'POST' and request.user.is_authenticated:
        # Handle like/unlike logic
        if 'like' in request.POST:
            if is_liked:
                post.likes.filter(user=request.user).delete()
            else:
                Like.objects.create(user=request.user, post=post)
            return redirect('post-detail', pk=post.pk)
        
        total_likes = post.likes.count()
        
        if 'text' in request.POST:  # Handle new comment
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect('post-detail', pk=post.pk)
        elif 'reply_to_id' in request.POST:  # Handle reply to comment
            reply_to_id = request.POST.get('reply_to_id')
            parent_comment = get_object_or_404(Comment, pk=reply_to_id)
            form = CommentForm(request.POST)
            if form.is_valid():
                reply_comment = form.save(commit=False)
                reply_comment.post = post
                reply_comment.author = request.user
                reply_comment.reply_to = parent_comment  # Assign parent comment
                reply_comment.save()
                return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    
    can_edit = request.user.is_superuser or request.user.groups.filter(name='Editors').exists()

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'is_liked': is_liked,
        'total_likes': post.likes.count(),  # Use the variable instead of post.likes.count() again
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
    template_name = 'registration/login.html'  # Specify your custom template if needed
    form_class = CustomLoginForm

    def get_success_url(self):
        return reverse_lazy('blog-home')  

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')