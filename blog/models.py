from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Permission

class Post(models.Model):
    DRAFT = 'draft'
    ON_HOLD = 'on_hold'
    PUBLISHED = 'published'

    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (ON_HOLD, 'On Hold'),
        (PUBLISHED, 'Published'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=DRAFT)
    image = models.ImageField(upload_to='blog_images', blank=True, null=True)

    def _str_(self):
        return self.title

    class Meta:
        permissions = [
            ("can_edit_posts", "Can edit posts"),
            ("can_publish_posts", "Can publish posts"),
            ("can_put_on_hold", "Can put posts on hold"),
        ]

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    reply_to = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='replies')

    def _str_(self):
        return f'Comment by {self.author} on {self.post}'
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)

    def _str_(self):
        return f'{self.user.username} likes {self.post.title}'