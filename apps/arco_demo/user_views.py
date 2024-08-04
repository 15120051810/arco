"""
@Author   : liuxiangyu
@File     : user_views.py
@TIme     : 2024/3/14 15:26
@Software : PyCharm
"""

import logging

from rest_framework.views import APIView
from rest_framework.response import Response

logger = logging.getLogger('arco')


class UserLogin(APIView):
    """
    用户登录
    """

    def post(self, request):
        """
        """
        data = request.data
        logger.info(f"前端传参~ {data}")

        res = {
            "data": {"token": '12345'},
            "status": 'ok',
            "msg": '请求成功',
            "code": 20000,
        }
        return Response(data=res)


class UserInfo(APIView):
    """
    用户信息
    """

    def post(self, request):
        """
        """
        data = request.data
        logger.info(f"前端传参~ {data}")

        infos = {
          "name": 'Ekko',
          # "avatar":'https://img2.baidu.com/it/u=2909427933,1285872418&fm=253&fmt=auto&app=138&f=JPEG?w=807&h=800',
          "email": 'wangliqun@email.com',
          "job": 'frontend',
          "jobName": '前端艺术家',
          "organization": 'Frontend',
          "organizationName": '前端',
          "location": 'beijing',
          "locationName": '北京',
          "introduction": '人潇洒，性温存',
          "personalWebsite": 'https://www.arco.design',
          "phone": '150****0000',
          "registrationDate": '2013-05-10 12:10:00',
          "accountId": '15012312300',
          "certification": 1,
          "role":"admin",
        }

        res = {
            "data": infos,
            "status": 'ok',
            "msg": '请求成功',
            "code": 20000,
        }
        return Response(data=res)



class UserOutLogin(APIView):
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
    def post(self, request):
        data = request.data
        logger.info(f"前端传参~ {data}")

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
                },
                {
                  "path": 'https://arco.design',
                  "name": 'arcoWebsite',
                  "meta": {
                    "locale": 'menu.arcoWebsite',
                    "requiresAuth": True,
                  },
                },
              ],
            },
          ]

        res = {
            "data": menuList,
            "status": 'ok',
            "msg": '请求成功',
            "code": 20000,
        }

        return Response(data=res)
