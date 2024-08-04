import urllib
import logging
from log.models import ViewLog
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, filters
from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.db.models import Q
from download_center.serializers import DownLoadCenterSerializer

from download_center.filters import DownLoadCenterFilter
from download_center.models import DownLoadCenter

logger = logging.getLogger('yxdp')

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = "page"
    # max_page_size = 100


class CallBackView(APIView):
    permission_classes = []

    def get(self, request):
        try:
            logger.info(f"回调参数为 ---> {request.GET}")
            uid = request.GET.get("id")
            status = request.GET.get("code")
            data_number = request.GET.get("recordNum")
            data_size = request.GET.get("fileSize")

            download_obj = DownLoadCenter.objects.get(task_id=uid)
            download_obj.status = status
            if data_number:
                download_obj.data_number = data_number
            if data_size:
                download_obj.data_size = data_size

            download_link = request.GET.get("downloadExcelPath")
            if download_link:
                download_link = urllib.parse.unquote(download_link)
            if download_link and download_link.startswith("http:"):
                download_link = download_link.replace("http", "https")
            if download_link:
                download_obj.download_link = download_link
            download_obj.save()
        except Exception as e:
            logger.info(f"回调失败错误原因：-->{e}")
            return JsonResponse({"code": 9000, "message": "系统异常", "success": "no"})
        return JsonResponse({"code": 0, "message": "感谢回调", "success": "ok"})


class DownLoadCenterViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = DownLoadCenter.objects.all().order_by('-create_time')
    serializer_class = DownLoadCenterSerializer
    pagination_class = CustomPagination
    authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = DownLoadCenterFilter

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        if not self.request.user.is_superuser:
            queryset = queryset.filter(create_user=self.request.user)
        return queryset

    def get_queryset(self):
        ViewLog.objects.log_handler(self.request.user, 'V', '下载中心', self.request.path,
                                    self.request.META.get("HTTP_X_FORWARDED_FOR") if self.request.META.get(
                                        "HTTP_X_FORWARDED_FOR") else self.request.META.get('REMOTE_ADDR'))
        return super(DownLoadCenterViewSet, self).get_queryset()
