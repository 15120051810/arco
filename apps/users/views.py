"""
@Author   : liuxiangyu
@File     : login_views.py
@TIme     : 2024/8/5 09:50
@Software : PyCharm
"""

import logging
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)
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
        # print('serializer', serializer)

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
        logger.info(f"获取当前请求的用户对象 {user_obj} ")

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


class UserMenu(APIView):
    """
    用户菜单
    """

    @viewlog('v', '获取菜单')
    def post(self, request):

        menuList = [
            {
                "path": '/dashboard',
                "name": 'dashboard',
                "meta": {
                    "locale": 'menu.server.dashboard',
                    "requiresAuth": True,
                    "icon": 'icon-dashboard',
                    "order": 1,
                },
                "children": [
                    {
                        "path": 'workplace',
                        "name": 'Workplace',
                        "meta": {
                            "locale": 'menu.server.workplace',
                            "requiresAuth": True,
                        },
                    }],
            },
            {
                "path": '/dashboard',
                "name": 'dashboard',
                "meta": {
                    "locale": 'menu.server.dashboard',
                    "requiresAuth": True,
                    "icon": 'icon-dashboard',
                    "order": 1,
                },
            }
        ]

        res = {
            "data": menuList,
            "status": 'ok',
            "msg": '请求成功',
            "code": 20000,
        }

        return Response(data=res)
