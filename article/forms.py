from django import forms
from .models import Comment, Post
from django.utils.translation import gettext_lazy as _


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, label=_('Name'))
    email = forms.EmailField(label=_('Email'))
    to = forms.EmailField(label=_('To'))
    comments = forms.CharField(required=False, widget=forms.Textarea, label=_('Comments'))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class': 'w3-input w3-border'}),
        }


class SearchForm(forms.Form):
    query = forms.CharField()
    widgets = {
        'query': forms.TextInput(attrs={'class': 'w3-input w3-border'}),
    }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'avatar', 'price', 'body', 'tags')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w3-input w3-border'}),
            'price': forms.TextInput(attrs={'class': 'w3-input w3-border'}),
            'body': forms.Textarea(attrs={'class': 'w3-input w3-border'}),
            'tags': forms.TextInput(attrs={'class': 'w3-input w3-border'}),
        }


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'avatar', 'price', 'body')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w3-input w3-border'}),
            'price': forms.TextInput(attrs={'class': 'w3-input w3-border'}),
            'body': forms.Textarea(attrs={'class': 'w3-input w3-border'}),
        }
