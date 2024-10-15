from django import forms
from . import models


"""
Form for creating a new post.
"""
class CreatePostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['image', 'description', 'text']


"""
Foma for getting multiple categories for a post.
"""
class CategoryForm(forms.Form):
    categories = forms.ModelMultipleChoiceField(
        queryset=models.Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

"""
Form for writing a comment.
"""
class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['text']


"""
The form to send a like.
"""
class LikeForm(forms.ModelForm):
    class Meta:
        model = models.Like
        fields = []
