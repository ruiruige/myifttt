#!/usr/bin/env python
# coding=utf-8
# author = ruiruige
# email = whx20202@gmail.com
"""天气情况表

也就是天气历史的记录
"""
from sqlalchemy import Column, INT, DATE, Text, TIMESTAMP
from myifttt.common.db.do.base_do import Base_do
from myifttt.common.db.db import Base

# 定义User对象:


class Weather_info(Base, Base_do):
    """[summary]

    [description]

    Extends:
        Base
        Base_do

    Variables:
        __tablename__ {str} -- [description]
        info_id {[type]} -- [description]
        city_alias {[type]} -- [description]
        city_id {[type]} -- [description]
        city_name {[type]} -- [description]
        temperature_high {[type]} -- [description]
        temperature_low {[type]} -- [description]
        text_day {[type]} -- [description]
        text_night {[type]} -- [description]
        info_date {[type]} -- [description]
        created_at {[type]} -- [description]
        updated_at {[type]} -- [description]
    """

    # 表的名字:
    __tablename__ = 'weather_info'

    # 表的结构:
    info_id = Column("id", INT(), primary_key=True)
    city_alias = Column("city_alias", Text)
    city_id = Column("city_id", Text)
    city_name = Column("city_name", Text)
    temperature_high = Column("temperature_high", INT)
    temperature_low = Column("temperature_low", INT)
    text_day = Column("text_day", Text)
    text_night = Column("text_night", Text)
    info_date = Column("info_date", DATE)
    created_at = Column("created_at", TIMESTAMP)
    updated_at = Column("updated_at", TIMESTAMP)
