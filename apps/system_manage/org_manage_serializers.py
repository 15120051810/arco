"""
@Author   : liuxiangyu
@File     : org_manage_views.py
@TIme     : 2024/10/11 18:25
@Software : PyCharm
"""
from django.db import models

from users.models import Org
from rest_framework import serializers


class OrgFlattenSerializer(serializers.ModelSerializer):
    """组织铺平"""

    class Meta:
        model = Org
        exclude = ('created_at',)


class OrgTreeSerializer(serializers.ModelSerializer):
    """ 在反序列化保存一个组织的时候，parent该怎么指定
    1. 如果不重写parent 字段，模型序列化器就自动使用 NestedSerializer（嵌套序列化器）
         parent = NestedSerializer(allow_null=True, read_only=True) 允许其为 null，并通过 read_only=True 使其在创建时不可直接赋值。

    2. 需求：需要在序列化的时候保存上，外键字段需要加 SlugRelatedField，指定 slug_field='org_id'，这表示它将使用 org_id 来查找对应的父组织。
        这样前端可以直接传递父组织的'org_id'
            eg:{"parent": "3f615c8f0dce11e99d340242ac110003","org_name":"新的组织名称"}
    3. 此处 queryset=Org.objects.all() 作用，查看 随笔ChatGpt.md `外键序列化器中queryset这里面的作用`
    """
    children = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    # org_type = serializers.SerializerMethodField() # 写成这样就不支持反序列化了
    key = serializers.SerializerMethodField()  # 1 前端树结构需要key字段,则需要序列化 2 另一种前端页面使用row-key去指定使用id，则不需要序列化该字段父组织 ID 作为外键 3 前端可以指定格式
    parent = serializers.SlugRelatedField(slug_field='org_id', queryset=Org.objects.all(), allow_null=True,
                                          required=False)

    class Meta:
        model = Org
        depth = 1
        exclude = ('created_at', 'updated_at')

    def get_children(self, obj):
        """递归获取子节点"""
        children = obj.children.all()
        if not children.exists():
            return  # 没有子节点时直接返回

        # 递归调用子节点的序列化器
        return OrgTreeSerializer(children, many=True).data

    def get_key(self, obj):
        """要是前段使用key,则需要序列化key字段"""
        return obj.id

    def get_title(self, obj):
        return obj.org_name

    def to_representation(self, instance):
        """在序列化时 组织类型返回友好名称,也可添加多的内容"""
        representation = super().to_representation(instance)
        representation['org_type_label'] = dict(Org.org_type_choices).get(instance.org_type)
        return representation
