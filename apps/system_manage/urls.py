from django.conf import settings
from django.urls import path, include
from system_manage.views import RouterViewSet, PRouterViewSet, PApiViewSet, PUserViewSet, POrgViewSet, PRoleViewSet, \
    PChannelShopViewSet, PDepartmentalProjectViewSet, PMedicalWorkerDPViewSet
from rest_framework.routers import SimpleRouter
from rest_framework_extensions.routers import (ExtendedDefaultRouter as DefaultRouter)

app_name = "system_manage"

router = DefaultRouter() if settings.DEBUG else SimpleRouter()
router.register("routers", RouterViewSet)

urlpatterns = [
    # 组织管理
    path('org_list/', POrgViewSet.as_view({'get': 'list'})),
    path('org_sync/', POrgViewSet.as_view({'post': 'org_sync'})),
    path('org_create/', POrgViewSet.as_view({'post': 'create'})),
    path('org_update/<int:pk>/', POrgViewSet.as_view({'put': 'update'})),
    path('org_destroy/<int:pk>/', POrgViewSet.as_view({'delete': 'destroy'})),

    # 用户管理
    path('user_list/', PUserViewSet.as_view({'get': 'list'})),
    path('user_create/', PUserViewSet.as_view({'post': 'create'})),
    path('user_update/<int:pk>/', PUserViewSet.as_view({'put': 'update'})),
    path('user_destroy/<int:pk>/', PUserViewSet.as_view({'delete': 'destroy'})),

    # 角色管理
    path('role_select/', PRoleViewSet.as_view({'get': 'select'})),
    path('role_list/', PRoleViewSet.as_view({'get': 'list'})),
    path('role_create/', PRoleViewSet.as_view({'post': 'create'})),
    path('role_update/<int:pk>/', PRoleViewSet.as_view({'put': 'update'})),
    path('role_destroy/<int:pk>/', PRoleViewSet.as_view({'delete': 'destroy'})),

    # 菜单管理
    path('router_select/', PRouterViewSet.as_view({'get': 'select'})),
    path('router_list/', PRouterViewSet.as_view({'get': 'list'})),
    path('router_create/', PRouterViewSet.as_view({'post': 'create'})),
    path('router_update/<int:pk>/', PRouterViewSet.as_view({'put': 'update'})),
    path('router_destroy/<int:pk>/', PRouterViewSet.as_view({'delete': 'destroy'})),

    # APIS 管理
    path('api_select/', PApiViewSet.as_view({'get': 'select'})),
    path('api_list/', PApiViewSet.as_view({'get': 'list'})),
    path('api_create/', PApiViewSet.as_view({'post': 'create'})),
    path('api_update/<int:pk>/', PApiViewSet.as_view({'put': 'update'})),
    path('api_destroy/<int:pk>/', PApiViewSet.as_view({'delete': 'destroy'})),

    # 渠道店铺
    path('chanel_shop_list/', PChannelShopViewSet.as_view({'get': 'list'})),
    # 部门项目
    path('departmental_project_list/', PDepartmentalProjectViewSet.as_view({'get': 'list'})),
    # 医工 部门项目
    path('medical_worker_dp_list/', PMedicalWorkerDPViewSet.as_view({'get': 'list'})),

]

urlpatterns += router.urls
