from django.contrib import admin
from .models import Post, Vote#Upvote, Downvote
# Register your models here.
admin.site.register(Post)
admin.site.register(Vote)
# admin.site.register(Upvote)
# admin.site.register(Downvote)