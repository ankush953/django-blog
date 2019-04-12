from django.db import models

from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.conf import settings
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

from PIL import Image
from django.urls import reverse


def imagepath(request, filename):
    return request.slug+'/'+filename

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=40)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    votes = models.IntegerField(verbose_name='Vote', default=0)
    tags = TaggableManager(blank=True)
    image = models.ImageField(upload_to=imagepath, blank=True)
    TAGGIT_CASE_INSENSITIVE = True

    def __str__(self):
        return self.title

    def snippet(self):
        words = self.content.split()
        return (' ').join(words[:40])

    def get_absolute_url(self):
        return reverse('articles:readmore', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            if img.height > 400 or img.width > 400:
                output_size = (400, 400)
                img.thumbnail(output_size)
                img.save(self.image.path)


def get_slug(instance, new_slug=None):
    slug = slugify(instance)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug)
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return get_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_saver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = get_slug(instance)


pre_save.connect(pre_save_post_saver, sender=Post)
