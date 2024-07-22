from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def _str_(self):
        return self.title
    
    class Meta:
        permissions = [
            ("can_edit_posts", "Can edit posts"),
        ]

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def _str_(self):
        return f'Comment by {self.author} on {self.post}'
    
class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def _str_(self):
        return f'Like by {self.user} on {self.post}'