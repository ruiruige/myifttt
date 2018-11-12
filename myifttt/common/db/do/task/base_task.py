#!/usr/bin/env python
# coding=utf-8
# author = ruiruige
# email = whx20202@gmail.com
# pylint: disable=R0201
"""基础任务类

[description]
"""

import time

from sqlalchemy import DATE
from sqlalchemy import cast

from myifttt.common.db import db
from myifttt.common.db.do.push_log import Push_log
from myifttt.common.log.log import getLogger
from myifttt.common.utils import datetime_utils

LOG = getLogger(__name__)


class Base_task(object):
    """[summary]

    [description]

    Extends:
        Base
        Base_do
    """

    # 这四个属性是task公共属性，且必须被子类覆盖
    task_id = None
    user = None
    push_method = None
    check_hour_of_day = None

    def time_to_run_task(self):
        """查看是否到了执行任务的时间

        [description]
        """
        localtime = time.localtime(time.time())
        hour = localtime.tm_hour
        if hour >= self.check_hour_of_day:
            return True
        return False

    def has_already_run(self):
        """检查任务是否已经执行过

        凡是推送完毕才叫执行完
        """
        try:
            date_str_to_check = self.date_str_of_checking_push_log()

            session = db.get_session()
            pushed_log_list = session.query(Push_log).filter(
                Push_log.task_id == self.task_id).filter(Push_log.push_plugin == self.get_task_plugin_name()).filter(
                    Push_log.push_user == self.user).filter(
                        cast(Push_log.push_datetime, DATE) == date_str_to_check).all()

            pushed_log_num = len(pushed_log_list)
            LOG.debug("[task_name: %s] [task_id: %d], pushed_log_list length is %d",
                      self.get_task_plugin_name(), self.task_id,
                      pushed_log_num)

            if pushed_log_num > 0:
                return True
            return False
        finally:
            session.close()

    def date_str_of_checking_push_log(self):
        """获取需要检查推送记录的日期

        每次检查push_log记录，检查的时间（日期）由这里指定
        """
        return datetime_utils.get_today_date_str()

    def should_run(self):
        """判断一个任务是否应该执行

        [description]

        Arguments:
            task {[type]} -- [description]
        """
        # 检查是否已经推送过
        if self.has_already_run():
            LOG.info("[%s] [task_id: %d] has_already_run !!! ",
                     self.get_task_plugin_name(), self.task_id)
            return False
        # 检查是否到执行任务的时间了
        elif self.time_to_run_task():
            LOG.info("[%s] [task_id: %d] time_to_run_task !!! ",
                     self.get_task_plugin_name(), self.task_id)
            return True

        LOG.info("[%s] [task_id: %d] time not yet !!! ",
                 self.get_task_plugin_name(), self.task_id)
        return False

    @classmethod
    def get_all_tasks(cls):
        """获取所有任务

        通过classmethod的方法，获取各个task的cls
        以便数据库查询
        """
        try:
            session = db.get_session()
            task_list = session.query(cls).all()
            return task_list
        finally:
            session.close()

    @classmethod
    def _get_class(cls):
        """返回当前类的类型

        基本上返回的都是子类的类型

        Returns:
            [type] -- [description]
        """
        return cls

    def get_task_plugin_name(self):
        """返回任务插件的名称

        子类task必须有 __task_plugin_name__ 属性 
        """
        if hasattr(self, "__task_plugin_name__"):
            return getattr(self, "__task_plugin_name__")
        raise Exception(
            "task object must have an attribute named __task_plugin_name__")
