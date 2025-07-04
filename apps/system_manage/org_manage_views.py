"""
@Author   : liuxiangyu
@File     : org_manage_views.py
@TIme     : 2024/10/11 18:25
@Software : PyCharm
"""
import logging
import json
from rest_framework import status
from django.conf import settings
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet  # ModelViewSet继承成了增删改查
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter  # 该字段是自带

from users.models import Org
from libs.permission import DeleteOrgPermission
from .org_manage_serializers import OrgTreeSerializer, OrgFlattenSerializer
from .filters import OrgFilter
from django_redis import get_redis_connection
from utils.common import viewlog

redis_cli = get_redis_connection('default')
logger = logging.getLogger('arco')


class OrgManageTreeViewSet(ModelViewSet):
    """获取组织树"""

    permission_classes = [IsAuthenticated, DeleteOrgPermission]

    queryset = Org.objects.all()
    serializer_class = OrgTreeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]  # DjangoFilterBackend这里需要写过滤后端，
    filterset_fields = ['org_name', 'org_id']  # 精确过滤 路由格式 /api/system_manage/org/?org_name=广东区

    # search_fields = ['org_name', 'org_id']  # 模糊搜索，结合 SearchFilter，路由格式 /api/system_manage/org/?search=广东，广东就会在org_name, org_id这两个字段中去查询
    # filterset_class = OrgFilter  # 更复杂的查询场景下用 例如有的字段需要范围查询等等


    def _clear_redis(self):
        """编辑删除或者创建的时候，先清空之前的缓存"""
        res = redis_cli.get('top_org_tree')
        if res:
            redis_cli.delete('top_org_tree')

    def get_queryset(self):
        org_name = self.request.query_params.get('org_name', None)
        if self.action == 'list' and not org_name:  # 初始化页面的时候展示组织树
            return self.queryset.filter(org_name=settings.TOP_ORG_NAME)
        return self.queryset

    def org_type(self, request, *args, **kwargs):
        """获取组织类型"""
        # org_types = [{'k': choice[0], 'v': choice[1]} for choice in Org.org_type_choices]
        # return Response(data=org_types)

        return JsonResponse(dict(Org.org_type_choices))

    # def list(self, request, *args, **kwargs):
    #     print('request',request)
    #     return super(OrgManageTreeViewSet, self).list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """重写list"""
        org_name = self.request.query_params.get('org_name', None)
        queryset = self.filter_queryset(self.get_queryset())
        logger.info(f"当前查询集-->{queryset}")

        serializer = self.get_serializer(queryset, many=True)

        if org_name:
            return Response(serializer.data)

        res = redis_cli.get('top_org_tree')
        if res:
            return Response(json.loads(res))
        else:
            data = serializer.data
            redis_cli.set('top_org_tree',json.dumps(data))
            return Response(data)

    @viewlog('I', '添加组织')
    def create(self, request, *args, **kwargs):
        self._clear_redis()
        return super(OrgManageTreeViewSet, self).create(request, *args, **kwargs)

    @viewlog('D', '删除组织')
    def destroy(self, request, *args, **kwargs):
        self._clear_redis()
        return super(OrgManageTreeViewSet, self).destroy(request, *args, **kwargs)

    @viewlog('U', '更新组织')
    def update(self, request, *args, **kwargs):
        self._clear_redis()
        return super(OrgManageTreeViewSet, self).update(request, *args, **kwargs)
