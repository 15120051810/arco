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
import datetime


class ContentDataView(APIView):
    """
    表格基本使用
    """

    def get(self, request):
        """
        """
        logger.info(f"request {request}")

        data = []
        presetData = [58, 81, 53, 90, 64, 88, 49, 79]

        for i, v in enumerate(presetData, 0):
            day = (datetime.datetime.today() + datetime.timedelta(days=i)).strftime('%Y-%m-%d')

            t = {
                "x": day,
                "y": presetData[i]
            }

            data.append(t)

        res = {
            "data": data,
            "status": 'ok',
            "msg": '请求成功',
            "code": 20000,
        }
        return Response(data=res)
