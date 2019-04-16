from django import forms
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from users.models import SiteUser
from django.contrib.auth.models import User
from pagedown.widgets import PagedownWidget

class LogInForm(forms.Form):
    user_name = forms.CharField(max_length=40)
    password = forms.CharField(widget=forms.PasswordInput())

    

class SignUpForm(forms.ModelForm):
    class Meta:
        model = SiteUser

        fields = [
            'First_name',
            'Last_name',
            'Email_address',
            'profile_pic',
            'bio',
            'facebook',
            'github',
            'linkedin',
            'twitter',
            'address',
        ]
    

class BasicForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password_again = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = [
            'username',
            # 'password1',
            'password',
            'password_again',
        ]

    def clean(self):
        clearform = super().clean()
        password1 = clearform['password']
        password2 = clearform['password_again']
        if password1 != password2:
            raise forms.ValidationError('Password Mismatched')
        if len(password1)<8:
            raise forms.ValidationError('Your Password is too short')
        return clearform
