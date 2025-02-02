from django import forms
from .models import Reviews, Comments


class ReviewsForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['title', 'content', 'rating']

class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['content']
