from rest_framework import routers
from django.urls import path

from .views import TableColumnsPermisson

app_name = 'table'

urlpatterns = [
    path('table/columns_permisson', TableColumnsPermisson.as_view()),
]

