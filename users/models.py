from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.


def imagepath(request, filename):
    return 'profile_pic/'+request.user.username+'/'+filename


class SiteUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=50, blank=True)
    facebook = models.CharField(max_length=60, blank=True)
    linkedin = models.CharField(max_length=60, blank=True)
    github = models.CharField(max_length=60, blank=True)
    twitter = models.CharField(max_length=60, blank=True)
    bio = models.TextField(max_length=200, blank=True)

    profile_pic = models.ImageField(
        upload_to=imagepath, blank=True, default='profile_pic/default-user.jpg')
    First_name = models.CharField(max_length=20)
    # middlename = models.CharField(max_length=20,null=True,blank=True)
    Last_name = models.CharField(max_length=20)
    Email_address = models.EmailField(unique=True)
    # UserNameForQuery = models.CharField(max_length=40,blank=True)

    def __str__(self):
        full_name = self.user.username
        return full_name

    def get_full_name(self):
        return self.First_name+self.Last_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profile_pic.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)
