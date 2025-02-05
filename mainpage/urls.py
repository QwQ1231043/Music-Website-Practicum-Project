from django.urls import path,include
from mainpage import views
# Create your tests here.

app_name = 'mainpage'
urlpatterns=[
    path('mainpage', views.mainpage_template2, name='mainpage'),
    path('sign_in',views.sign_in,name='sign_in'),
    path('sign_up',views.sign_up,name='sign_up'),
    path('sign_out',views.sign_out,name='sign_out'),
    path('Management',views.Management,name='Management'),
    path('user_mainpage',views.user_mainpage,name='user_mainpage'),
    path('check_verification',views.check_verification,name='check_verification'),
    path('mainpage_template',views.mainpage_template3,name='mainpage_template'),
]