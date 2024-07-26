from django.contrib import admin
from .models import Post, Comment
from django.contrib.auth.models import Group

class PostAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Only allow superuser to add posts
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        # Allow users in the 'Editor' group to edit posts
        if request.user.is_superuser:
            return True
        if request.user.groups.filter(name='Editor').exists():
            return True
        return False

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    list_filter = ('created_at', 'post')
    search_fields = ('content', 'author__username')  # Assuming author is a User model

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)