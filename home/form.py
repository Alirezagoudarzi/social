
from django import forms
from django.forms import ModelForm

from .models import Post,CommentModel

class PostUpdateForm(ModelForm):
    class Meta:
        model=Post
        fields=('title','body')


class PostCreateForm(ModelForm):
    class Meta:
        model=Post
        fields=('title','body')


class CommentCreateForm(ModelForm):
    class Meta:
        
        model=CommentModel
        fields=('body',)
        
        labels = {
        'body': 'Comment'
        }

        widgets= {
            'body':forms.Textarea(attrs={'class':'form-control'})
        }
