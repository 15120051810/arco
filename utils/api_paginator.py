from rest_framework.pagination import PageNumberPagination
from django.conf import settings
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from rest_framework.views import Response


# 分页（局部）：自定义分页器 局部
class PageNum(PageNumberPagination):
    # 查询字符串中代表每页返回数据数量的参数名, 默认值: None
    page_size_query_param = 'page_size'


def Paginators(objs, request, Serializer):
    """
    objs : 实体对象, queryset
    request : 请求对象
    Serializer : 对应实体对象的类
    page_size : 每页显示多少条数据
    page  ： 显示第几页数据
    total_count ：总共有多少条数据
    total ：总页数
    """
    try:
        page_size = int(request.GET.get('page_size', settings.REST_FRAMEWORK['PAGE_SIZE']))
        page = int(request.GET.get('page', 1))
    except (TypeError, ValueError):
        return Response(status=400)

    paginator = Paginator(objs, page_size)    # paginator对象
    total_count = paginator.count
    total = paginator.num_pages    # 总页数
    try:
        objs = paginator.page(page)
    except PageNotAnInteger:
        objs = paginator.page(1)
    except EmptyPage:
        objs = paginator.page(paginator.num_pages)
    serializer = Serializer(objs, many=True)    # 序列化操作
    return Response(
        data={
            'results': serializer.data,
            'page': page,
            'page_size': page_size,
            'total': total,
            'count': total_count
        }
    )
