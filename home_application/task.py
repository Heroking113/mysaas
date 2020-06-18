# _*_ coding: utf-8 _*_
from __future__ import absolute_import, unicode_literals

from celery import Celery
from celery.task import task
from celery.schedules import crontab

from blueapps.utils.logger import logger_celery as logger

from home_application.models import MissionRecord


app = Celery('tasks', backend='rpc://', broker='amqp://guest@localhost//')


@task
def async_handle_execute_script(client, kwargs, record_id):
    print("111")
    try:
        result = client.job.fast_execute_script(kwargs)
    except Exception as e:
        logger.error(e)
        MissionRecord.objects.filter(pk=record_id).update(status="fail")
    else:
        if result["result"]:
            MissionRecord.objects.filter(pk=record_id).update(status="success")
        else:
            MissionRecord.objects.filter(pk=record_id).update(status="fail")
