"""
@Author   : liuxiangyu
@File     : Router_manage_views.py
@TIme     : 2024/10/11 18:25
@Software : PyCharm
"""
from django.db import models
import logging

from users.models import Role, Router
from rest_framework import serializers
from .router_manage_serializers import RouterFlattenSerializer
logger = logging.getLogger('arco')




class RoleSerializer(serializers.ModelSerializer):
    """
    routers_data 字段解释
    source='routers'：表示 routers_data 字段的数据来源于 Role 模型的 routers 字段。尽管字段命名为 routers_data，它实际显示的是 routers 字段的内容。
    many=True：由于 routers 是一个多对多关系，因此使用 many=True 告诉序列化器它需要序列化成一个对象列表。
    read_only=True：指定该字段为只读，仅用于序列化输出，而不会在反序列化时接受数据输入。
    """
    routers = serializers.PrimaryKeyRelatedField(queryset=Router.objects.all(), many=True)  # 反序列化时使用 传入主键
    routers_data = RouterFlattenSerializer(source='routers', many=True, read_only=True)  # 序列化用嵌套数据

    class Meta:
        model = Role
        depth = 1  # 关联的菜单
        exclude = ('created_at',)
