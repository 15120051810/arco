from django.contrib.auth import get_user_model
from users.models import Role, Router
from rest_framework import serializers

User = get_user_model()


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["name"]


class UserSerializer(serializers.ModelSerializer):
    # roles = RoleSerializer(many=True) # 前端登录后，将用户的角色信息返回过去，前端可以基于角色信息去展示不同内容
    role = serializers.SerializerMethodField()  # 自定义字段
    permission = serializers.SerializerMethodField()  # 自定义字段

    class Meta:
        model = User
        fields = ["username", "name", 'email', 'mobile', 'is_active', "is_staff",
                  "is_superuser", "staff_code", 'role', 'permission']

    def get_role(self, obj) -> list:
        return [role.keyword for role in obj.roles.all()]  # 返回角色名称列表

    def get_permission(self, obj) -> list:
        """用户->找到多个角色->多个角色找到菜单->多个菜单中，每个菜单有绑定多个权限关键字，将权限关键字全部返回"""
        return [role.keyword for role in obj.roles.all()]  # 返回角色名称列表


class RouerFlattenSerializer(serializers.ModelSerializer):
    """菜单铺平"""

    class Meta:
        model = Router
        exclude = ('created_at',)


class RouerTreeSerializer(serializers.ModelSerializer):
    """菜单树序列化器"""
    children = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    key = serializers.SerializerMethodField()
    parent = serializers.SlugRelatedField(slug_field='id', queryset=Router.objects.all(), allow_null=True,
                                          required=False)

    class Meta:
        model = Router
        depth = 1
        exclude = ('created_at', 'updated_at')

    def get_children(self, obj):
        """递归获取子节点"""
        children = obj.children.all()
        if not children.exists():
            return []  # 没有子节点时直接返回

        # 递归调用子节点的序列化器
        return RouerTreeSerializer(children, many=True).data

    def get_key(self, obj):
        """要是前段使用key,则需要序列化key字段"""
        return obj.id

    def get_name(self, obj):
        return obj.name
