"""
@Author   : liuxiangyu
@File     : logging_filters.py
@TIme     : 2025/5/21 15:12
@Software : PyCharm
@describe : 
"""


import logging
from middlemares.log_middleware import get_current_request

class UsernameIpLoggingFilter(logging.Filter):
    # def filter(self, record):
    #     user = get_current_user()
    #     # print('获取用户11111',user.username)
    #     record.username = user.username if user else 'anonymous'
    #
    #     return True

    def filter(self, record):
        request = get_current_request()
        if request:
            user = getattr(request, 'user', None)
            record.username = user.username if user and user.is_authenticated else 'Anonymous'
            record.ip = request.META.get('REMOTE_ADDR', '')
        else:
            record.username = 'N/A'
            record.ip = ''
        return True