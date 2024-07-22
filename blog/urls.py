from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('post/<int:pk>/edit/', views.post_edit, name='post-edit'),
    path('post/<int:pk>/like/', views.like_post, name='like-post'),
    path('post/create/', views.create_post, name='create-post'),
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login1'),
]