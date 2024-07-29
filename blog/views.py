from django.forms import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import Like, Post, Comment
from .forms import CommentForm, CustomLoginForm, PostForm, RegisterForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserChangeForm
from django.contrib import messages
from django import forms

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
    # Fetch the post and top-level comments
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(parent__isnull=True)  # Fetch only top-level comments
    is_liked = post.likes.filter(user=request.user).exists()
    total_likes = post.likes.count()
    
    # Handle POST requests
    if request.method == 'POST':
        if request.user.is_authenticated:
            # Handle like/unlike logic
            if 'like' in request.POST:
                if is_liked:
                    post.likes.filter(user=request.user).delete()
                else:
                    Like.objects.create(user=request.user, post=post)
                return redirect('post-detail', pk=post.pk)
            
            # Handle comment or reply
            if 'text' in request.POST:
                form = CommentForm(request.POST)
                if form.is_valid():
                    comment = form.save(commit=False)
                    comment.post = post
                    comment.author = request.user
                
                # Handle reply or new comment
                    reply_to_id = request.POST.get('reply_to_id')
                    if reply_to_id:
                    # If replying to an existing comment
                        parent_comment = get_object_or_404(Comment, pk=reply_to_id)
                        comment.parent = parent_comment
                    else:
                    # If it's a new comment (not a reply)
                        comment.parent = None
                
                comment.save()
                return redirect('post-detail', pk=post.pk)
    else:
        # Initialize the form for GET request
        form = CommentForm()
    
    # Check if the user has editing permissions
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

def CustomLoginView(request):
    if request.user.is_authenticated:
        # Redirect to home page if user is already logged in
        return redirect('blog-home')  # Adjust 'home' to the name of your home page view
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('blog-home')  # Redirect to home page after login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
 
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

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('edit-profile')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})

class EmailChangeForm(forms.Form):
    email = forms.EmailField(label='New Email Address')

@login_required
def edit_email(request):
    if request.method == 'POST':
        form = EmailChangeForm(request.POST)
        if form.is_valid():
            new_email = form.cleaned_data['email']
            try:
                user = request.user
                # Validate email uniqueness
                if User.objects.filter(email=new_email).exists():
                    raise ValidationError("This email is already in use.")
                # Update user email
                user.email = new_email
                user.save()
                messages.success(request, "Your email address has been updated.")
                return redirect('blog-home') 
            except ValidationError as e:
                form.add_error('email', str(e))
    else:
        form = EmailChangeForm()

    return render(request, 'edit_email.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password changed successfully.')
            return redirect('change-password')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})

@login_required
def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'profile.html', {'user': user})