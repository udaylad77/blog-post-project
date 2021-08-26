from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    """
    ModelForm for 'Post' with 'author', 'title', 'text' fields.
    """
    class Meta:
        model = Post
        fields = ('author', 'title', 'text',)

        # Set Form Widgets corresponding to CSS.
        # CSS Classes('editable', 'medium-editor-textarea').
        # ('textinputclass', 'postcontent') is our own class.
        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }


class CommentForm(forms.ModelForm):
    """
    ModelForm for 'Comment' with 'author', 'text' fields.
    """
    class Meta:
        model = Comment
        fields = ('author', 'text',)

        # Set Form Widgets corresponding to CSS.
        # CSS Classes('editable', 'medium-editor-textarea').
        # textinputclass' is our own class
        widgets = {
            'author': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        }