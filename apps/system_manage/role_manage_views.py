"""
@Author   : liuxiangyu
@File     : Role_manage_views.py
@TIme     : 2024/10/11 18:25
@Software : PyCharm
"""
import logging
import json
from rest_framework import status

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet  # ModelViewSet继承成了增删改查
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter  # 该字段是自带

from .filters import RoleFilter
from .role_manage_serializers import RoleSerializer
from users.models import Role
from django_redis import get_redis_connection
from utils.common import viewlog

redis_cli = get_redis_connection('default')
logger = logging.getLogger('arco')


class RoleManageViewSet(ModelViewSet):
    """获取菜单树"""

    permission_classes = [IsAuthenticated]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name']
    filterset_class = RoleFilter

