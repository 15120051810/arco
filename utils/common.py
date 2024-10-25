"""
@Author   : yuanfei
@File     : common.py
@TIme     : 2023/1/11 20:09
@Software : PyCharm
"""
import re

import logging
import itertools
import pandas as pd
import requests
import json
import uuid
from functools import wraps
from users.models import Org
from django.db.models import Q
from download_center.models import DownLoadCenter
from django.conf import settings
from log.models import ViewLog
from system_manage.org_manage_serializers import OrgTreeSerializer
from datetime import datetime, timedelta

BASE_KEYWORD = "big_data_app_product"
USER_DEFAULT_PASSWORD = 'Miao13456'

logger = logging.getLogger("arco")


def tree_to_list(tree_data, keys):
    _result = []

    def inner(ele):
        if isinstance(keys, str):
            _result.append(ele[keys])
        elif isinstance(keys, list):
            tmp = {}
            for i in keys:
                tmp[i] = ele[i] if ele[i] is not None else ""
            _result.append(tmp)

        for i in ele['children']:
            inner(i)

    inner(tree_data)
    return _result


def get_user_org(request, is_large_region=False):
    """
        获取用户下面的所有机构（大区 -> 机构）
    """
    user_org_list = request.user.orgs.all()
    logger.info(f"当前用户所在机构名称 ---> {user_org_list}")

    org_id_list = []
    for org in user_org_list:
        # 如果是门店直接添加
        # if org.org_type == 6:
        #     org_id_list.append({"org_id": org.org_id, "org_name": org.org_name, 'org_type': org.org_type})

        # 如果是 圆心科技 那就直接查出来所有的门店（不包括电商）
        if org.org_name == "圆心科技":
            org_list = Org.objects.exclude(Q(is_ds=1) | Q(state=0))
            org_list = [
                {"org_id": org.org_id, "org_name": org.org_name, 'org_type': org.org_type if org.org_type else ""}
                for org in org_list]
            org_id_list.extend(org_list)
        # 如果是电商或者电商下的门店 先查出来机构名称
        elif org.is_ds == 1:
            org_name_list = tree_to_list(OrgTreeSerializer(org).data, 'org_name')
            org_list = Org.objects.exclude(Q(is_ds=1) | Q(state=0)).filter(org_name__in=org_name_list)
            org_list = [
                {"org_id": org.org_id, "org_name": org.org_name, 'org_type': org.org_type if org.org_type else ""}
                for org in org_list]
            org_id_list.extend(org_list)
        else:
            org_ser = OrgTreeSerializer(org)
            res = tree_to_list(org_ser.data, ['org_id', 'org_name', 'org_type'])
            org_id_list.extend(res)

    # 同一个用户在电商组织下有个机构1，又在华南组织下有个机构1，导致机构1数据重复
    df = pd.DataFrame(org_id_list)
    df.drop_duplicates(inplace=True)
    org_list = df.to_dict(orient='records')
    return org_list


def check_params(params):
    pattern = re.compile(
        r"(\bselect\b|\bupdate\b|\band\b|\bor\b|\bdelete\b|\binsert\b"
        r"|\btruncate\b|\bchar\b|\bsubstr\b|\bascii\b|\bdeclare\b|\bexec\b"
        r"|\bcount\b|\bmaster\b|\binto\b|\bdrop\b|\bexecute\b)"
    )

    # 检查请求参数是否包含潜在的 SQL 注入问题
    for key, value in params.items():
        s = str(value)
        if pattern.search(s):
            # 如果发现潜在的 SQL 注入问题，抛出自定义异常
            raise Exception('Potential SQL injection detected in the request parameters.')


def viewlog(action, page_desc):
    def my_decorator(func):
        @wraps(func)
        def wrapper(_, request, *args, **kwargs):
            m = request.method
            query_params = request.query_params if m == 'GET' else request.data
            logger.info(f"{request.user.username} {page_desc} {m} 参数->{query_params}")
            check_params(query_params)

            _ip = request.META.get('REMOTE_ADDR') if request.META.get(
                'REMOTE_ADDR') != '127.0.0.1' else request.META.get('HTTP_X_FORWARDED_FOR')

            ViewLog.objects.log_handler(request.user, action, page_desc, request.path, _ip)
            response = func(_, request, *args, **kwargs)
            return response

        return wrapper

    return my_decorator


def async_download(request, sql, headers, file_name):
    """
        异步下载
    """
    params = {
        "taskId": str(uuid.uuid4()),
        "downloadSql": sql,
        "callbackUrl": settings.CALLBACK_URL,
        "predictNum": 0,
        "downloadSource": "erp",
        "metaType": 1,
        "metaFlag": "impala_prod",
        "metaWorkspace": "bdp",
        "headers": headers,
        "fileName": file_name,
        "methodType": 1
    }

    d_headers = {'Connection': 'close'}
    logger.info(f"请求导出接口：http://{settings.DOWNLOAD_URL}/download/create 请求头：{d_headers}")
    response = requests.post(url=f"http://{settings.DOWNLOAD_URL}/download/create", headers=d_headers, json=params)
    logger.info(f"导出接口返回：{response.status_code}")

    if response.status_code == requests.codes.ok:
        resp = response.text
        data = json.loads(resp)
        dlc = DownLoadCenter()
        dlc.name = data['data']["name"]
        dlc.create_user = request.user
        dlc.task_id = data['data']["taskId"]
        dlc.format = "excel"
        dlc.save()

    return response


def get_appoint_parent(org_obj, org_type):
    if org_obj.org_type == org_type:
        return org_obj
    return get_appoint_parent(org_obj.parent, org_type)


def paginate(data, page_size, page_number):
    start_index = (page_number - 1) * page_size
    end_index = page_number * page_size
    return data[start_index:end_index]


def give_org_return_shop(org_id):
    org_obj = Org.objects.filter(org_id=org_id).first()

    if org_obj.org_name == '圆心科技':
        return [{'org_id': org_obj.org_id, "org_name": org_obj.org_name, "org_type": org_obj.org_type} for org_obj in
                Org.objects.filter(org_type=6)]

    resp_tree = OrgTreeSerializer(org_obj)
    tmp = list(map(lambda x: tree_to_list(x, ['org_id', 'org_name', 'org_type']), [resp_tree.data]))
    org_list = list(itertools.chain(*tmp))
    org_list = [i for i in org_list if i['org_id'] != org_id and i['org_type'] == 6] if org_list else []
    org_obj.org_type == 6 and org_list.append(
        {'org_id': org_obj.org_id, "org_name": org_obj.org_name, "org_type": org_obj.org_type})
    return org_list


list_to_tuple = lambda x: str(x).replace('[', '(').replace(']', ')')


def generate_continuous_times(start_time_str, end_time_str):
    """
    生成连续 时间
    :param start_time_str: 起始时间
    :param end_time_str: 结束时间
    :return:
    """
    start_time = datetime.strptime(start_time_str, '%Y-%m-%d')
    end_time = datetime.strptime(end_time_str, '%Y-%m-%d')

    continuous_times = []
    current_time = start_time
    while current_time <= end_time:
        continuous_times.append(current_time.strftime('%Y-%m-%d'))
        current_time += timedelta(days=1)

    return continuous_times


def change_char(s, index, new_char):
    if index < 0 or index >= len(s):
        raise IndexError("Index out of range")
    return s[:index] + new_char + s[index + 1:]


def get_weeks_in_range(start_date_str, end_date_str):
    """基于时间范围获取 周范围"""
    from datetime import datetime, timedelta

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    current_date = start_date

    weeks = []

    while current_date <= end_date:
        year, week_num, _ = current_date.isocalendar()
        week_start = current_date - timedelta(days=current_date.weekday())

        weeks.append({"title": f"{year}-{week_num}周", "dataIndex": week_start.strftime("%Y-%m-%d"), "width": 120})
        current_date += timedelta(days=7)

    return weeks


def get_months_in_range(start_month_str, end_month_str):
    """基于起始月生产连续的月"""
    date_range = pd.date_range(start=start_month_str, end=end_month_str, freq='MS')
    months = date_range.strftime("%Y-%m").tolist()

    tmp = [{"title": f"{i}月", "dataIndex": i, "width": 120} for i in months]

    return tmp
