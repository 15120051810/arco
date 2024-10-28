from django.conf import settings
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from system_manage.org_manage_views import OrgManageTreeViewSet
from system_manage.router_manage_views import RouterManageTreeViewSet

from rest_framework_extensions.routers import (ExtendedDefaultRouter as DefaultRouter)

app_name = "system_manage"

router = DefaultRouter() if settings.DEBUG else SimpleRouter()
router.register("org", OrgManageTreeViewSet)
router.register("router", RouterManageTreeViewSet)

# 注册后，router.register 会为 OrgManageTreeViewSet 创建以下默认路由：
# GET /api/system_manage/org/ - 列出所有组织 list
# GET /api/system_manage/org/?org_name=广东区 - 精确搜索
# GET /api/system_manage/org/?search=广东 - 模糊搜索
# POST /api/system_manage/org/ - 创建一个新组织
# GET /api/system_manage/org/{id}/ - 获取特定组织的详细信息
# PUT /api/system_manage/org/{id}/ - 更新特定组织
# PATCH /api/system_manage/org/{id}/ - 部分更新特定组织
# DELETE /api/system_manage/org/{id}/ - 删除特定组织



urlpatterns = [
    # 组织管理
    path('org_type/', OrgManageTreeViewSet.as_view({'get': 'org_type'})),
    # path('org/<int:pk>/', OrgManageTreeViewSet.as_view({'get': 'retrieve'})),

    # path('org_sync/', OrgManageViewSet.as_view({'post': 'org_sync'})),
    # path('org_create/', OrgManageViewSet.as_view({'post': 'create'})),
    # path('org_update/<int:pk>/', OrgManageViewSet.as_view({'put': 'update'})),
    # path('org_destroy/<int:pk>/', OrgManageViewSet.as_view({'delete': 'destroy'})),

    # 用户管理
    # path('user_list/', PUserViewSet.as_view({'get': 'list'})),
    # path('user_create/', PUserViewSet.as_view({'post': 'create'})),
    # path('user_update/<int:pk>/', PUserViewSet.as_view({'put': 'update'})),
    # path('user_destroy/<int:pk>/', PUserViewSet.as_view({'delete': 'destroy'})),
    #
    # # 角色管理
    # path('role_select/', PRoleViewSet.as_view({'get': 'select'})),
    # path('role_list/', PRoleViewSet.as_view({'get': 'list'})),
    # path('role_create/', PRoleViewSet.as_view({'post': 'create'})),
    # path('role_update/<int:pk>/', PRoleViewSet.as_view({'put': 'update'})),
    # path('role_destroy/<int:pk>/', PRoleViewSet.as_view({'delete': 'destroy'})),
    #
    # # 菜单管理
    # path('router_select/', PRouterViewSet.as_view({'get': 'select'})),
    # path('router_list/', PRouterViewSet.as_view({'get': 'list'})),
    # path('router_create/', PRouterViewSet.as_view({'post': 'create'})),
    # path('router_update/<int:pk>/', PRouterViewSet.as_view({'put': 'update'})),
    # path('router_destroy/<int:pk>/', PRouterViewSet.as_view({'delete': 'destroy'})),
    #
    # # APIS 管理
    # path('api_select/', PApiViewSet.as_view({'get': 'select'})),
    # path('api_list/', PApiViewSet.as_view({'get': 'list'})),
    # path('api_create/', PApiViewSet.as_view({'post': 'create'})),
    # path('api_update/<int:pk>/', PApiViewSet.as_view({'put': 'update'})),
    # path('api_destroy/<int:pk>/', PApiViewSet.as_view({'delete': 'destroy'})),
    #
    # # 渠道店铺
    # path('chanel_shop_list/', PChannelShopViewSet.as_view({'get': 'list'})),
    # # 部门项目
    # path('departmental_project_list/', PDepartmentalProjectViewSet.as_view({'get': 'list'})),
    # # 医工 部门项目
    # path('medical_worker_dp_list/', PMedicalWorkerDPViewSet.as_view({'get': 'list'})),

]

urlpatterns += router.urls
