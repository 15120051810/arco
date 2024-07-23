
from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',  # 数据库主机127.0.0.1
        'PORT': 33307,  # 数据库端口，DOCKer搭建8.0
        'USER': 'root',  # 数据库用户名
        'PASSWORD': '515079',  # 数据库用户密码
        'NAME': 'arco'  # 数据库名字 docker搭建
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "TIMEOUT": 300,  # 不传默认为300保留时间
        "LOCATION": "redis://127.0.0.1:6379/8",  # mac 搭建
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # Mimicing memcache behavior.
            # https://github.com/jazzband/django-redis#memcached-exceptions-behavior
            "IGNORE_EXCEPTIONS": True,
            "MAX_ENTRIES": 300,  # 删除旧数据之前，允许在缓存中存放的最大数量，默认：300
        },
    }

}
