from articles.models import Post
from django import forms
from django.contrib.auth.forms import UserCreationForm

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'draft',
            'tags',
            'image',
        ]
    