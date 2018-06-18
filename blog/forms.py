
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class PostForm(forms.ModelForm):
    status = forms.CharField(required=False)
    image = forms.FileField(required=False)
    class Meta:
        model = Post
        fields = ('title', 'body', 'status', 'image', 'category')

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class PostPassword(forms.ModelForm):
    class Meta:
        model=Post
        fields= 'status',
    # def clean_status(self):
    #     try:
    #         Post.objects.get(status=="aaa")
    #         raise forms.ValidationError("password taken.")
    #     except forms.ValidationError("The passwords don't match."):
    #         pass