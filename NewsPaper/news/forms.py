from django_filters import DateFilter
from django import forms
from .models import Post, Author
from django.core.exceptions import ValidationError
from datetime import datetime


class PostForm(forms.ModelForm):
    title = forms.CharField(min_length=2)
    author = Author.objects.all().values('user__username')

    class Meta:
        model = Post
        fields = ['title', 'author', 'text_post', 'category']

    def clean(self):
        cleaned_data = super().clean()
        heading = cleaned_data.get("title")
        text = cleaned_data.get("text_post")
        if heading == text:
            raise ValidationError("Описание не должно быть идентично названию.")
        return cleaned_data
