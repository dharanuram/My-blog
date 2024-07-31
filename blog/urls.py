from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('home/', views.home, name='blog-home'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('post/<int:pk>/edit/', views.post_edit, name='post-edit'),
    path('post/<int:pk>/like/', views.like_post, name='like-post'),
    path('post/create/', views.create_post, name='create-post'),
    path('register/', views.register, name='register'),
    path('', views.CustomLoginView, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login1'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('edit-email/', views.edit_email, name='edit-email'),
    path('change-password/', views.change_password, name='change-password'),
    path('comments/<pk>/delete/', views.delete_comment, name='delete_comment'),
    path('hashtag/', views.hashtag_search, name='hashtag_search'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('comment/<int:comment_id>/delreply/', views.delete_reply, name='delete_reply'),
]