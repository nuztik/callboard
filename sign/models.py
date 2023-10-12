from django.db import models

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    username = forms.CharField(label="Имя")
    nickname = forms.CharField(label="Nickname")

    class Meta:
        model = User
        fields = ("username",
                  "nickname",
                  "email",
                  "password1",
                  "password2",)


class CommonSignupForm(SignupForm):

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class OneTimeCode(models.Model):
    objects = None
    code = models.CharField(max_length=10)
    user = models.CharField(max_length=255)

