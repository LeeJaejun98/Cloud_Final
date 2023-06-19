from django import forms

from .models import Comment


class CommentForm(forms.ModelForm): ##views 에서 postCreate와 비교
    class Meta:
        model = Comment
        fields = ['content', ]
