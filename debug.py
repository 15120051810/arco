"""
@Author   : liuxiangyu
@File     : debug.py.py
@TIme     : 2024/8/10 10:58
@Software : PyCharm
"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.local")
django.setup()

# 导入models一定要在 django.setup() 之后
from users.models import User, Role, Org, Api, Router
from system_manage.org_manage_serializers import OrgFlattenSerializer,OrgTreeSerializer

user = User.objects.get(username='liuxiangyu')


def get_user_roles():
    """获取当前用户角色"""
    roles = user.roles.all()
    print('正查-》当前用户角色',roles)
    # one_role= roles.get() # get()语法是危险的 1 如果当前用户有 多个角色 会报错：MultipleObjectsReturned；2 如果 没有角色 会报错：DoesNotExist。
    one_role = roles.first()

    # 可以像字典一样链式下去：A.objects.filter(B__C__D=value)。
    roles = Role.objects.filter(role_users=user)
    print('反查-》通过该用户查询角色',roles)

    # 该用户能看哪些路由 !!!!! 理解的时候 roles__role_users=user 从右往左理解
    # Router.roles 👉 多对多字段，指向 Role
    # Role.role_users 👉 多对多字段，指向 User
    routers = Router.objects.filter(roles__role_users=user).distinct()
    # print("sql",Router.objects.filter(roles__role_users=user).distinct().query)
    """
        SELECT DISTINCT * 
        FROM `users_router` 
        INNER JOIN `users_role_routers` ON (`users_router`.`id` = `users_role_routers`.`router_id`) 
        INNER JOIN `users_role` ON (`users_role_routers`.`role_id` = `users_role`.`id`) 
        INNER JOIN `users_user_roles` ON (`users_role`.`id` = `users_user_roles`.`role_id`) 
        WHERE `users_user_roles`.`user_id` = <当前用户id> 
        ORDER BY `users_router`.`order_index` ASC;
    """
    print('反查-》查询用户能看哪些菜单',routers)


def org_flatten():
    """组织铺平"""

    qs = Org.objects.all().order_by('-order_index')  # 倒序查询集
    ser = OrgFlattenSerializer(instance=qs, many=True)  # 序列化器

    print(ser.data)


def org_tree():
    """组织树结构"""

    qs = Org.objects.all()
    ser = OrgTreeSerializer(instance=qs, many=True)  # 序列化器

    print(ser.data)


def view_modelSerializer():
    """查看模型序列化器"""
    from system_manage.org_manage_serializers import OrgTreeSerializer
    serializer = OrgTreeSerializer()

    print(serializer)

if __name__ == '__main__':
    # org_flatten()
    # org_tree()

    # view_modelSerializer()
    get_user_roles()