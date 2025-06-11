"""
@Author   : liuxiangyu
@File     : get_jwt_token.py
@TIme     : 2023/1/12 17:12
@Software : PyCharm
"""

from rest_framework_simplejwt.tokens import RefreshToken


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'token': str(refresh.access_token),
    }
