"""
@Author   : liuxiangyu
@File     : Role_manage_views.py
@TIme     : 2024/10/11 18:25
@Software : PyCharm
"""
import logging
import json
from rest_framework import status
from django.conf import settings

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet  # ModelViewSet继承成了增删改查
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter  # 该字段是自带

from .filters import UserFilter
from .user_manage_serializers import UserSerializer

from users.models import User, UserOrg
from django_redis import get_redis_connection
from utils.common import viewlog

redis_cli = get_redis_connection('default')
logger = logging.getLogger('arco')
from users.models import Org
from system_manage.org_manage_serializers import OrgTreeSerializer


class UserManageViewSet(ModelViewSet):
    """用户管理"""

    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name']
    filterset_class = UserFilter

    @viewlog('C', '创建用户')
    def create(self, request, *args, **kwargs):
        """重写只为记录操作之日"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(check_org_list=request.data.get('orgs'))
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @viewlog('U', '更新用户')
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        # self.get_object() 的作用是获取当前视图正在操作的模型实例。具体来说，它会根据请求的参数（通常是 URL 中的主键 pk 或其他唯一标识字段）来查找对应的对象
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        # 调用save()方法可以额外传递数据，这些数据可以在create()和update()中的validated_data参数获取到
        serializer.save(check_org_list=request.data.get('orgs'), org_change_flag=request.data.get('orgChangeFlag'))
        return Response(serializer.data)
