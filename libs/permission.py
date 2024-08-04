"""
@Author   : liuxiangyu
@File     : permission.py
@TIme     : 2024/6/11 20:35
@Software : PyCharm
"""

from rest_framework.permissions import BasePermission


class MyPermission(BasePermission):

    def has_permission(self, request, view):
        """控制对obj对象的访问权限，此案例决绝所有对对象的访问"""

        print('request', request)
        print('view', view)
        return True
