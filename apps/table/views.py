import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import Router
from users.serializers import RouerFlattenSerializer
import pandas as pd

logger = logging.getLogger('arco')


class TableColumnsPermisson(APIView):
    """
    表格基本使用 - 后端控制列权限
    """

    def get(self, request):
        """
        基于不同的权限返回不同的列数据
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

        questy = Router.objects.filter(roles__role_users=self.request.user, type=2).distinct()
        permisson = [i['keyword'] for i in RouerFlattenSerializer(instance=questy, many=True).data]

        df = pd.DataFrame(data)

        if 'table:table_columns_salary' not in permisson:
            df_new = df.drop(columns='salary')
        else:
            df_new = df

        data = df_new.to_dict(orient='records')

        return Response(data=data)
