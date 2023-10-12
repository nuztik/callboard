from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.template import response
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .filters import PostFilter
from .forms import ReplyForm, PostForm
from .models import Post, Reply



class PostList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'board/board.html'
    context_object_name = 'board'
    paginate_by = 10

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     self.filterset = PostFilter(self.request.GET, queryset)
    #     return self.filterset
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['filterset'] = self.filterset
    #     return context


class PostDetail(DetailView):
    model = Post
    template_name = 'board/post.html'
    context_object_name = 'post'


class PostSearch(ListView):
    model = Post
    ordering = 'title'
    template_name = 'board/search.html'
    context_object_name = 'search'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'board/up_create.html'
    context_object_name = 'p_create'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_author = self.request.user
        post.save()
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = '__all__'
    template_name = 'board/up_create.html'
    context_object_name = 'p_update'


class AccountDetail(LoginRequiredMixin, ListView):
    model = Post
    fields = '__all__'
    template_name = 'board/account.html'
    context_object_name = 'account'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts_to_author = Post.objects.filter(author=self.request.user)
        context['posts_to_author'] = posts_to_author
        return context


class ReplyList(ListView):
    model = Reply
    form_class = ReplyForm
    template_name = 'reply/replies.html'
    context_object_name = 'replies'


class ReplyCreate(LoginRequiredMixin, CreateView):
    model = Reply
    form_class = ReplyForm
    template_name = 'reply/up_create.html'
    context_object_name = 'r_create'

    def form_valid(self, form):
        reply = form.save(commit=False)
        reply.reply_author = self.request.user
        reply.save()
        return super().form_valid(form)


class ReplyUpdate(LoginRequiredMixin, UpdateView):
    model = Reply
    fields = '__all__'
    template_name = 'reply/up_create.html'
    context_object_name = 'r_update'


def delete_reply(self, pk):
    reply = Reply.objects.get(id=pk)
    reply.delete()
    return redirect('board/')


@login_required()
def accept_reply(request, pk):
    reply = Reply.objects.get(id=pk)
    reply.accept = True
    reply.save()
    send_mail(
        subject=f'Отлик принят.',
        message=f'Ваш отклик на пост "{response.post.title}" принят',
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[response.user.email]
    )
    return HttpResponseRedirect(reverse('response_list'))


def delete_post(self, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return redirect('board/')