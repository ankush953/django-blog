from django import forms
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from users.models import SiteUser
from django.contrib.auth.models import User


class LogInForm(forms.Form):
    user_name = forms.CharField(max_length=40)
    password = forms.CharField(widget=forms.PasswordInput())

<<<<<<< HEAD
    # def get_choice(self):
    #     return self.select
=======
  
>>>>>>> ed51eae750468f8c89cfa2bdc67f79c95e6d5d36

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
<<<<<<< HEAD
    # first_name = forms.CharField(max_length=15,min_length=1)
    # middle_name = forms.CharField(max_length=15,min_length=0)
    # last_name = forms.CharField(max_length=15,min_length=1)
    # email = forms.EmailField(help_text='Enter Your Email Here')
    # image = forms.ImageField()
    # password = forms.CharField(widget=forms.PasswordInput())
    # conf_password = forms.CharField(widget=forms.PasswordInput())
    # class Meta:
    #     model = SiteUser
    #     fields = ['first_name','middle_name','last_name','email_id','profile_pic','address']
=======
 
>>>>>>> ed51eae750468f8c89cfa2bdc67f79c95e6d5d36

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
