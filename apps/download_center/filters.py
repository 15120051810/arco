import django_filters

from download_center.models import DownLoadCenter


class DownLoadCenterFilter(django_filters.rest_framework.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='文件名称')
    create_user = django_filters.CharFilter(field_name='create_user__name', lookup_expr='icontains')
    create_time = django_filters.DateFromToRangeFilter()

    class Meta:
        model = DownLoadCenter
        fields = ('name', "create_user__name", "create_time")
