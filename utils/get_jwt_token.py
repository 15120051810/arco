"""
@Author   : liuxiangyu
@File     : get_jwt_token.py
@TIme     : 2023/1/12 17:12
@Software : PyCharm
"""

from rest_framework_jwt.settings import api_settings

def get_token(user_info):

    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user_info)
    token = jwt_encode_handler(payload)

    return token