from django.conf import settings
from django.urls import path
from download_center.views import DownLoadCenterViewSet, CallBackView
from rest_framework.routers import SimpleRouter

app_name = "download_center"

router =  SimpleRouter()
router.register("downloads", DownLoadCenterViewSet)

urlpatterns = [
    path('callback/', CallBackView.as_view())   # 回调函数
]

urlpatterns += router.urls
