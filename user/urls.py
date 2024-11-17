from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

from user import views

app_name='user'
urlpatterns=[

    path("profile",views.profile,name="profile"),
    path("flavorite", views.user_flavorite, name="flavorite"),
    path("likes", views.user_likes, name="likes"),
    path("management", views.user_management, name="management"),
    path("friends", views.user_friends, name="friends"),

]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)