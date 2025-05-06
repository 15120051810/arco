"""
@Author   : liuxiangyu
@File     : urls.py
@TIme     : 2023/1/12 13:53
@Software : PyCharm
"""
from django.urls import path
from django.conf import settings
from rest_framework.routers import SimpleRouter
from rest_framework_extensions.routers import (ExtendedDefaultRouter as DefaultRouter)


from .views import UserLoginView, UserInfoView, UserLoginOutView, UserMenuView

app_name = "users"

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

urlpatterns = [
    path('user/login/', UserLoginView.as_view()),
    path('user/info/', UserInfoView.as_view()),
    path('user/menu/', UserMenuView.as_view()),
    path('user/logout/', UserLoginOutView.as_view()),
]

urlpatterns += router.urls
