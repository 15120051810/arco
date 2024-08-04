import django_filters
from users.models import Router, Api, Org, Role


class OrgInfoFilter(django_filters.rest_framework.FilterSet):
    org_name = django_filters.CharFilter(field_name='org_name', label='组织名称')
    org_type = django_filters.CharFilter(field_name='org_type', label='组织类型')

    class Meta:
        model = Org
        fields = ['org_name', 'org_type']


class RoleInfoFilter(django_filters.rest_framework.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='角色名称')

    class Meta:
        model = Role
        fields = ['name']


class RouterInfoFilter(django_filters.rest_framework.FilterSet):
    title = django_filters.CharFilter(field_name='title', label='页面标题')
    system = django_filters.NumberFilter(field_name='system', label='系统类型')

    class Meta:
        model = Router
        fields = ['title', 'system']


class ApiInfoFilter(django_filters.rest_framework.FilterSet):
    name = django_filters.CharFilter(field_name='name', label='API名称')

    class Meta:
        model = Api
        fields = ['name']
