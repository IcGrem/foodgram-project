from django import forms
from django.forms import ModelForm, Textarea

from .models import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': Textarea(attrs={'class': 'form__textarea', 'rows': '6'}),
        }
