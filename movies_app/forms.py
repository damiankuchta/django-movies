from django import forms
from .models import Comments, Reviews


class AddComment(forms.ModelForm):
    comment_content = forms.CharField(widget=forms.TextInput(attrs={'class': 'special', 'size': '100'}))

    class Meta:
        model = Comments
        fields = ['comment_content']


class AddReview(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['review_content']
