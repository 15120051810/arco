"""
@Author   : liuxiangyu
@File     : login_views.py
@TIme     : 2024/8/5 09:50
@Software : PyCharm
"""

import logging
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)

from users.serializers import RouerTreeSerializer, RouerFlattenSerializer
from system_manage.views import RouterViewSet
from .serializers import UserSerializer
from .models import Router

from utils.common import viewlog

logger = logging.getLogger('arco')


class UserLoginView(TokenObtainPairView):
    """
    用户登录
    """
    """
        用户登录，重写TokenObtainPairView
        为什么自定义接口在访问时，不提示未认证？
        因为 继承的类里面指定了
                permission_classes = ()
                authentication_classes = ()
    """

    def post(self, request: Request, *args, **kwargs) -> Response:

        serializer = self.get_serializer(data=request.data)
        logger.info(f'serializer-->{serializer}')

        try:
            serializer.is_valid(raise_exception=True)

        except Exception as e:
            # print('e', e, dir(e), type(e), e.args)
            # raise InvalidToken(e.args[0])

            return Response({'code': 201, 'msg': str(e), 'ok': False},
                            status=status.HTTP_200_OK)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class UserInfoView(APIView):
    """
    用户信息
    """

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, *args, **kwargs) -> Response:

        user_obj = request.user
        # logger.info(f"获取当前请求的用户对象 {user_obj} ")

        try:

            username = user_obj.username
            if username:
                serializer_data = UserSerializer(user_obj).data
                return Response(data={"code": 200, "data": serializer_data}, status=status.HTTP_200_OK)
            else:
                logger.warning(f"该对象不存在 ")
                # serializer.is_valid():
                # serializer.save()
                # return Response(serializer.data)

        except Exception as e:
            raise Exception('获取用户信息失败', e)


class UserLoginOutView(APIView):
    """
    用户退出
    """

    def post(self, request):
        """
        """
        data = request.data
        logger.info(f"前端传参~ {data}")

        res = {
            "data": None,
            "status": 'ok',
            "msg": '请求成功',
            "code": 20000,
        }

        return Response(data=res)


class UserMenuView(APIView):
    """
    用户菜单
    1 管理员 将菜单树与菜单列表返回
    2 非管理员 将该用户对应的菜单树与菜单列表返回
    """

    permission_classes = [IsAuthenticated]

    def build_tree(self, queryset):
        """
        把扁平的 Router queryset 构造成树结构。
        """
        id_to_node = {}
        tree = []

        # 第一步：初始化每个节点的 children
        for obj in queryset:
            id_to_node[obj.id] = {
                "id": obj.id,
                "name": obj.name,
                "redirect": obj.redirect,
                "component": obj.component,
                "meta": {
                    "locale": obj.locale_title,
                    "icon": obj.icon,
                    "hideInMenu": not obj.show,
                    "order": obj.order_index,
                    "roles": [r.name for r in obj.roles.all()],
                },
                "children": [],
                "parent_id": obj.parent_id,
            }
        print('id_to_node', id_to_node)
        # 第二步：组装树
        for node in id_to_node.values():
            parent_id = node["parent_id"]
            if parent_id and parent_id in id_to_node:
                print('parent_id', parent_id)
                id_to_node[parent_id]["children"].append(node)
            else:
                tree.append(node)  # 根节点

        return tree

    @viewlog('V', '获取当前菜单树')
    def get(self, request):
        if self.request.user.is_superuser:  # 超级用户可以看所有菜单
            queryset = Router.objects.filter(parent__isnull=True, system=0).order_by('order_index').distinct()
            serializer = RouerTreeSerializer(instance=queryset, many=True)
            return Response(data=serializer.data)
        else:  # 其余用户基于所属角色，查询自己能看到的菜单。1 如果某个角色，只勾选了某个目录下的页面，该目录是办勾选状态，也要将该目录菜单返回 2 包含多个层级
            # Router <--(related_name='roles')-- Role <--(related_name='role_users')-- User
            # 可以像字典一样链式下去：A.objects.filter(B__C__D=value)。

            # 查出所有已勾选的 的目录和页面，生成路由树返回给前端
            queryset = Router.objects.filter(type__in=[0, 1], system=0,
                                             roles__role_users=self.request.user).order_by(
                'order_index')
            print('queryset', queryset)
            tree = self.build_tree(queryset)
            return Response(data=tree)


class UserPermissionView(APIView):
    """
    用户权限
    1 超级用户 返回所有权限列表
    2 非超级用户 返回指定角色下的列表
    """

    permission_classes = [IsAuthenticated]

    @viewlog('V', '获取当前权限列表')
    def get(self, request):
        if self.request.user.is_superuser:  # 超级用户可以看所有菜单
            queryset = Router.objects.filter(type=2, system=0).order_by('order_index').distinct()
        else:
            # 查出所有已勾选的 的目录和页面，生成路由树返回给前端
            queryset = Router.objects.filter(type=2, system=0, roles__role_users=self.request.user).distinct()

        serializer = RouerFlattenSerializer(instance=queryset, many=True)
        return Response(data=serializer.data)