from .base import *

DEBUG = True

# mysql链接
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',  # 数据库主机127.0.0.1
        'PORT': 33307,  # 数据库端口，DOCKer搭建8.0
        'USER': 'root',  # 数据库用户名
        'PASSWORD': '515079',  # 数据库用户密码
        'NAME': 'arco',  # 数据库名字 docker搭建
        'CONN_MAX_AGE': 600,  # 保持连接 10 分钟
    },
}

# redis链接
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # "TIMEOUT": 300,  # 不传默认为300保留时间
        "LOCATION": "redis://127.0.0.1:6379/1",  # mac 搭建
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # Mimicing memcache behavior.
            # https://github.com/jazzband/django-redis#memcached-exceptions-behavior
            "IGNORE_EXCEPTIONS": True,
            # "PASSWORD":"515079",
            "MAX_ENTRIES": 300,  # 删除旧数据之前，允许在缓存中存放的最大数量，默认：300
        },
    }
}

# base后台token的 校验与登出
# BASE_CHECKTOKEN_URL = "http://test-admin-base-api.miaoshou.com/api/system/checkToken"
BASE_CHECKTOKEN_URL = "https://test-admin-base-api.miaoshou.com/api/system/getBigDataAppList"
BASE_CHECKLOGOUT_URL = "https://test-admin-base-api.miaoshou.com/api/system/checkLogOut"
