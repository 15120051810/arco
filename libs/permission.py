"""
@Author   : liuxiangyu
@File     : permission.py
@TIme     : 2024/6/11 20:35
@Software : PyCharm
"""

from rest_framework.permissions import BasePermission


class DeleteOrgPermission(BasePermission):

    def has_permission(self, request, view):
        """
        是否可以访问视图， view表示当前视图对象
        """
        return True

    def has_object_permission(self, request, view, obj):
        """控制对obj对象的访问权限，此案例决绝所有对对象的访问"""
        return True
