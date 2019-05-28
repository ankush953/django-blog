from django.db import models

# Create your models here.
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User
from articles.models import Post

class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    # needs to be removed to use generic keys
    # post = models.ForeignKey(Post,on_delete=models.CASCADE)

    # Essential code you have to write to use generic keys
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username