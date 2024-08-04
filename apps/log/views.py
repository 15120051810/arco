import logging
import datetime
from rest_framework.views import APIView, Response
from utils.permissions import APIPermission
from log.query_api import get_chunk_data, get_line_data, get_page_top10, get_person_top10, get_all
from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger('acro')


class BrowsingLogKeyIndexAPIView(APIView):
    permission_classes = [IsAuthenticated, APIPermission]

    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        chunk_data = get_chunk_data(start_date, end_date)
        return Response(chunk_data)


class MetricTrendAPIView(APIView):
    permission_classes = [IsAuthenticated, APIPermission]

    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        metric = request.GET.get('sign')
        data = get_line_data(start_date, end_date, metric)
        return Response(data)


class PageTop10Detail(APIView):
    """
        访问最多页面 TOP10
    """
    permission_classes = [IsAuthenticated, APIPermission]

    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        keyword = request.GET.get('page_keyword')
        result = get_page_top10(start_date, end_date, keyword)
        return Response(result)


class PersonTop10Detail(APIView):
    """
        访问最多的人 TOP10
    """
    permission_classes = [IsAuthenticated, APIPermission]

    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        keyword = request.GET.get('person_keyword')
        result = get_person_top10(start_date, end_date, keyword)
        return Response(result)


class AllDetail(APIView):
    """
        全部详情
    """
    permission_classes = [IsAuthenticated, APIPermission]

    def get(self, request):
        page = int(request.GET.get('page'))
        page_size = int(request.GET.get('page_size'))
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        keyword = request.GET.get('keyword')
        action = request.GET.get('action')
        result = get_all(start_date, end_date, keyword, action, page, page_size)
        return Response(result)

