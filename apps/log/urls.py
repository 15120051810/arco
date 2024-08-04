"""
@Author   : yuanfei
@File     : urls.py
@TIme     : 2023/4/06 16:53
@Software : PyCharm
"""
from django.urls import path
from log.views import BrowsingLogKeyIndexAPIView, MetricTrendAPIView, PageTop10Detail, PersonTop10Detail, AllDetail

app_name = "log"

urlpatterns = [
    path('browsing_log_key_index/', BrowsingLogKeyIndexAPIView.as_view()),  # 浏览日志
    path('browsing_log_metric_trend/', MetricTrendAPIView.as_view()),  # 趋势图
    path('browsing_log_page_top10/', PageTop10Detail.as_view()),  # 访问最多的页面
    path('browsing_log_person_top10/', PersonTop10Detail.as_view()),  # 访问最多的人
    path('browsing_log_all_detail/', AllDetail.as_view()),  # 访问最多的人

]
