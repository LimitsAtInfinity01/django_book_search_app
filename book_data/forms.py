from django import forms
from .models import Reviews, Comments


class ReviewsForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['title', 'content', 'rating']

        widgets = {
            'rating': forms.NumberInput(attrs={'min': 0, 'max': 5})
        }

class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['content', 'author']


