"""
@Author   : liuxiangyu
@File     : log_middleware.py
@TIme     : 2025/5/21 15:08
@Software : PyCharm
@describe : 
"""

import threading

_thread_locals = threading.local()


def set_current_request(request):
    _thread_locals.request = request

def get_current_request():
    return getattr(_thread_locals, 'request', None)

# def get_current_user():
#     request = getattr(_thread_locals, 'request', None)
#
#     # print("请求方法:", request.method)
#     # print("请求路径:", request.path)
#     # print("GET 参数:", request.GET)
#     # print("POST 参数:", request.POST)
#     # print("请求头:", dict(request.headers))
#     # print("当前请求用户:", request.user)
#     # print("当前请求用户认证状态:", request.user.is_authenticated)
#     if request:
#         user = getattr(request, 'user', None)
#         if user and user.is_authenticated:
#             return user
#     return None


class ThreadLocalMiddleware:
    """将当前 request 注入 thread local，供日志中使用"""
    def __init__(self, get_response):
        # print('get_response', get_response)

        self.get_response = get_response # 保留视图调用接口


    def __call__(self, request):
        """请求前逻辑"""
        # print("请求方法:", request.method)
        # print("请求路径:", request.path)
        # print("GET 参数:", request.GET)
        # print("POST 参数:", request.POST)
        # print("请求头:", dict(request.headers))
        # print("请求用户:", request.user)

        set_current_request(request)

        response = self.get_response(request)
        return response


