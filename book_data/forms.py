from django import forms
from .models import Reviews, Comments, Biography


class ReviewsForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['content', 'rating']

        widgets = {
            'rating': forms.NumberInput(attrs={'min': 0, 'max': 5})
        }

class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['content', 'author']

class BiographyForm(forms.ModelForm):
    class Meta:
        model = Biography
        fields = ['text']  # Don't include 'user' if you plan to set it in the view
