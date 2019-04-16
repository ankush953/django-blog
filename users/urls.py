<<<<<<< HEAD

from users.views import searchbyauthor, login_view, logout_view, signup_view, myprofile, update
from users.views import (
    searchbyauthor, login_view, logout_view,
    signup_view, myprofile, update, activate_account)

from users.views import (
    searchbyauthor, login_view, logout_view,
    signup_view, myprofile, update, activate_account)
from django.conf import urls
from django.urls import path, include
=======
from users.views import (
    searchbyauthor, login_view, logout_view,
     signup_view, myprofile, update, activate_account )
from django.conf import urls
from django.urls import path,include
>>>>>>> ed51eae750468f8c89cfa2bdc67f79c95e6d5d36
from django.conf import settings
from django.conf.urls.static import static


app_name = 'users'

urlpatterns = [

<<<<<<< HEAD
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('<str:author>/', searchbyauthor, name='searchbyauthor'),
    path('<str:req_user>/update/', update, name='update'),
    path('activate-account/<user>/<profile>/',
         activate_account, name='activate_account'),
    path('activate-account/<user>/<profile>/',
         activate_account, name='activate_account'),

=======
    path('login/',login_view,name='login'),
    path('signup/',signup_view,name='signup'),
    path('logout/',logout_view,name='logout'),
    path('<str:author>/',searchbyauthor,name='searchbyauthor'),
    path('<str:req_user>/update/',update,name='update'),
    path('activate-account/<user>/<profile>/',activate_account,name='activate_account'),
    
>>>>>>> ed51eae750468f8c89cfa2bdc67f79c95e6d5d36
]


if settings.DEBUG:
<<<<<<< HEAD
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
=======
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> ed51eae750468f8c89cfa2bdc67f79c95e6d5d36
