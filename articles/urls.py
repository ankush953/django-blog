from django.conf import urls
from django.urls import path,include
from articles.views import homepage, create,readmore, searchbytag, upvote, downvote
from articles.views import update_article, ask_delete_article, confirm_delete_article
from django.conf import settings
from django.conf.urls.static import static


app_name = 'articles'

urlpatterns = [
    path('',homepage,name='homepage'),
    path('article/create/',create,name='create'),
    path('article/<str:slug>/',readmore,name='readmore'),
    path('article/<str:slug>/upvote/',upvote,name='upvote'),
    path('article/<str:slug>/downvote/',downvote,name='downvote'),
    path('article/tags/<str:tag>/',searchbytag,name='tagged'),
    path('article/<int:pk>/update/',update_article,name='update-article'),
    path('article/<int:pk>/delete/',ask_delete_article,name='delete-article'),
    path('article/<int:pk>/delete/confirm',confirm_delete_article,name='deleted-article'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)