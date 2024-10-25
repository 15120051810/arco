from rest_framework import routers
from django.urls import path

from .workplace_view import ContentDataView
from .dj_table_view import DJTableBaseUse

app_name = 'arco_demo'

urlpatterns = [
    path('dashboard/content-data', ContentDataView.as_view()),
    path('dj_tables/base_use', DJTableBaseUse.as_view()),
]

