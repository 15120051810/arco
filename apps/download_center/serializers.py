import pytz
from rest_framework import serializers

from download_center.models import DownLoadCenter


class DownLoadCenterSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', default_timezone=pytz.timezone('Asia/Shanghai'))
    status = serializers.CharField(source='get_status_display')
    create_user = serializers.CharField(source='create_user.name')

    class Meta:
        model = DownLoadCenter
        fields = '__all__'
