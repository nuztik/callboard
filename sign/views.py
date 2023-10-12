import random
from string import hexdigits

from allauth.conftest import user
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from django.contrib.auth.models import User, Group
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm, OneTimeCode



class BaseRegisterView(CreateView):
    model = User
    # template_name = 'sign/signup.html'
    form_class = BaseRegisterForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BaseRegisterForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
        return redirect('code', request.POST['username'])

class CodeRandomView(CreateView):
    template_name = 'sign/coder.html'

    def get_context_data(self, **kwargs):
        user_ = self.kwargs.get('user')
        if not OneTimeCode.objects.filter(user=user_).exists():
            code = ''.join(random.sample(hexdigits, 5))
            OneTimeCode.objects.create(user=user_, code=code)
            user = User.objects.get(username=user_)
            send_mail(
                subject='Код активации',
                message=f'Код активации аккаунта: {code}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )


    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            user = request.path.split('/')[-1]
            if OneTimeCode.objects.filter(code=request.POST['code'], user=user).exists():
                User.objects.filter(username=user).update(is_active=True)
                OneTimeCode.objects.filter(code=request.POST['code'], user=user).delete()
            else:
                return render(self.request, 'sign/in_code.html')
        return redirect ('login')