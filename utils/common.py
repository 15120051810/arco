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


