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
from users.views import UserViewSet, AppletLogin, AppletGetSuperOrg, AppletSearchOrg
from .views import CheckBaseTokenView, DestroyBaseTokenView, GetUserRegionProvinceTreeAPIView, GetUserOrgsView, \
    GetUserRegionsView, GetUserProvinceView, GetOrgReturnShopAPIView, GetUserChainCorpView, \
    GetUserDepartmentalProjectTreeView, GetUserMedicalWorkerDPTreeView

app_name = "users"

router = DefaultRouter() if settings.DEBUG else SimpleRouter()
router.register("", UserViewSet)

urlpatterns = [
    path('checkbasetoken/', CheckBaseTokenView.as_view()),
    path('destorybasetoken/', DestroyBaseTokenView.as_view()),

    path('region_province_tree/', GetUserRegionProvinceTreeAPIView.as_view()),
    path('departmental_project_tree/', GetUserDepartmentalProjectTreeView.as_view()),
    path('medical_worker_dp_tree/', GetUserMedicalWorkerDPTreeView.as_view()),

    path('orgs/', GetUserOrgsView.as_view()),

    path('chain_corps/', GetUserChainCorpView.as_view()),

    path('reginons/', GetUserRegionsView.as_view()),
    path('provinces/', GetUserProvinceView.as_view()),

    path('get_org_return_shop/', GetOrgReturnShopAPIView.as_view()),

    path('applet_login/', AppletLogin.as_view()),

    path('applet_get_superorg/', AppletGetSuperOrg.as_view()),
    path('applet_search_org/', AppletSearchOrg.as_view()),
]

urlpatterns += router.urls
