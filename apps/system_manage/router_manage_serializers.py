"""
@Author   : liuxiangyu
@File     : Router_manage_views.py
@TIme     : 2024/10/11 18:25
@Software : PyCharm
"""
from django.db import models

from users.models import Router
from rest_framework import serializers

class RouterFlattenSerializer(serializers.ModelSerializer):
    """为序列化使用，不用树形"""

    class Meta:
        model = Router
        exclude = ('created_at',)


class RouterTreeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    parent = serializers.SlugRelatedField(slug_field='id', queryset=Router.objects.all(), allow_null=True,
                                          required=False)

    class Meta:
        model = Router
        depth = 1
        exclude = ('created_at', 'updated_at', 'icon')

    def get_children(self, obj):
        """递归获取子节点"""
        children = obj.children.all()
        if not children.exists():
            return  # 没有子节点时直接返回

        # 递归调用子节点的序列化器
        return RouterTreeSerializer(children, many=True).data
