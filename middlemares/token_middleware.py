"""
@Author   : liuxiangyu
@File     : middleware.py
@TIme     : 2023/1/11 20:12
@Software : PyCharm
"""

import logging
import requests
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.state import token_backend
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

logger = logging.getLogger('arco')


class CheckTokenMiddleware(MiddlewareMixin):
    """校验token中间件"""

    def process_request(self, request):
        """
        处理请求前
        在 Django 调用视图之前调用。应返回 None 或 HttpResponse 对象。
        """
        # print("Request is being processed")

        auth_header_base_token = request.headers.get('BaseToken')
        logger.info(f"auth_header_base_token_--->{auth_header_base_token}")
        if auth_header_base_token:
            try:
                res = requests.post(url=settings.BASE_CHECKTOKEN_URL,
                                    data={'token': auth_header_base_token, "keyword": settings.BASE_KEYWORD}).json()
                if res['code'] != 200:
                    logger.info(f'base_token 过期')
                    data = {'code': '401', 'msg': 'base_token is invalid or expired'}
                    return JsonResponse(data=data, status=status.HTTP_401_UNAUTHORIZED)
            except (TokenError, InvalidToken):
                data = {'code': '300', 'msg': '校验base_token时失败'}
                return JsonResponse(data=data, status=status.HTTP_202_ACCEPTED)
        return None

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        请求进入视图前，可进行权限、认证判断
        在 Django 调用视图之前调用，但在 process_request 之后调用。应返回 None 或 HttpResponse
        :param request:
        :param view_func:
        :param view_args:
        :param view_kwargs:
        :return:
        """
        # print("View is being processed")
        return None

    def process_exception(self, request, exception):
        # 异常统一处理
        logger.exception(f"发生异常: {exception}")
        return JsonResponse({
            "code": 500,
            "msg": "服务器内部错误",
            "detail": str(exception)
        }, status=500)

    def process_response(self, request, response):
        """返回前，可做日志、包装返回体等"""
        logger.info(f"响应状态: {response.status_code} | 路径: {request.path}")
        return response

    def get_client_ip(self, request):
        # 获取客户端 IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
