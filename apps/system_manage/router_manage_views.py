"""
@Author   : liuxiangyu
@File     : Router_manage_views.py
@TIme     : 2024/10/11 18:25
@Software : PyCharm
"""
import logging
import json
from rest_framework import status

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .filters import RouterFilter
from rest_framework.viewsets import ModelViewSet  # ModelViewSet继承成了增删改查
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter  # 该字段是自带

from users.models import Router
from .router_manage_serializers import RouterTreeSerializer
from django_redis import get_redis_connection
from utils.common import viewlog

redis_cli = get_redis_connection('default')
logger = logging.getLogger('arco')


class RouterManageTreeViewSet(ModelViewSet):
    """获取菜单树"""

    permission_classes = [IsAuthenticated]

    queryset = Router.objects.all()
    serializer_class = RouterTreeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['title']
    filterset_class = RouterFilter

    def get_queryset(self):
        title = self.request.query_params.get('title', None)
        if self.action == 'list' and not title:
            return self.queryset.filter(type=0, parent__isnull=True)  # 取目录结构，并且父级目录是null,防止序列化出子目录
        logger.info(f"搜索查询--> {title} ")
        return self.queryset


    @viewlog('I', '添加菜单')
    def create(self, request, *args, **kwargs):
        """重写只为记录操作之日"""
        return super(RouterManageTreeViewSet, self).create(request, *args, **kwargs)


    @viewlog('U', '更新菜单')
    def update(self, request, *args, **kwargs):
        return super(RouterManageTreeViewSet, self).update(request, *args, **kwargs)
