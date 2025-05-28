from django.contrib.auth import get_user_model
from users.models import Role, Router
from rest_framework import serializers

User = get_user_model()


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["name"]


class RouerFlattenSerializer(serializers.ModelSerializer):
    """菜单铺平"""

    class Meta:
        model = Router
        fields = ('keyword',)  # ✅只保留这些字段
        # exclude = ('component', 'created_at', 'updated_at', 'redirect', 'locale_title', 'order_index', 'show', 'icon')


class UserSerializer(serializers.ModelSerializer):
    # roles = RoleSerializer(many=True) # 前端登录后，将用户的角色信息返回过去，前端可以基于角色信息去展示不同内容
    role = serializers.SerializerMethodField()  # 自定义字段
    permission = serializers.SerializerMethodField()  # 自定义字段
    homepage = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["username", "name", 'email', 'mobile', 'is_active', "is_staff",
                  "is_superuser", "staff_code", 'role', 'permission', 'homepage']

    def get_role(self, obj) -> list:
        return [role.keyword for role in obj.roles.all()]  # 返回角色名称列表

    def get_homepage(self, obj):
        """返回首页的组件名称"""
        page = obj.home_page
        return page.component


    def get_permission(self, obj) -> list:
        """用户->找到多个角色->多个角色找到菜单->多个菜单中，每个菜单有绑定多个权限关键字，将权限关键字全部返回"""
        # return [role.keyword for role in obj.roles.all()]  # 返回角色名称列表
        permission = Router.objects.filter(roles__role_users=obj, type=2)
        data = RouerFlattenSerializer(instance=permission, many=True).data  # 返回角色名称列表
        names = [item['keyword'] for item in data]
        return names


class RouerTreeSerializer(serializers.ModelSerializer):
    """菜单树序列化器"""
    children = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    path = serializers.CharField(source='redirect')
    key = serializers.SerializerMethodField()
    parent = serializers.SlugRelatedField(slug_field='id', queryset=Router.objects.all(), allow_null=True,
                                          required=False)
    meta = serializers.SerializerMethodField()

    class Meta:
        model = Router
        depth = 1
        exclude = ('created_at', 'updated_at', 'redirect', 'locale_title', 'order_index', 'show', 'icon')

    def get_children(self, obj):
        """递归获取子节点"""
        children = obj.children.all()
        if not children.exists():
            return []  # 没有子节点时直接返回
        children = obj.children.exclude(type=2).order_by(
            'order_index')  # 排除权限，否则前段读取{t(element?.meta?.locale || '')} 报警告
        return RouerTreeSerializer(children, many=True).data

    def get_key(self, obj):
        """要是前段使用key,则需要序列化key字段"""
        return obj.id

    def get_name(self, obj):
        return obj.name

    def get_meta(self, obj: Router):
        meta_info = {'locale': obj.locale_title, 'hideInMenu': not obj.show, 'order': obj.order_index, 'icon': obj.icon,
                     'roles': [role.keyword for role in obj.roles.all()]}

        return meta_info
