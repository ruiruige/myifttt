#!/usr/bin/env python
# coding=utf-8
# author = ruiruige
# email = whx20202@gmail.com
"""
宵夜补助任务
"""

from sqlalchemy import Column, INT, Text
from sqlalchemy import func

from myifttt.common.db import db
from myifttt.common.db.db import Base
from myifttt.common.db.do.base_do import Base_do
from myifttt.common.db.do.task.base_task import Base_task
from myifttt.common.db.do.push_log import Push_log
from myifttt.common.log.log import getLogger
from myifttt.common.utils.holiday_utils import get_target_month_year

LOG = getLogger(__name__)


class Midnight_subsidy_tasks(Base_task, Base, Base_do):
    """宵夜补助任务

    [description]

    Extends:
        Base
        Base_do

    Variables:
        __tablename__ {str} -- [description]
        task_id {[type]} -- [description]
        user {[type]} -- [description]
        city_id {[type]} -- [description]
        ge_high_delta_watermark {[type]} -- [description]
        le_high_delta_watermark {[type]} -- [description]
        ge_low_delta_watermark {[type]} -- [description]
        le_low_delta_watermark {[type]} -- [description]
        push_method {[type]} -- [description]
        check_hour_of_day {[type]} -- [description]
    """

    # 表的名字:
    __tablename__ = 'midnight_subsidy_tasks'
    __task_plugin_name__ = "midnight_subsidy"

    # 表的结构:
    task_id = Column("id", INT, primary_key=True)
    user = Column("user", Text)
    push_method = Column("push_method", Text)
    check_hour_of_day = Column("check_hour_of_day", INT)

    def has_already_run(self):
        """检查任务是否已经执行过

        @override
        首先获取当前应该判断那个月
        然后看看这个月是否已经执行过了
        """
        try:
            target_month, target_year = get_target_month_year()

            session = db.get_session()
            pushed_log_list = session.query(Push_log).\
                filter(Push_log.task_id == self.task_id).\
                filter(Push_log.push_plugin == self.get_task_plugin_name()).\
                filter(Push_log.push_user == self.user).\
                filter(func.month(Push_log.push_datetime) == target_month).\
                filter(func.year(Push_log.push_datetime) == target_year).\
                all()

            pushed_log_num = len(pushed_log_list)
            LOG.debug("[task_name: %s] [task_id: %d], pushed_log_list length is %d",
                      self.get_task_plugin_name(), self.task_id,
                      pushed_log_num)

            if pushed_log_num > 0:
                return True
            return False
        finally:
            session.close()

    def time_to_run_task(self):
        """判断是否到了发送宵夜补助提示的时候

        @override
        先判断是否到了需要发送告警的当天，如果是则调用父类方法
        如果不是直接返回False
        """

        localtime = time.localtime(time.time())
        hour = localtime.tm_hour
        if hour >= self.check_hour_of_day:
            return True
        return False
