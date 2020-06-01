# _*_ coding: utf-8 _*_

from __future__ import absolute_import, unicode_literals

import datetime

from blueapps.utils.logger import logger
from celery import task
from home_application.models import ScriptJobRecord
from celery.schedules import crontab
from celery.task import periodic_task

from home_application.models import ScriptSearch, FastExecuteScript


@task()
def async_handle_execute_script(client, kwargs):
    result = client.job.fast_execute_script(kwargs)
    script_job_record = ScriptJobRecord.objects.filter(pk=kwargs["record_id"])
    script_job_record.update(status=result["result"])
