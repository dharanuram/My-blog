from django import forms
from .models import Post
from .models import Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
    
    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'form-control', 'rows': 3})
        self.fields['reply_to_id'] = forms.IntegerField(widget=forms.HiddenInput, required=False)

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