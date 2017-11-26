#!/usr/bin/env python
# coding=utf-8
# author = ruiruige
# email = whx20202@gmail.com
"""推送记录表

所有的推送记录都在这里
"""

import datetime

from sqlalchemy import Column, INT, Text, TIMESTAMP
from sqlalchemy import func
from myifttt.common.db.do.base_do import Base_do
from myifttt.common.db.db import Base


class Push_log(Base, Base_do):
    """[summary]

    [description]

    Extends:
        Base
        Base_do

    Variables:
        __tablename__ {str} -- [description]
        log_id {[type]} -- [description]
        push_method {[type]} -- [description]
        push_datetime {[type]} -- [description]
        push_user {[type]} -- [description]
        push_plugin {[type]} -- [description]
        plugin_push_reason {[type]} -- [description]
        key_value {[type]} -- [description]
        key_value_2 {[type]} -- [description]
        task_id {[type]} -- [description]
    """

    # 表的名字:
    __tablename__ = 'push_log'

    # 表的结构:
    log_id = Column("id", INT, primary_key=True)
    push_method = Column("push_method", Text)
    push_datetime = Column("push_datetime", TIMESTAMP,
                           default=func.now())
    push_user = Column("push_user", Text)
    push_plugin = Column("push_plugin", Text)
    plugin_push_reason = Column("plugin_push_reason", Text)
    key_value = Column("key_value", Text)
    key_value_2 = Column("key_value_2", Text)
    task_id = Column("task_id", INT)
