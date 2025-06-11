"""
@Author   : liuxiangyu
@File     : auth.py
@TIme     : 2024/6/11 17:49
@Software : PyCharm
"""
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from typing import Any, Dict, Optional, Type, TypeVar
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from django.contrib.auth.models import update_last_login


# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class TokenObtainPairSerializer(TokenObtainSerializer):
    """
    源码 copy过来作对比
    """
    token_class = RefreshToken

    # validate 中的 get_token 方法会调用 cls.token_class.for_user(user)
    # cls.token_class->RefreshToken 该类继承了 class RefreshToken(BlacklistMixin, Token):
    # BlacklistMixin 中方法for_user 会去给数据库添加一条token记录

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)

        refresh = self.get_token(self.user)
        print('refresh', refresh)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class MyTokenObtainPairSerializerDBTwo(TokenObtainPairSerializer):
    """
    继承 TokenObtainPairSerializer
    DBTwo 数据库会导致生产两条token记录
    """

    @classmethod
    def get_token(cls, user):
        """
        该函数的功能
        1 生成刷新令牌
        2 而刷新令牌又会用于生成视图的访问令牌
        """
        token = super().get_token(user)

        # print('啊啊啊啊1', type(token), token, user, type(user), dir(token))

        # Add custom claims
        # print('user.name', user.name)

        token['name'] = user.name
        # print('get_token-->',dir(token))
        return token

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        """
        super().validate(attrs) 中调用 get_token 产生第一条token记录
        自身 validate中又 调用 self.get_token 就会在数据库保存第二条token记录
        """
        try:
            old_data = super().validate(attrs)  # 必须验证，才可以有属性 user
            refresh = self.get_token(self.user)

            data = {'code': 200,
                    'msg': '登录成功成功',
                    'username': self.user.username,
                    'name': str(refresh['name']),
                    'refreshToken': str(refresh),
                    'token': str(refresh.access_token)
                    }
            return data
        except Exception as err:
            raise Exception(err)


class MyTokenObtainPairSerializer(TokenObtainSerializer):
    """
    不继承 TokenObtainPairSerializer
    直接重写 TokenObtainPairSerializer
    数据库只会有一份 token记录
    """
    token_class = RefreshToken

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        """
        自定义返回的格式
        """
        try:
            super().validate(attrs)  # 必须验证，才可以有属性 user
            refresh = self.get_token(self.user)  # refresh 是一个对象，不是字符串，不能直接放进 JSON

            # print('refresh', refresh, type(refresh),
            #       dir(refresh))  # <class 'rest_framework_simplejwt.tokens.RefreshToken'>

            if api_settings.UPDATE_LAST_LOGIN:
                update_last_login(None, self.user)

            data = {
                'username': self.user.username,
                'name': self.user.name,
                'refresh': str(refresh),  # 如果不使用str返回  "detail": "Object of type RefreshToken is not JSON serializable"
                'token': str(refresh.access_token)
            }

            login_info = {'code': 200,
                          'msg': '登录成功成功',
                          'ok': True,
                          'data': data
                          }
            return login_info
        except Exception as err:
            raise Exception(f'login error {err}')
