"""
@Author   : liuxiangyu
@File     : middleware.py
@TIme     : 2023/1/11 20:12
@Software : PyCharm
"""

from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.state import token_backend
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse


class CheckTokenMiddleware(MiddlewareMixin):
    """校验token中间件"""
    def process_request(self, request):
        """
        处理请求前
        在 Django 调用视图之前调用。应返回 None 或 HttpResponse 对象。
        """
        # print("Request is being processed")

        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                # Decode the token and verify its validity 解码令牌并验证其有效性
                access_token = AccessToken(token)
                # print调用了 AccessToken.__repr__方法
                # print('打印的是AccessToken类中init方法已经验证玩后的token,调用了__repr__方法')

                # If token is valid, store the user information in the request
                request.user_id = access_token['user_id']
            except (TokenError, InvalidToken):
                data = {'code': '300', 'msg': 'Token is invalid or expired'}
                return JsonResponse(data=data, status=status.HTTP_202_ACCEPTED)
        return None

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        在 Django 调用视图之前调用，但在 process_request 之后调用。应返回 None 或 HttpResponse
        :param request:
        :param view_func:
        :param view_args:
        :param view_kwargs:
        :return:
        """
        # print("View is being processed")
        return None

    def process_response(self, request, response):
        """处理响应前"""
        # print("Response is being processed")
        return response
