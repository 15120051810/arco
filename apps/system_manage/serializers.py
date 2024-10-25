"""
@Author   : yuanfei
@TIme     : 2023/1/30 10:02
@Software : PyCharm
"""

from users.models import Router, Api, User, Org, Role, ChannelShop, DepartmentalProject, MedicalWorkerDP
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'name', 'roles', 'email', 'is_active', 'is_superuser', 'last_login', 'orgs',
                  'home_page', 'channel_shop', 'mobile', 'departmental_project', 'medical_worker_dp')
        depth = 1


class EditUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validate_data):
        user = super(EditUserSerializer, self).create(validated_data=validate_data)
        user.set_password(validate_data.get('password'))
        user.save()
        return user

    def update(self, instance, validated_data):
        # 当前密码
        password = validated_data.get('password')
        if password == instance.password:
            print('不修改密码 使用原始密码不用加密')
            user = super(EditUserSerializer, self).update(instance, validated_data=validated_data)
        else:
            print('修改密码 输入密码为明文需要加密')
            user = super(EditUserSerializer, self).update(instance, validated_data=validated_data)
            user.set_password(validated_data.get('password'))
            user.save()
        return user


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"
        depth = 1


class EditRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class RouterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Router
        fields = ['id', 'name', 'title', 'component', 'redirect', 'icon', 'show', 'parent_id', 'keyword', 'type',
                  'locale_title']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['parent_id'] is None:
            data['parent_id'] = 0
        return data


class EditRouterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Router
        fields = "__all__"


class RouterChildSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Router
        exclude = ['created_at']
        depth = 1

    def get_children(self, obj):
        if obj.children:
            return RouterChildSerializer(obj.children, many=True).data
        return None


class RouterTreeSerializer(serializers.ModelSerializer):
    children = RouterChildSerializer(many=True)

    class Meta:
        model = Router
        exclude = ['created_at']
        depth = 1


class RouterChildTwoSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Router
        fields = ['id', 'title', 'children']
        depth = 1

    def get_children(self, obj):
        if obj.children:
            return RouterChildTwoSerializer(obj.children, many=True).data
        return None


class RouterTreeTwoSerializer(serializers.ModelSerializer):
    children = RouterChildTwoSerializer(many=True)

    class Meta:
        model = Router
        fields = ['id', 'title', 'children']
        depth = 1


class EditApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Api
        fields = "__all__"


class ApiChildSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Api
        exclude = ['created_at']
        depth = 1

    def get_children(self, obj):
        if obj.children:
            return ApiChildSerializer(obj.children, many=True).data
        return None


class ApiTreeSerializer(serializers.ModelSerializer):
    children = ApiChildSerializer(many=True)

    class Meta:
        model = Api
        exclude = ['created_at']
        depth = 1


class ChannelShopSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = ChannelShop
        fields = '__all__'

    def get_children(self, obj):
        if obj.children: return ChannelShopSerializer(obj.children, many=True).data
        return None


class ChannelShopTreeSerializer(serializers.ModelSerializer):
    children = ChannelShopSerializer(many=True)

    class Meta:
        model = ChannelShop
        fields = '__all__'


class DepartmentalProjectTreeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = DepartmentalProject
        fields = '__all__'

    def get_children(self, obj):
        if obj.children: return DepartmentalProjectTreeSerializer(obj.children, many=True).data
        return None


class MedicalWorkerDPTreeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = MedicalWorkerDP
        fields = '__all__'

    def get_children(self, obj):
        if obj.children: return MedicalWorkerDPTreeSerializer(obj.children, many=True).data
        return None
