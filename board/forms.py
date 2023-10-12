from django import forms
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

from .models import Post, Reply


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'title',
            'author',
            'category',
            'context',
            'file'
        ]

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("title")
        context = cleaned_data.get("context")

        if name == context:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data


class ReplyForm(forms.ModelForm):

    class Meta:
        model = Reply
        fields = [
            'author',
            'post',
            'context'
        ]

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get("context")

        if content is None:
            raise ValidationError(
                "Описание не должно быть пустым."
            )

        return cleaned_data