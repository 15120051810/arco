"""
@Author   : yuanfei
@TIme     : 2023/1/30 10:02
@Software : PyCharm
"""
import json

from users.models import Router, Api, User, Role, Org, ChannelShop, DepartmentalProject, MedicalWorkerDP
from system_manage.serializers import RouterSerializer, EditRouterSerializer, RouterTreeSerializer, ApiTreeSerializer, \
    EditApiSerializer, UserSerializer, EditUserSerializer, OrgTreeSerializer, OrdinaryOrgSerializer, RoleSerializer, \
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
from system_manage.filters import RouterInfoFilter, ApiInfoFilter, OrgInfoFilter, RoleInfoFilter
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


class POrgViewSet(ModelViewSet):
    serializer_class = OrgTreeSerializer
    queryset = Org.objects.filter(parent__isnull=True).order_by('order_index')
    permission_classes = [IsAuthenticated, APIPermission]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = OrgInfoFilter

    @staticmethod
    def __set_redis():
        resp_tree = OrgTreeSerializer(Org.objects.filter(parent__isnull=True).order_by('order_index'), many=True)
        orgs_tree = json.dumps(resp_tree.data)
        redis_cli.set("orgs_tree", orgs_tree)
        return resp_tree.data

    def list(self, request, *args, **kwargs):
        if self.request.query_params.get('org_name') or self.request.query_params.get('org_type'):
            return super(POrgViewSet, self).list(request)
        else:
            orgs_tree = redis_cli.get('orgs_tree')
            if orgs_tree:
                orgs_tree = json.loads(orgs_tree.decode())
            else:
                orgs_tree = self.__set_redis()
            return Response(orgs_tree)

    def get_queryset(self):
        if self.request.query_params.get('org_name') or self.request.method in ['PUT', 'DELETE']:
            queryset = Org.objects.all().order_by('order_index')
        elif self.request.query_params.get('org_type'):
            queryset = Org.objects.exclude(org_name='电商').order_by('order_index')
        else:
            queryset = Org.objects.filter(parent__isnull=True).order_by('order_index')
        return queryset

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT'] or self.request.query_params.get('org_type'):
            return OrdinaryOrgSerializer
        return OrgTreeSerializer

    @action(methods=['post'], detail=False)
    def org_sync(self, request, *args, **kwargs):
        """同步机构"""
        self.__set_redis()
        return Response("sync success")


class PUserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('-id')
    permission_classes = [IsAuthenticated, APIPermission]
    pagination_class = PageNum
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('is_active', 'is_superuser', 'id')

    def get_queryset(self):
        org_id = self.request.query_params.get('org_id[]')
        channel_shop_id = self.request.query_params.get('channel_shop_id[]')
        departmental_project_id = self.request.query_params.get('departmental_project_id[]')
        medical_worker_dp_id = self.request.query_params.get('medical_worker_dp_id[]')

        print('self.request.query_params', self.request.query_params)

        queryset = User.objects.all().order_by('-id')
        if self.request.method == 'GET' and org_id:
            queryset = queryset.filter(orgs__id=org_id)
        if self.request.method == 'GET' and channel_shop_id:
            queryset = queryset.filter(channel_shop__id=channel_shop_id)
        if self.request.method == 'GET' and departmental_project_id:
            queryset = queryset.filter(departmental_project__id=departmental_project_id)
        if self.request.method == 'GET' and medical_worker_dp_id:
            queryset = queryset.filter(medical_worker_dp__id=medical_worker_dp_id)

        name = self.request.query_params.get('name')
        if self.request.method == 'GET' and name and name != '':
            queryset = queryset.filter(Q(username__icontains=name) | Q(name__icontains=name)).order_by('-id')

        return queryset

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return EditUserSerializer
        return UserSerializer

    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     start_orgs = [i.id for i in instance.orgs.all()]
    #
    #     # 想给该新用户配置什么权限？
    #     if not request.user.is_superuser and instance.is_superuser:
    #         return Response('只有SuperUser才能对SuperUser操作', status=403)
    #
    #     if "roles" in request.data.keys():
    #         roles = request.data.get('roles')
    #         super_obj = Role.objects.filter(name="SuperUser").first()
    #
    #         if roles and not request.user.is_superuser and super_obj.id in roles:
    #             return Response('只有SuperUser才能设置SuperUser', status=403)
    #         if request.user.is_superuser and request.user.username == instance.username and super_obj.id not in roles:
    #             return Response('SuperUser不能给自己禁用了', status=403)
    #         if roles and super_obj.id in roles and request.user.is_superuser:
    #             request.data['is_superuser'] = 1
    #         elif roles and super_obj.id not in roles and request.user.is_superuser:
    #             request.data['is_superuser'] = 0
    #     else:
    #         if "is_active" in request.data.keys():
    #             if request.user.username == instance.username:
    #                 return Response('不能禁用自己', status=403)
    #
    #     username = request.data.get('username')
    #     password = request.data.get('password')
    #     if not username or username == '':
    #         request.data['username'] = instance.username
    #     if not password or password == '':
    #         request.data['password'] = instance.password
    #
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #
    #     if getattr(instance, '_prefetched_objects_cache', None):
    #         # If 'prefetch_related' has been applied to a queryset, we need to
    #         # forcibly invalidate the prefetch cache on the instance.
    #         instance._prefetched_objects_cache = {}
    #
    #     logger.info(f"{username} 更换了组织架构 ")
    #     result = get_user_orgs(request)
    #     redis_cli.set(username, json.dumps(result), settings.USER_ORG_TIMEOUT)
    #     return Response(serializer.data)


class PRoleViewSet(ModelViewSet):
    serializer_class = RoleSerializer
    queryset = Role.objects.filter().order_by('-created_at')
    permission_classes = [IsAuthenticated, APIPermission]
    pagination_class = PageNum
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = RoleInfoFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return EditRoleSerializer
        return RoleSerializer

    # 获取所有的角色名称...
    @action(methods=['get'], detail=False)
    def select(self, request, *args, **kwargs):
        qs = Role.objects.all()
        resp = [{"id": i.id, "name": i.name} for i in qs]
        return Response(resp)


class PRouterViewSet(ModelViewSet):
    queryset = Router.objects.filter(parent__isnull=True).order_by('order_index')
    serializer_class = RouterTreeSerializer
    permission_classes = [IsAuthenticated, APIPermission]
    pagination_class = PageNum
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = RouterInfoFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return EditRouterSerializer

        if self.request.query_params.get('type') == 'small_tree':
            return RouterTreeTwoSerializer
        return RouterTreeSerializer

    def get_queryset(self):
        if self.request.query_params.get('title') or self.request.method in ['PUT', 'DELETE']:
            queryset = Router.objects.all().order_by('order_index')
        else:
            queryset = Router.objects.filter(parent__isnull=True).order_by('order_index')
        return queryset

    # 获取所有的 菜单 下拉列表...
    @action(methods=['get'], detail=False)
    def select(self, request, *args, **kwargs):
        type = request.query_params.get('type')
        if type:
            qs = Router.objects.filter(show=True, type=1).order_by('order_index')
        else:
            qs = Router.objects.filter().order_by('order_index')
        resp = [{"id": i.id, "title": i.title} for i in qs]
        return Response(resp)


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
