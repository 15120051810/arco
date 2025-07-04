"""
@Author   : liuxiangyu
@File     : dj_table.view.py
@TIme     : 2024/3/13 17:35
@Software : PyCharm
"""
import logging

from rest_framework.views import APIView
from rest_framework.response import Response

logger = logging.getLogger('arco')


class DJTableBaseUse(APIView):
    """
    表格基本使用
    """

    def get(self, request):
        """
        """
        logger.info(f"request {request}")
        data = [{
            "key": '1',
            "name": 'Jane Doe',
            "salary": 23000,
            "address": '32 Park Road, London',
            "email": 'jane.doe@example.com'
        }, {
            "key": '2',
            "name": 'Alisa Ross',
            "salary": 25000,
            "address": '35 Park Road, London',
            "email": 'alisa.ross@example.com'
        }, {
            "key": '3',
            "name": 'Kevin Sandra',
            "salary": 22000,
            "address": '31 Park Road, London',
            "email": 'kevin.sandra@example.com'
        }, {
            "key": '4',
            "name": 'Ed Hellen',
            "salary": 17000,
            "address": '42 Park Road, London',
            "email": 'ed.hellen@example.com'
        }, {
            "key": '5',
            "name": 'William Smith',
            "salary": 27000,
            "address": '62 Park Road, London',
            "email": 'william.smith@example.com'
        }]

        return Response(data=data)
