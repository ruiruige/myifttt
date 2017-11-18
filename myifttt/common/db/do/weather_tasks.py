#!/usr/bin/env python
# coding=utf-8
# author = ruiruige
# email = whx20202@gmail.com
"""天气任务表

记录每个用户的配置
"""
import time

from sqlalchemy import Column, INT, Text, DATE
from sqlalchemy import cast

from myifttt.common.db.do.base_do import Base_do
from myifttt.common.db import db
from myifttt.common.db.db import Base
from myifttt.common.db.do.push_log import Push_log
from myifttt.common.utils import datetime_utils
from myifttt.common.log.log import getLogger

LOG = getLogger(__name__)


class Weather_tasks(Base, Base_do):
    """[summary]

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
    __tablename__ = 'weather_tasks'

    # 表的结构:
    task_id = Column("id", INT, primary_key=True)
    user = Column("user", Text)
    city_id = Column("city_id", Text)
    ge_high_delta_watermark = Column("ge_high_delta_watermark", INT)
    le_high_delta_watermark = Column("le_high_delta_watermark", INT)
    ge_low_delta_watermark = Column("ge_low_delta_watermark", INT)
    le_low_delta_watermark = Column("le_low_delta_watermark", INT)
    push_method = Column("push_method", Text)
    check_hour_of_day = Column("check_hour_of_day", INT)

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
            today_str = datetime_utils.get_today_day_str()

            session = db.get_session()
            pushed_log_list = session.query(Push_log).filter(
                Push_log.task_id == self.task_id).filter(Push_log.push_plugin == "weather").filter(
                    Push_log.push_user == self.user).filter(
                        cast(Push_log.push_datetime, DATE) == today_str).all()

            pushed_log_num = len(pushed_log_list)
            LOG.debug("task_id: %d, pushed_log_list lenght is %d", self.task_id,
                      pushed_log_num)

            if pushed_log_num > 0:
                return True
            return False
        finally:
            session.close()

    def should_run(self):
        """判断一个任务是否应该执行

        [description]

        Arguments:
            task {[type]} -- [description]
        """
        # 检查是否已经推送过
        if self.has_already_run():
            LOG.info("task_id: %d has_already_run !!! ", self.task_id)
            return False
        # 检查是否到执行任务的时间了
        elif self.time_to_run_task():
            LOG.info("task_id: %d time_to_run_task !!! ", self.task_id)
            return True

        LOG.info("task_id: %d time not yet !!! ", self.task_id)
        return False


def get_all_tasks():
    """获取所有天气任务

    [description]
    """
    try:
        session = db.get_session()
        task_list = session.query(Weather_tasks).all()
        return task_list
    finally:
        session.close()
