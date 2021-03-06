import urllib.parse

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView

from .models import Post, Vote  # , Upvote, Downvote
from comments.models import Comment

from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType


from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from articles import forms
from django.forms import modelformset_factory

from django.contrib.auth import login, logout
from django.contrib import messages

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models.signals import post_save
from notifications.signals import notify
from articles.models import Post

import re

from django.contrib.auth.models import User

# Importing Q to make queries
from django.db.models import Q

# To handle 404 in production
def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def homepage(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(user__username__startswith=query) |
            Q(content__icontains=query) |
            Q(tags__name__in=[query])
        ).distinct().order_by('-updated_at')
    else:
        posts = Post.objects.filter(draft=False).order_by('-updated_at')
    paginator = Paginator(posts, 10)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts,
    }
    return render(request, 'show_menu.html', context=context)


def find(text, curr):
    user_name = ''
    while curr < len(text) and text[curr] != ' ' and text[curr] != '?' and text[curr] != '-':
        user_name += text[curr]
        curr += 1
    user = User.objects.filter(username=user_name).first()
    return user


# ------------------------------------------------
# django-notifications-hq

def my_handler(sender, instance, created, **kwargs):
    post = Post.objects.filter(slug=instance.slug).first()
    mentioned_users = []
    string = post.content
    for i in range(len(string)):
        if string[i] == '@':
            user = find(string, i+1)
            if user:
                mentioned_users.append(user)
    # print(mentioned_users)
    # print(post.content.split('@'))
    # print(mentioned_users.group(1))
    # qs = User.objects.filter(username='ankush')
    string = '<a href=\'{% url \'articles:readmore\' post.slug %}\'>' + \
        instance.title + '</a>'
    # print(string)
    notify.send(sender=instance.user, recipient=mentioned_users,
                verb=" mentioned you in {}".format(instance.title))


post_save.connect(my_handler, sender=Post)
# --------------------------------------------------


@login_required(login_url='users:login')
def create(request, obj=None):
    post_form = forms.PostForm(
        request.POST or None, request.FILES or None, instance=obj)
    if request.user.is_authenticated:
        if request.method == 'POST':
            post_form = forms.PostForm(
                request.POST or None, request.FILES or None, instance=obj)
            if post_form.is_valid():
                instance = post_form.save(commit=False)
                instance.user = request.user

                instance.save()

                post_form.save_m2m()
                messages.success(request, 'Your Post is saved')
                # notifyusers(instance.content)
                return redirect('articles:readmore', slug=instance.slug)
                # notifyusers(instance.content)
                return redirect('articles:readmore', slug=instance.slug)
            else:
                messages.error(request, 'Error Occured during saving post')
                post_form = forms.PostForm(
                    request.POST or None, request.FILES or None, instance=obj)
    else:
        messages.error(request, 'You are not authenticated')
        post_form = forms.PostForm(
            request.POST or None, request.FILES or None, instance=obj)
    content = {
        'form': post_form,
    }
    return render(request, 'createpost.html', context=content)


def readmore(request, slug):
    post = Post.objects.filter(slug=slug, draft=False).first()
    share_quote = urllib.parse.quote_plus(post.content)

    content_type = ContentType.objects.get_for_model(Post)
    object_id = post.id
    # # print(object_id)
    comments = Comment.objects.filter(
        content_type=content_type, object_id=object_id)
    # # print(comments)
    content = {
        'post': post,
        'post_tags': list(post.tags.names()),
        'share_string': share_quote,
        'comments': comments,
    }
    return render(request, 'full_blog.html', content)


@login_required(login_url='users:login')
def upvote(request, slug):
    already_did = 'You cannot vote twice.'
    post = Post.objects.filter(slug=slug, draft=False).first()
    user_did = Vote.objects.filter(user=request.user, post=post).first()
    if user_did == None:
        post.votes += 1
        Vote.objects.create(user=request.user, post=post)
        post.save()
        already_did = 'You vote is registered.'
    content = {
        'post': post,
        'post_tags': list(post.tags.names()),
        'message': already_did,
    }
    return render(request, 'full_blog.html', context=content)


@login_required(login_url='users:login')
def downvote(request, slug):
    already_did = 'You cannot vote twice.'
    post = Post.objects.filter(slug=slug, draft=False).first()
    user_did = Vote.objects.filter(user=request.user, post=post).first()
    if user_did == None:
        post.votes -= 1
        Vote.objects.create(user=request.user, post=post)
        post.save()
        already_did = 'You vote is registered.'
    content = {
        'post': post,
        'post_tags': list(post.tags.names()),
        'message': already_did,
    }
    return render(request, 'full_blog.html', context=content)


def searchbytag(request, tag=None):
    posts_with_same_tag = Post.objects.filter(
        tags__name__in=[tag], draft=False).order_by('-id')
    content = {
        'posts': posts_with_same_tag,
        'tagged_as': tag,
    }
    return render(request, 'sametagged.html', context=content)


def update_article(request, pk):
    post = Post.objects.filter(pk=pk, draft=False).first()
    if request.user != post.user:
        return redirect('articles:homepage')
    return create(request, obj=post)


@login_required(login_url='users:login')
def ask_delete_article(request, pk):
    post = Post.objects.filter(pk=pk, draft=False).first()
    if request.user != post.user:
        return redirect('articles:homepage')
    content = {
        'post': post,
    }
    return render(request, 'ask_delete_article.html', context=content)


@login_required(login_url='users:login')
def confirm_delete_article(request, pk):
    post = Post.objects.filter(pk=pk, draft=False).first()
    if request.user != post.user:
        return redirect('articles:homepage')
    post.delete()
    return redirect('articles:homepage')
