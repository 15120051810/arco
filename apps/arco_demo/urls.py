from rest_framework import routers
from django.urls import path

from .user_views import UserLogin, UserInfo, UserOutLogin, UserMenu
from .workplace_view import ContentDataView
from .dj_table_view import DJTableBaseUse

app_name = 'arco_demo'

urlpatterns = [
    path('user/login', UserLogin.as_view()),
    path('user/info', UserInfo.as_view()),
    path('user/logout', UserOutLogin.as_view()),
    path('user/menu', UserMenu.as_view()),
    path('dashboard/content-data', ContentDataView.as_view()),
    path('dj_tables/base_use', DJTableBaseUse.as_view()),
]

