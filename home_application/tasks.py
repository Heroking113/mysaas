# _*_ coding: utf-8 _*_
from __future__ import absolute_import, unicode_literals

import json
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab
from celery.task import task, periodic_task

from blueking.component.client import ComponentClient
from blueapps.utils.logger import logger_celery as logger


from home_application.utils import update_business_db, update_host_db
from home_application.models import MissionRecord, BkToken, QueryParams

UNAHTHENTICATED_CODE = 1306000
CLIENT = ComponentClient(
        app_code="herokingfsaas",
        app_secret="d9664192-989a-424e-b0e6-5acb404fee2d",
        common_args={"bk_token": BkToken.objects.first().bk_token}
    )


class DataRange(object):
    START = 0
    LIMIT = 200


@periodic_task(run_every=crontab(minute=30))
def get_cc_businesses():
    """调用第三方接口，获取业务信息
       每30分钟执行1次
    """
    kwargs = {
        "page": {
            "start": DataRange.START,
            "limit": DataRange.LIMIT
        }
    }

    try:
        result = CLIENT.cc.search_business(kwargs)
    except Exception as e:
        logger.error("home_application.tasks, 调用client.cc.search_business接口失败{}".format(e))
        return
    if not result["result"]:
        # 记录日志，退出celery进程
        logger.warn("用户信息失效, 请先登录应用!")
        return
    to_business_db_data = result["data"]["info"]
    # 异步执行查询主机信息的任务
    for item in to_business_db_data:
        bk_biz_id = item.get("bk_biz_id", "")
        get_cc_hosts.delay(bk_biz_id)

    # 更新业务信息表
    update_business_db(to_business_db_data)


@task
def get_cc_hosts(bk_biz_id=None):
    """根据bk_biz_id调用第三方接口，获取对应业务下的主机信息
    """
    kwargs = {
        "page": {
            "start": DataRange.START,
            "limit": DataRange.LIMIT
        }
    }
    if bk_biz_id:
        kwargs["bk_biz_id"] = bk_biz_id
    try:
        host_res = CLIENT.cc.search_host(kwargs)
    except Exception as e:
        logger.error("home_application.tasks, 调用client.cc.search_host接口失败{}".format(e))
        return

    # 更新主机信息表
    update_host_db(host_res["data"]["info"], bk_biz_id)


@task
def async_handle_execute_script(kwargs, record_id):
    """异步执行脚本任务
    """
    try:
        result = CLIENT.job.fast_execute_script(kwargs)
    except Exception:
        logger.error("home_application.tasks, client.job.fast_execute_script接口执行失败 "
                     "kwargs={kwargs}, result={result}".format(kwargs=kwargs, result=result))
        MissionRecord.objects.filter(pk=record_id).update(status="fail")
        return

    if result["result"]:
        job_instance_id = result["data"]["job_instance_id"]
        MissionRecord.objects.filter(pk=record_id).update(job_instance_id=job_instance_id, status="2")
        QueryParams.objects.create(
            bk_biz_id=kwargs.get("bk_biz_id", ""),
            job_instance_id=job_instance_id,
            record_id=record_id
        )
    else:
        if result["code"] == UNAHTHENTICATED_CODE:
            MissionRecord.objects.filter(pk=record_id).update(status="13")
            logger.error("用户认证信息失效，请重新登陆.")
        else:
            MissionRecord.objects.filter(pk=record_id).update(status="4")
            logger.error("home_application.tasks, 调用client.job.fast_execute_script接口失败 "
                         "kwargs={kwargs}, result={result}".format(kwargs=kwargs, result=result))


@periodic_task(run_every=crontab())
def get_job_status():
    querysets = QueryParams.objects.all()
    for item in querysets:
        kwargs = {
            "bk_biz_id": item.bk_biz_id,
            "job_instance_id": item.job_instance_id
        }
        record_id = item.record_id
        result = CLIENT.job.get_job_instance_status(kwargs)
        if result["result"] and result["data"]["is_finished"]:
            status = result["data"]["job_instance"]["status"]
            MissionRecord.objects.filter(pk=record_id).update(status=status)
