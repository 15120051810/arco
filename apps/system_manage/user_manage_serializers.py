"""
@Author   : liuxiangyu
@File     : User_manage_views.py
@TIme     : 2024/10/11 18:25
@Software : PyCharm
"""
from django.db import models
import logging

from django.conf import settings
from users.models import Role, User, Org, Router, UserOrg
from rest_framework import serializers
from .role_manage_serializers import RoleSerializer
from .org_manage_serializers import OrgFlattenSerializer, OrgTreeSerializer
from .router_manage_serializers import RouterFlattenSerializer

logger = logging.getLogger('arco')


class UserOrgSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    key = serializers.SerializerMethodField()
    parent = serializers.SlugRelatedField(slug_field='org_id', queryset=Org.objects.all(), allow_null=True,
                                          required=False)

    class Meta:
        model = UserOrg
        fields = ['id', 'org', 'selected', 'half_selected', 'children', 'title', 'key', 'parent']

    def get_children(self, obj):
        # 递归序列化子节点
        children = obj.children.all()
        # 如果没有子节点，直接返回空列表
        if not children:
            return []

        children_data = UserOrgSerializer(children, many=True).data

        # 如果需要倒序，可以使用sorted函数进行倒序排列 保持跟大组织树一致
        children_data = sorted(children_data, key=lambda x: x['id'], reverse=True)
        return children_data

    def get_title(self, obj):
        """
        获取标题，通过访问 org 外键实现
        :param obj:
        :return:
        """
        if obj.org:  # 确保 org 存在
            return obj.org.org_name
        return None

    def get_key(self, obj):
        if obj.org:  # 确保 org 存在
            return obj.org.org_id
        return None


class UserSerializer(serializers.ModelSerializer):
    # orgs = serializers.PrimaryKeyRelatedField(queryset=Org.objects.all(), many=True)  # 反序列化时使用 传入主键 [1,2,3]
    # orgs_data = OrgFlattenSerializer(source='orgs', many=True, read_only=True)  # 序列化用嵌套数据  铺平

    orgs = serializers.SerializerMethodField()
    orgs_tree = serializers.SerializerMethodField()  # 组织树
    roles = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), many=True)  # 反序列化时使用 传入主键
    roles_data = RoleSerializer(source='roles', many=True, read_only=True)  # 序列化用嵌套数据
    home_page = serializers.PrimaryKeyRelatedField(queryset=Router.objects.all(), allow_null=True)  # 反序列化传入主键
    home_page_data = RouterFlattenSerializer(source='home_page', read_only=True)  # 序列化用外键数据
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)  # 密码为可选字段

    class Meta:
        model = User
        depth = 1  # 关联的菜单
        exclude = ('updated_at', 'created_at')
        extra_kwargs = {'password': {'write_only': True}}

    def get_orgs(self, obj):
        """动态生成用户的组织树"""
        return UserOrg.objects.filter(user=obj, selected=True).values_list('org_id', flat=True)

    def get_orgs_tree(self, obj):
        """动态生成用户的组织树"""
        # 获取用户的根组织（即 parent=None 的 UserOrg）
        root_nodes = UserOrg.objects.filter(user=obj, parent=None)

        # 序列化根组织及其子树
        return UserOrgSerializer(root_nodes, many=True).data

    def get_orgs_status(self, tree_data, check_orgs):
        """
        获取已选中的节点，并标注其父级，同时处理父节点的半选状态。
        :param tree_data: 树形结构数据
        :param check_orgs: 已选中节点的 ID 列表
        :return: 包含已选中和半选状态节点的列表
        """
        result = []

        def traverse(node, org_parent_id=None):
            """
            递归遍历树节点，确定节点状态。
            :param node: 当前节点
            :param org_parent_id: 当前节点的父节点 ID
            :return: 当前节点是否选中，是否为半选状态
            """
            node_id = node["id"]
            is_selected = node_id in check_orgs

            # 遍历子节点，计算子节点状态
            any_child_selected = False
            all_children_selected = True
            child = node.get("children")
            if child:
                for child in node.get("children", []):
                    child_selected, child_half_selected = traverse(child, node_id)
                    any_child_selected |= child_selected or child_half_selected
                    all_children_selected &= child_selected

            # 当前节点的状态
            if is_selected or any_child_selected:
                result.append({
                    "id": node_id,
                    "org_name": node.get("org_name"),
                    "org_parent_id": org_parent_id,
                    "selected": all([is_selected, all_children_selected]),
                    "half_selected": not all([is_selected, all_children_selected]),
                    # "status": "selected" if is_selected and all_children_selected else "half_selected"
                })

            return is_selected, any_child_selected

        # 遍历每个根节点
        for root in tree_data:
            traverse(root)

        return result

    def build_tree(self, flat_data):
        """
        构建树- 代码构建，暂时没使用，使用的是序列化器构建树
        """
        # 创建一个以 id 为键的字典，方便快速查找
        nodes = {node['id']: node for node in flat_data}
        tree = []

        # 遍历每个节点，构建树形结构
        for node in flat_data:
            parent_id = node.get('parent_id')

            # 如果该节点有父节点，则将该节点添加到父节点的 children 列表中
            if parent_id:
                parent_node = nodes.get(parent_id)
                if parent_node:
                    parent_node.setdefault('children', []).append(node)
            else:
                # 如果没有父节点，则是根节点，直接添加到树中
                tree.append(node)
        return tree

    def create(self, validated_data):
        """"""
        # orgs_data = validated_data.pop('orgs', [])
        check_org_list = validated_data.pop('check_org_list', [])
        roles_data = validated_data.pop('roles', [])
        password = validated_data.get('password', 'Miao13456')

        print('check_org_list', check_org_list)
        # 创建用户
        user = User(**validated_data)
        user.set_password(password)  # 设置加密后的密码
        user.save()  # 保存用户

        if check_org_list:
            org_qs = Org.objects.filter(org_name=settings.TOP_ORG_NAME)
            serializer = OrgTreeSerializer(org_qs, many=True)
            orgs_status_list = self.get_orgs_status(serializer.data, check_org_list)
            logger.info(f"orgs_status {orgs_status_list}")

            user_org_dict = {}
            for org in reversed(orgs_status_list):
                if not org['org_parent_id']:
                    parent_id = None
                else:
                    parent_id = user_org_dict[org['org_parent_id']]

                user_org_entry = UserOrg(
                    user=user,
                    org_id=org['id'],
                    selected=org['selected'],
                    half_selected=org['half_selected'],
                    org_parent_id=org['org_parent_id'],
                    parent_id=parent_id
                )
                user_org_entry.save()
                # 将创建的主键id添加到列表中

                user_org_dict[org['id']] = user_org_entry.id

        # 使用 set() 方法来处理 ManyToManyField 的关系
        # user.orgs.set(orgs_data)  # 设置用户的组织
        user.roles.set(roles_data)  # 设置用户的角色

        return user

    def update(self, instance, validated_data):
        """更新某个示例
        额外的用pop 从validated_data 剔除出来
        """

        logger.info(f'已验证的数据 {validated_data}')

        check_org_list = validated_data.pop('check_org_list', [])
        org_change_flag = validated_data.pop('org_change_flag', False)  # 确定组织是否有更新
        logger.info(f'需要修改的组织 {check_org_list, org_change_flag}')

        if org_change_flag and check_org_list:
            existing_orgs = UserOrg.objects.filter(user_id=instance)
            logger.info(f"已存在的组织-->{existing_orgs}")
            UserOrg.objects.filter(user_id=instance, id__in=existing_orgs).delete()
            logger.info(f"删除已存在的组织-->{existing_orgs}")

            # 重新构建
            org_qs = Org.objects.filter(org_name=settings.TOP_ORG_NAME)
            serializer = OrgTreeSerializer(org_qs, many=True)
            orgs_status_list = self.get_orgs_status(serializer.data, check_org_list)
            logger.info(f"orgs_status {orgs_status_list}")

            user_org_dict = {}
            for org in reversed(orgs_status_list):
                if not org['org_parent_id']:
                    parent_id = None
                else:
                    parent_id = user_org_dict[org['org_parent_id']]

                user_org_entry = UserOrg(
                    user=instance,
                    org_id=org['id'],
                    selected=org['selected'],
                    half_selected=org['half_selected'],
                    org_parent_id=org['org_parent_id'],
                    parent_id=parent_id
                )
                user_org_entry.save()
                # 将创建的主键id添加到列表中

                user_org_dict[org['id']] = user_org_entry.id

        return super().update(instance, validated_data)
