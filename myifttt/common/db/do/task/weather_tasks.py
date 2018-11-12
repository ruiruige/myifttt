#!/usr/bin/env python
# coding=utf-8
# author = ruiruige
# email = whx20202@gmail.com
"""天气任务表

记录每个用户的配置
"""
from sqlalchemy import Column, INT, Text

from myifttt.common.db.db import Base
from myifttt.common.db.do.base_do import Base_do
from myifttt.common.db.do.task.base_task import Base_task
from myifttt.common.log.log import getLogger

LOG = getLogger(__name__)


class Weather_tasks(Base_task, Base, Base_do):
    """[summary]

    [description]

    Extends:
        Base
        Base_do

    Variables:
        task_id {[type]} -- [description]
        user {[type]} -- [description]
        city_id {[type]} -- [description]
        ge_high_delta_watermark {[type]} -- [description]
        le_high_delta_watermark {[type]} -- [description]
        ge_low_delta_watermark {[type]} -- [description]
        le_low_delta_watermark {[type]} -- [description]
        push_method {[type]} -- [description]
        check_hour_of_day {[type]} -- [description]
        low_threshold {[type]} -- [description]
        high_threshold {[type]} -- [description]
    """

    # 表的名字:
    __tablename__ = 'weather_tasks'
    __task_plugin_name__ = "weather"

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
    low_threshold = Column("low_threshold", INT)
    high_threshold = Column("high_threshold", INT)
