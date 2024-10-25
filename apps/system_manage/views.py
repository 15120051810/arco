"""
@Author   : yuanfei
@TIme     : 2023/1/30 10:02
@Software : PyCharm
"""
import json

from users.models import Router, Api, User, Role, Org, ChannelShop, DepartmentalProject, MedicalWorkerDP

# from system_manage.org_manage_serializers import OrgTreeSerializer, OrdinaryOrgSerializer
from system_manage.serializers import RouterSerializer, EditRouterSerializer, RouterTreeSerializer, ApiTreeSerializer, \
    EditApiSerializer, UserSerializer, EditUserSerializer, RoleSerializer, \
    RouterTreeTwoSerializer, EditRoleSerializer, ChannelShopTreeSerializer, DepartmentalProjectTreeSerializer, \
    MedicalWorkerDPTreeSerializer
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet
from utils.permissions import APIPermission
from utils.api_paginator import PageNum
from rest_framework import filters
from django.db.models import Q
from rest_framework.decorators import action
from system_manage.filters import RouterInfoFilter, ApiInfoFilter, OrgFilter, RoleInfoFilter
from django_filters.rest_framework import DjangoFilterBackend
from django_redis import get_redis_connection
from utils.common import viewlog

redis_cli = get_redis_connection('default')


class RouterViewSet(ListModelMixin, GenericViewSet):
    queryset = Router.objects.all().order_by('order_index')
    serializer_class = RouterSerializer
    permission_classes = [IsAuthenticated]

    def filter_queryset(self, queryset):
        queryset = super(RouterViewSet, self).filter_queryset(queryset)
        p_type = self.request.query_params.get('type')
        if p_type == 'button':
            if self.request.user.is_superuser:
                queryset = queryset.filter(type=2, system=0).distinct()
            else:
                queryset = queryset.filter(type=2, system=0, roles__role_users=self.request.user).distinct()
        else:
            # 获取前端动态路由 按钮的过滤掉
            if self.request.user.is_superuser:
                queryset = queryset.filter(type__range=[0, 1], system=0).order_by('order_index').distinct()
            else:
                queryset = queryset.filter(type__range=[0, 1], system=0, roles__role_users=self.request.user).distinct()
        return queryset



class PApiViewSet(ModelViewSet):
    queryset = Api.objects.filter(parent__isnull=True).order_by('order_index')
    serializer_class = ApiTreeSerializer
    permission_classes = [IsAuthenticated, APIPermission]
    pagination_class = PageNum
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = ApiInfoFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return EditApiSerializer
        return ApiTreeSerializer

    def get_queryset(self):
        if self.request.query_params.get('name') or self.request.method in ['PUT', 'DELETE']:
            queryset = Api.objects.all().order_by('order_index')
        else:
            queryset = Api.objects.filter(parent__isnull=True).order_by('order_index')
        return queryset

    # 获取所有的 Api 下拉列表...
    @action(methods=['get'], detail=False)
    def select(self, request, *args, **kwargs):
        qs = Api.objects.filter().order_by('order_index')
        resp = [{"id": i.id, "name": i.name, "abs_path": i.abs_path} for i in qs]
        return Response(resp)


class PChannelShopViewSet(ModelViewSet):
    serializer_class = ChannelShopTreeSerializer
    queryset = ChannelShop.objects.filter(parent__isnull=True, state=1).order_by('order_index')
    permission_classes = [IsAuthenticated, APIPermission]

    @staticmethod
    def __set_redis():
        resp_tree = ChannelShopTreeSerializer(
            ChannelShop.objects.filter(parent__isnull=True, state=1).order_by('order_index'), many=True)
        channel_shop_tree = json.dumps(resp_tree.data)
        redis_cli.set("channel_shop_tree", channel_shop_tree)
        return resp_tree.data

    def list(self, request, *args, **kwargs):
        channel_shop_tree = redis_cli.get('channel_shop_tree')
        if channel_shop_tree:
            channel_shop_tree = json.loads(channel_shop_tree.decode())
        else:
            channel_shop_tree = self.__set_redis()
        return Response(channel_shop_tree)


class PDepartmentalProjectViewSet(ModelViewSet):
    serializer_class = DepartmentalProjectTreeSerializer
    queryset = DepartmentalProject.objects.filter(parent__isnull=True, state=1).order_by('order_index')
    permission_classes = [IsAuthenticated, APIPermission]

    @staticmethod
    def __set_redis():
        resp_tree = DepartmentalProjectTreeSerializer(
            DepartmentalProject.objects.filter(parent__isnull=True, state=1).order_by('order_index'), many=True)
        departmental_project_tree = json.dumps(resp_tree.data)
        redis_cli.set("departmental_project_tree", departmental_project_tree)
        return resp_tree.data

    def list(self, request, *args, **kwargs):
        departmental_project_tree = redis_cli.get('departmental_project_tree')
        if departmental_project_tree:
            departmental_project_tree = json.loads(departmental_project_tree.decode())
        else:
            departmental_project_tree = self.__set_redis()
        return Response(departmental_project_tree)


class PMedicalWorkerDPViewSet(ModelViewSet):
    serializer_class = MedicalWorkerDPTreeSerializer
    queryset = MedicalWorkerDP.objects.filter(parent__isnull=True, state=1).order_by('order_index')
    permission_classes = [IsAuthenticated, APIPermission]

    @staticmethod
    def __set_redis():
        resp_tree = MedicalWorkerDPTreeSerializer(
            MedicalWorkerDP.objects.filter(parent__isnull=True, state=1).order_by('order_index'), many=True)
        medical_worker_dp_tree = json.dumps(resp_tree.data)
        redis_cli.set("medical_worker_dp_tree", medical_worker_dp_tree)
        return resp_tree.data

    def list(self, request, *args, **kwargs):
        medical_worker_dp_tree = redis_cli.get('medical_worker_dp_tree')
        if medical_worker_dp_tree:
            medical_worker_dp_tree = json.loads(medical_worker_dp_tree.decode())
        else:
            medical_worker_dp_tree = self.__set_redis()
        return Response(medical_worker_dp_tree)
