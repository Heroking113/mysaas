# -*- coding: utf-8 -*-
from config import RUN_VER
if RUN_VER == 'open':
    from blueapps.patch.settings_open_saas import *  # noqa
else:
    from blueapps.patch.settings_paas_services import *  # noqa

# 正式环境
RUN_MODE = 'PRODUCT'

# 只对正式环境日志级别进行配置，可以在这里修改
LOG_LEVEL = 'ERROR'

# APP本地静态资源目录
STATIC_URL = '/static/'

# 线上环境的静态文件路径
BK_STATIC_URL = STATIC_URL + 'dist'

# V2
# import logging
# logging.getLogger('root').setLevel('INFO')
# V3
# import logging
# logging.getLogger('app').setLevel('INFO')


# 正式环境数据库可以在这里配置

DATABASES.update(
    {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': '2017222072_prod_herokingfsaas',  # 数据库名
            'USER': 'yinxionwang',  # 数据库用户
            'PASSWORD': 'Heroking113.',  # 数据库密码
            'HOST': '10.0.2.8',  # 数据库主机
            'PORT': '3306',  # 数据库端口
        },
    }
)



