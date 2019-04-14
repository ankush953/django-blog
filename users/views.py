from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
from articles.models import Post
from django.contrib import messages
from users import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from users.models import SiteUser
from django.contrib.auth.models import User
from PIL import Image


def searchbyauthor(request, author):
    posts = Post.objects.filter(user__username=author).order_by('-updated_at')
    user = User.objects.filter(username=author).first()
    context = {
        'posts': posts,
        'author': user,
        'title': 'By Author',
    }
    return render(request, 'byauthor.html', context)


def login_view(request):
    form = AuthenticationForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            messages.success(request, 'You are Logged In')
            login(request, user)

            if not user:
                messages.error(request, 'Please Check Your Credentials')
                form = AuthenticationForm(request.POST or None)
            else:
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))

                return redirect('articles:homepage')
        else:

            messages.error(request, 'Please Check Your Credentials')
            form = AuthenticationForm(request.POST or None)
    context = {
        'form': form,
        'title': 'Log In',
    }
    return render(request, 'login.html', context)
   


def logout_view(request):
    logout(request)
    messages.success(request, 'You are Successfully logged out.')
    return redirect('articles:homepage')

def activate_account(request,user,profile):
    return redirect('password-reset')

def savemyprofile(request,user,profile):
    user.save()
    profile.save()

def signup_view(request, instance=None):
    Profileform = forms.SignUpForm(
        request.POST or None, request.FILES or None, instance=instance)
    Basicform = forms.BasicForm(
        request.POST or None, request.FILES or None, instance=instance)
    if request.method == 'POST':
        if Profileform.is_valid() and Basicform.is_valid():
            user = Basicform.save(commit=False)
            profile = Profileform.save(commit=False)
            user.first_name = profile.First_name
            user.last_name = profile.Last_name
            user.email = profile.Email_address
            user.set_password(user.password)
            user.save()
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            else:
                profile.profile_pic = 'profile_pic/default-user.jpg'

            profile.save()

            messages.success(request, 'Account has been created.')
            return redirect('articles:homepage')
            # messages.success(request, 'Account has been created.')
            return redirect('users:searchbyauthor',author=user.username)
            # return redirect('users:activate_account',user=user,profile=profile)
            # messages.success(request, 'Account has been created.')
            return redirect('users:searchbyauthor',author=user.username)
            # return redirect('users:activate_account',user=user,profile=profile)
        else:
            messages.error(request, 'Failed to Create User')
            Profileform = forms.SignUpForm(
                request.POST or None, request.FILES or None, instance=instance)
            Basicform = forms.BasicForm(
                request.POST or None, request.FILES or None, instance=instance)
    else:

        messages.error(request, 'Failed to Create User')
        Profileform = forms.SignUpForm(
            request.POST or None, request.FILES or None, instance=instance)
        Basicform = forms.BasicForm(
            request.POST or None, request.FILES or None, instance=instance)

    context = {
        'profileform': Profileform,
        'basicform': Basicform,
        'title': 'Sign Up',
    }
    return render(request, 'signup.html', context)


@login_required(login_url='users:login')
def myprofile(request):
    return searchbyauthor(request, request.user.username)


@login_required(login_url='users:login')
def update(request, req_user=None):
    user = request.user
    if user.username != req_user:
        return redirect('users:searchbyauthor',author=user.username)
    profile = SiteUser.objects.filter(user=user).first()
    Profileform = forms.SignUpForm(
        request.POST or None, request.FILES or None, instance=profile)
    Basicform = forms.BasicForm(
        request.POST or None, request.FILES or None, instance=user)
    if request.method == 'POST':
        if Profileform.is_valid() and Basicform.is_valid():
            user = Basicform.save(commit=False)
            profile = Profileform.save(commit=False)
            user.first_name = profile.First_name
            user.last_name = profile.Last_name
            user.email = profile.Email_address
            user.set_password(user.password)
            user.save()

            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            else:
                profile.profile_pic = 'profile_pic/default-user.jpg'

            profile.save()

            messages.success(request, 'Account has been updated.')
            return redirect('users:searchbyauthor',author=request.user)
        else:
            messages.error(request, 'Failed to Update Details')
            Profileform = forms.SignUpForm(
                request.POST or None, request.FILES or None, instance=profile)
            Basicform = forms.BasicForm(
                request.POST or None, request.FILES or None, instance=user)
    else:

        messages.error(request, 'Failed to Update Details')
        Profileform = forms.SignUpForm(
            request.POST or None, request.FILES or None, instance=profile)
        Basicform = forms.BasicForm(
            request.POST or None, request.FILES or None, instance=user)

    context = {
        'profileform': Profileform,
        'basicform': Basicform,
        'title': 'Update',
    }
    return render(request, 'update.html', context)


def searchbyanything(request, string=None):
    user = User.objects.filter(username=string).first()
    posts_content = Post.objects.filter(content_icontains=string)
    posts_title = Post.objects.filter(title_contains=string)
    context = {
        'user': user,
        'content_posts': posts_content,
        'title_posts': posts_title,
    }
    return render(request, 'search.html', context)

def about(request):
    Me = User.objects.filter(username='ankush').first()
    return render(request,'about.html',{'author': Me})
    