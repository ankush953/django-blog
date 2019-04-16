from articles.models import Post
from django import forms
from django.contrib.auth.forms import UserCreationForm
from pagedown.widgets import PagedownWidget

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget())
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'draft',
            'tags',
            # 'image',
        ]
    