"""
@Author   : yuanfei liuxiangyu
@File     : common_view.py
@TIme     : 2023/7/28 15:06
@Software : PyCharm
"""
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response
from utils.permissions import APIPermission
from rest_framework.exceptions import APIException
import re
import datetime
import logging
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

from django.conf import settings

logger = logging.getLogger("arco")


class QueryBigDataTool:
    """
    查询大数据接口工具
    1 查询接口
    2 导出接口
    """

    def query_one(self, sql, is_fetchall=False):
        """
        单独查询一个sql
        :param sql: sql语句
        :param is_fetchall: 是否返回
        :return:
        """

        response = requests.post(url=settings.BIG_DATA_API, json={"sql": sql, "pool": "yxdp"})

        if response.status_code != requests.codes.ok:
            raise Exception(f'query big data error，not ok!! errInfo: {response.json()}')

        result = response.json()
        if result['code'] != 20000:
            raise Exception(f'query big data error，not 20000!!, errInfo {response.json()}')

        query_res = result['data'] if is_fetchall else result['data'][0]

        return query_res

    def query_many(self, sign, sql, is_fetchall=False):
        """
        用于并发查询查询多个sql
        :param sql: sql语句
        :param is_fetchall: 是否返回
        :param sign: 查询的那个业务
        :return:
        """
        logger.info(f"查询业务 {sign}")

        state, query_res = True, [] if is_fetchall else {}

        try:
            query_res = self.query_one(sql, is_fetchall)
        except Exception as err:
            state = False
            logger.error(f"{sign} 接口出错 {err}")

        return sign, state, query_res

    def query_concurrent(self, yw_name, sql_list):
        """
        并发查询接口
        yw_name: 那块的业务查询
        sql_list: [{'sign':'',"sql":sql语句,'is_fetchall':bool},....]
        """

        results = {}

        with ThreadPoolExecutor(max_workers=len(sql_list), thread_name_prefix=f'{yw_name} 子线程') as ex:
            tasks = [ex.submit(self.query_many, **_s) for _s in sql_list]
            for i in as_completed(tasks):
                sign, state, query_res = i.result()

                results.update({sign: query_res})

            return results


class QueryBaseView(APIView):
    permission_classes = [IsAuthenticated, APIPermission]

    @staticmethod
    def big_data_query_interface(sql, is_fetchall=False):
        status = 200
        query_res = [] if is_fetchall else {}
        try:
            response = requests.post(url='http://api.bdp.miaoshou.com/impala/query/selectList',
                                     json={"sql": sql, "pool": "yxdp"})
            if response.status_code == requests.codes.ok:
                result = response.json()
                if result['code'] == 20000:
                    query_res = result['data'] if is_fetchall else result['data'][0] if len(
                        result['data']) == 1 else query_res
                else:
                    logger.error(f"查询错误：{response.json()}")
                    status = 500
                    query_res = response.json()
        except Exception as e:
            logger.error(f'查询接口错误：{e}')
            status = 500
            query_res = e
        finally:
            return status, query_res

    def query_get_data(self, count_sql, data_sql):
        status = 200
        base_data = {"total": 0, "data": []}
        doc = self.__doc__

        logger.info(f"{doc} 开始查 count_sql {count_sql}")
        status, query_res = self.big_data_query_interface(count_sql, is_fetchall=False)
        if status == 500:
            return status, query_res
        elif not query_res.get('num', 0):
            return status, base_data
        else:
            base_data['total'] = query_res['num']

        logger.info(f"{doc} 开始查 data_sql {data_sql}")
        status, query_res = self.big_data_query_interface(data_sql, is_fetchall=True)
        if status == 500:
            return status, query_res
        else:
            base_data['data'] = query_res

        return status, base_data


class SQLInjectionException(APIException):
    status_code = 400
    default_detail = "Potential SQL injection detected in the request parameters."
    default_code = "invalid_parameters"


class SQLInjectionCheckMixin:
    """
    自定义 Django REST Framework 基类，用于检测请求参数中的潜在 SQL 注入问题。
    """
    # 定义正则表达式模式，用于检测潜在的 SQL 注入问题
    pattern = re.compile(
        r"(?:')|(?:--)|(?:/\*(?:.|[\n\r])*?\*/)"
        r"|(\bselect\b|\bupdate\b|\band\b|\bor\b|\bdelete\b|\binsert\b"
        r"|\btruncate\b|\bchar\b|\bsubstr\b|\bascii\b|\bdeclare\b|\bexec\b"
        r"|\bcount\b|\bmaster\b|\binto\b|\bdrop\b|\bexecute\b)"
        r"|(\*|;|\+|'|%)"
    )

    def check_params(self, params):
        # 检查请求参数是否包含潜在的 SQL 注入问题
        for key, value in params.items():
            if isinstance(value, str):
                if self.pattern.search(value):
                    # 如果发现潜在的 SQL 注入问题，抛出自定义异常
                    raise SQLInjectionException()


if __name__ == '__main__':
    obj = QueryBigDataTool()
