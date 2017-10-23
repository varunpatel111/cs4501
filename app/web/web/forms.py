from django import forms

from .models import Listing

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)