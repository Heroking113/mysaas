# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from config import RUN_VER


if RUN_VER == 'open':
    from blueapps.patch.settings_open_saas import *  # noqa
else:
    from blueapps.patch.settings_paas_services import *  # noqa

# 本地开发环境
RUN_MODE = 'DEVELOP'

# APP本地静态资源目录
STATIC_URL = '/static/'

# BK_STATIC_URL = STATIC_URL + "dist/"
# APP静态资源目录url
# REMOTE_STATIC_URL = '%sremote/' % STATIC_URL

# Celery 消息队列设置 RabbitMQ
# BROKER_URL = 'amqp://guest:guest@localhost:5672//'
# # # Celery 消息队列设置 Redis
# # # BROKER_URL = 'redis://localhost:6379/0'
# BACKEND_URL = 'redis://localhost:6379/1'
# BROKER_URL = 'redis://localhost:6379/2'
# Celery backend设置 Redis
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/3'
BROKER_URL = 'amqp://'
CELERY_RESULT_BACKEND = 'amqp://'

# celery时区设置，使用settings中TIME_ZONE同样的时区
# CELERY_TIMEZONE = TIME_ZONE

DEBUG = True

# 本地开发数据库设置
# USE FOLLOWING SQL TO CREATE THE DATABASE NAMED APP_CODE
# SQL: CREATE DATABASE `framework_py` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci; # noqa: E501
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'herokingfsaas',
        'USER': 'root',
        'PASSWORD': 'Heroking113.',
        'HOST': 'localhost',
        'PORT': '3306',
    },
}

# 多人开发时，无法共享的本地配置可以放到新建的 local_settings.py 文件中
# 并且把 local_settings.py 加入版本管理忽略文件中
try:
    from local_settings import *  # noqa
except ImportError:
    pass

BK_STATIC_URL = STATIC_URL + 'dist/'
