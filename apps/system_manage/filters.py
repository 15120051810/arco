import django_filters
from users.models import Router, User, Org, Role


class OrgFilter(django_filters.rest_framework.FilterSet):
    org_id = django_filters.CharFilter(field_name='org_id', lookup_expr='exact', label='组织id')
    org_name = django_filters.CharFilter(field_name='org_name', label='组织名称')

    class Meta:
        model = Org
        fields = ['org_name','org_id']


class UserFilter(django_filters.rest_framework.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='用户名称')

    class Meta:
        model = User
        fields = ['name']


class RouterFilter(django_filters.rest_framework.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='菜单标题')

    class Meta:
        model = Router
        fields = ['title']

class RoleFilter(django_filters.rest_framework.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='角色名称')

    class Meta:
        model = Role
        fields = ['name']

