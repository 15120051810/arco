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

    view_modelSerializer()