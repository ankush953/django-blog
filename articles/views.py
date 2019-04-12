from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import Post
from django.contrib.auth.decorators import login_required


from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from articles import forms
from django.forms import modelformset_factory

from django.contrib.auth import login, logout
from django.contrib import messages

from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger

def homepage(request):
    posts = Post.objects.filter(draft=False).order_by('-updated_at')
    paginator = Paginator(posts,10)

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

def notifyusers(text):
    pass

@login_required(login_url='users:login')
def create(request, instance=None):
    post_form = forms.PostForm(request.POST or None, request.FILES or None, instance=instance)
    if request.user.is_authenticated:
        if request.method == 'POST':
            post_form = forms.PostForm(request.POST or None,request.FILES or None,instance=instance)
            if post_form.is_valid():
                instance = post_form.save(commit=False)
                instance.user = request.user
                # instance.author = request.user


                instance.save()
                for tag in instance.tags.names():
                    instance.post_tags.append(tag)
                instance.save()
                post_form.save_m2m()
                messages.success(request, 'Your Post is saved')
                notifyusers(instance.content)
                return redirect('articles:readmore',slug=instance.slug)
            else:
                messages.error(request, 'Error Occured during saving post')
                post_form = forms.PostForm(
                    request.POST or None,request.FILES or None, instance=instance)
    else:
        messages.error(request, 'You are not authenticated')
        post_form = forms.PostForm(request.POST or None,request.FILES or None, instance=instance)
    content = {
        'form': post_form,
       }
    return render(request, 'createpost.html', context=content)


def readmore(request, slug):
    post = Post.objects.filter(slug=slug, draft=False).first()
    content = {
        'post': post,
        'post_tags': list(post.tags.names()),
    }
    return render(request, 'full_blog.html', content)


@login_required(login_url='users:login')
def upvote(request, slug):
    post = Post.objects.filter(slug=slug, draft=False).first()
    post.votes += 1
    post.save()
    content = {
        'post': post,
        'post_tags': list(post.tags.names()),
    }
    return render(request, 'full_blog.html', context=content)


@login_required(login_url='users:login')
def downvote(request, slug):
    post = Post.objects.filter(slug=slug, draft=False).first()
    post.votes -= 1
    post.save()
    content = {
        'post': post,
        'post_tags': list(post.tags.names()),
    }
    return render(request, 'full_blog.html', context=content)


def searchbytag(request, tag=None):
    posts_with_same_tag = Post.objects.filter(
        tags__name__in=[tag],draft=False).order_by('-id')
    content = {
        'posts': posts_with_same_tag,
        'tagged_as': tag,
    }
    return render(request, 'sametagged.html', context=content)

def update_article(request, pk):
    post = Post.objects.filter(pk=pk,draft=False).first()
    if request.user != post.user:
        return redirect('articles:homepage')
    return create(request,post)

@login_required(login_url='users:login')
def ask_delete_article(request,pk):
    post = Post.objects.filter(pk=pk,draft=False).first()
    if request.user != post.user:
        return redirect('articles:homepage')
    content = {
        'post':post,
    }
    return render(request,'ask_delete_article.html',context=content)

@login_required(login_url='users:login')
def confirm_delete_article(request,pk):
    post = Post.objects.filter(pk=pk,draft=False).first()
    if request.user != post.user:
        return redirect('articles:homepage')
    post.delete()
    return redirect('articles:homepage')