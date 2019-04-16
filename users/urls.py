
from users.views import searchbyauthor, login_view, logout_view, signup_view, myprofile, update
from users.views import (
    searchbyauthor, login_view, logout_view,
    signup_view, myprofile, update, activate_account)

from users.views import (
    searchbyauthor, login_view, logout_view,
    signup_view, myprofile, update, activate_account)
from django.conf import urls
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


app_name = 'users'

urlpatterns = [

    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('<str:author>/', searchbyauthor, name='searchbyauthor'),
    path('<str:req_user>/update/', update, name='update'),
    path('activate-account/<user>/<profile>/',
         activate_account, name='activate_account'),
    path('activate-account/<user>/<profile>/',
         activate_account, name='activate_account'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
