from django import forms
from .models import Post
from .models import Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CommentForm(forms.ModelForm):
    reply_to_id = forms.IntegerField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Comment
        fields = ['text']
    
    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)

    def save(self, commit=True):
        comment = super().save(commit=False)
        if self.post:
            comment.post = self.post
    
        reply_to_id = self.cleaned_data.get('reply_to_id')
        if reply_to_id:
            comment.parent = Comment.objects.get(id=reply_to_id)
    
        if commit:
            comment.save()
        return comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CustomLoginForm(AuthenticationForm):
   
    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)