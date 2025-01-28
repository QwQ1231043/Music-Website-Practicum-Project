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
    path('delete_friend/<int:friend_id>/', views.delete_friend, name='delete_friend'),
    path('edit_profile',views.edit_profile,name="edit_profile"),
    path('delete_video_from_folder/<int:folder_id>/<int:video_id>/', views.delete_video_from_folder,
         name='delete_video_from_folder'),
    path('friend/<int:friend_id>/', views.friend_page, name='friend_page'),
    path('video_page/<int:video_id>/',views.view_specific_video,name='view_specific_video'),
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)