from django import forms
from .models import Reviews, Comments, Profile, TextPosts, VideoPosts, ImagePosts


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


class AvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']

class BioForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']


class ImagePostForm(forms.ModelForm):
    class Meta:
        model = ImagePosts
        fields = ['image', 'description']

class VideoPostForm(forms.ModelForm):
    class Meta:
        model = VideoPosts
        fields = ['video', 'description']

class TextPostForm(forms.ModelForm):
    class Meta:
        model = TextPosts
        fields = ['text']