#!/usr/bin/env python
# coding=utf-8
# author = ruiruige
# email = whx20202@gmail.com
"""
宵夜补助插件
"""


from myifttt.common.utils import holiday_utils
from myifttt.common.db.do.task.midnight_subsidy_tasks import Midnight_subsidy_tasks
from myifttt.common.log.log import getLogger

LOG = getLogger(__name__)


def get_all_subsidy_tasks():
    """[summary]

    [description]

    Returns:
        [type] -- [description]
    """
    LOG.info("getting all tasks")
    task_list = Midnight_subsidy_tasks.get_all_tasks()
    LOG.info("task list length is %d", len(task_list))
    return task_list


def run_job(task):
    """[summary]

    [description]

    Arguments:
        task {[type]} -- [description]
    """
    valid_remind_days = holiday_utils.get_remind_day()
    for date_str in valid_remind_days:
        if not holiday_utils.is_huawei_rest_day(date_str=date_str):
            # send
            # post_execute_task
            break


def execute_routine():
    """上游调用此模块的唯一入口

    调用后未必会真的执行核心业务
    """
    task_list = get_all_subsidy_tasks()
    for task in task_list:
        LOG.info("processing %s task [id: %d]", __name__, task.task_id)
        if task.should_run():
            LOG.debug("going to run %s task [id: %d]", __name__, task.task_id)
            run_job(task)
        else:
            LOG.info("%s task [id: %d, user: %s] should not run",
                     __name__, task.task_id, task.user)
