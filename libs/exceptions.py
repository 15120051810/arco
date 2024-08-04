"""
@Author   : liuxiangyu
@File     : exceptions.py
@TIme     : 2023/1/12 14:47
@Software : PyCharm
"""


import logging
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import exception_handler as drf_exception_handler

logger = logging.getLogger('yxdp')



def exception_handler(exc, context):
    response = drf_exception_handler(exc, context)

    if response is None:
        view = context['view']
        logger.exception(f"{view}; {exc} ;{context}")
        response = Response({'message': 'Server error', "view": str(view), 'errInfo': f'{exc}'},
                            status=status.HTTP_507_INSUFFICIENT_STORAGE)

    return response
