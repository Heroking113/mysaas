# _*_ coding: utf-8 _*_
from __future__ import absolute_import, unicode_literals

import time

from celery.task import task

from blueapps.utils.logger import logger_celery as logger

from home_application.utils import update_business_db, update_host_db, get_client
from home_application.models import MissionRecord, QueryParams

UNAHTHENTICATED_CODE = 1306000


class DataRange(object):
    START = 0
    LIMIT = 200


@task
def get_cc_businesses(bk_token):
    """调用第三方接口，获取业务信息
       每30分钟执行1次
    """
    kwargs = {
        "page": {
            "start": DataRange.START,
            "limit": DataRange.LIMIT
        }
    }
    if not bk_token:
        logger.warn("看起来您未登陆应用，请登陆应用")
    try:
        client = get_client(bk_token)
        result = client.cc.search_business(kwargs)
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
        get_cc_hosts.delay(bk_token, bk_biz_id)

    # 更新业务信息表
    update_business_db(to_business_db_data)


@task
def get_cc_hosts(bk_token, bk_biz_id=None):
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
        client = get_client(bk_token)
        host_res = client.cc.search_host(kwargs)
    except Exception as e:
        logger.error("home_application.tasks, 调用client.cc.search_host接口失败{}".format(e))
        return

    # 更新主机信息表
    update_host_db(host_res["data"]["info"], bk_biz_id)


@task
def async_handle_execute_script(client, kwargs, record_id):
    """异步执行脚本任务
    """
    try:
        result = client.job.fast_execute_script(kwargs)
    except Exception:
        logger.error("home_application.tasks, client.job.fast_execute_script接口执行失败 "
                     "kwargs={kwargs}, result={result}".format(kwargs=kwargs, result=result))
        MissionRecord.objects.filter(pk=record_id).update(status="fail")
        return

    if result["result"]:
        job_instance_id = result["data"]["job_instance_id"]
        MissionRecord.objects.filter(pk=record_id).update(job_instance_id=job_instance_id, status="2")
        bk_biz_id = kwargs.get("bk_biz_id", "")
        QueryParams.objects.create(
            bk_biz_id=bk_biz_id,
            job_instance_id=job_instance_id,
            record_id=record_id
        )
        get_job_status.delay(client, record_id, bk_biz_id, job_instance_id)
    else:
        if result["code"] == UNAHTHENTICATED_CODE:
            MissionRecord.objects.filter(pk=record_id).update(status="13")
            logger.error("用户认证信息失效，请重新登陆.")
        else:
            MissionRecord.objects.filter(pk=record_id).update(status="4")
            logger.error("home_application.tasks, 调用client.job.fast_execute_script接口失败 "
                         "kwargs={kwargs}, result={result}".format(kwargs=kwargs, result=result))


@task
def get_job_status(client, record_id, bk_biz_id, job_instance_id):
    try_num = 0
    while True and try_num < 5:
        kwargs = {
            "bk_biz_id": bk_biz_id,
            "job_instance_id": job_instance_id
        }
        record_id = record_id
        result = client.job.get_job_instance_status(kwargs)
        if result["result"] and result["data"]["is_finished"]:
            status = result["data"]["job_instance"]["status"]
            MissionRecord.objects.filter(pk=record_id).update(status=status)
            return
        try_num += 1
        time.sleep(1)
