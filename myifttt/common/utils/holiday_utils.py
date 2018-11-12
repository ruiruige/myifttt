#!/usr/bin/env python
# coding=utf-8
# author = ruiruige
# email = whx20202@gmail.com
"""节假日工具集

包括阳历农历中国节假日
"""

import calendar
from datetime import datetime

from dateutil import relativedelta

from myifttt.common.utils.datetime_utils import date_str_to_int_formatted
from myifttt.common.utils.httputils import http_get
from myifttt.common.utils import datetime_utils
from myifttt.common.log.log import getLogger

LOG = getLogger(__name__)

_date_cache = {}


def is_huawei_rest_day(date_str=None):
    """[summary]

    [description]

    Keyword Arguments:
        date_str {[type]} -- [description] (default: {None})

    Returns:
        bool -- [description]
    """
    if get_date_attribute(date_str=date_str) in [1, 2]:
        return True
    return False


def get_date_attribute(date_str=None):
    """获取法定的日期属性

    [description]

    Arguments:
        date_str {[type]} -- [description], eg: 2018-01-25

    Returns:
        number -- 0:工作日 1:周末 2:节假日
    """
    if date_str in _date_cache:
        return _date_cache[date_str]

    url = "https://tool.bitefu.net/jiari/"
    int_formatted_str = date_str_to_int_formatted(date_str)
    params = {
        "d": int_formatted_str
    }
    resp = http_get(url=url, params=params, timeout=20)

    _date_cache[date_str] = resp.text
    return resp.text


def get_huawei_date_attribute(date_str=None):
    """获取华为版的日期属性

    先判断是否为月末周六，如果是就直接返回1，不是再调用法定的方法

    Keyword Arguments:
        date_str {[type]} -- [description] (default: {None})

    Returns:
        number -- [description]
    """
    if is_last_saturday_of_month(date_str=date_str):
        return 1

    return get_date_attribute(date_str=date_str)


def is_last_saturday_of_month(date_str=None):
    """判断一天是否是月末周六

    [description]

    Keyword Arguments:
        date_str {[type]} -- [description] (default: {None})
    """
    splitted_date_str = datetime_utils.split_date_str(date_str)
    year = splitted_date_str[0]
    month = splitted_date_str[1]

    saturday_date_str = last_saturday_of_month(year=year, month=month)
    return True if date_str == saturday_date_str else False


def last_saturday_of_month(year=None, month=None):
    """获取指定年月的月末周六

    格式形如2017-11-01

    Keyword Arguments:
        year {[type]} -- [description] (default: {None})
        month {[type]} -- [description] (default: {None})

    Returns:
        [type] -- [description]
    """
    month_range = calendar.monthrange(year, month)

    saturday_list = []
    for i in xrange(1, month_range[1] + 1):
        dt = datetime(year, month, i)
        if dt.weekday() == 5:
            saturday_list.append(datetime_utils.datetime_to_date_str(dt))

    return max(saturday_list)


def get_target_month_year():
    """获取宵夜补助所对应的月和年

    如果现在是月初，那么检查的是上个月的
    如果现在是月末，那么检查这个月的

    Returns:
        [type] -- [description]
    """
    dt = datetime.now()
    year = dt.year
    month = dt.month
    today = dt.day

    if today < 15:
        previous_month_date = dt + relativedelta.relativedelta(months=-1)
        return previous_month_date.month, previous_month_date.year
    elif today >= 15:
        return month, year


def get_all_possible_subsidy_remind_days(dt=None):
    """返回所有可能需要申报补助的日子

    算法思路是这样的：
        1. 如果现在已经是月初了，那么只看前四天
        2. 如果现在是月末，那么看本月末和下个月前四天

    Returns:
        [type] -- [description]
    """
    year = dt.year
    month = dt.month
    today = dt.day
    rst = []

    if today < 15:
        rst.extend(first_4_days_of_month(year=year, month=month))
    elif today >= 15:
        next_month_date = dt + relativedelta.relativedelta(months=1)
        rst.extend(last_7_days_of_month(year=year, month=month))
        rst.extend(first_4_days_of_month(
            next_month_date.year, next_month_date.month))

    return rst


def last_7_days_of_month(year=None, month=None):
    """返回指定月最后7天

    [description]

    Keyword Arguments:
        year {[type]} -- [description] (default: {None})
        month {[type]} -- [description] (default: {None})

    Returns:
        [type] -- [description]
    """
    month_range = calendar.monthrange(year, month)
    month_length = month_range[1]

    rst = []
    for i in range(month_length - 6, month_length + 1):
        rst.append(datetime_utils.datetime_to_date_str(
            datetime(year, month, i)))
    return rst


def first_4_days_of_month(year=None, month=None):
    """返回指定月的前5天

    [description]

    Keyword Arguments:
        year {[type]} -- [description] (default: {None})
        month {[type]} -- [description] (default: {None})

    Returns:
        [type] -- [description]
    """
    rst = []
    for i in range(1, 5):
        rst.append(datetime_utils.datetime_to_date_str(
            datetime(year, month, i)))
    return rst


def get_remind_day_list():
    """获取应该提醒的日期列表

    应该为月初的最早工作日，或者月末的最晚工作日
    已经过去的日子会被过滤掉

    Returns:
        [type] -- [description]
    """
    dt = datetime.now()
    possible_remind_days = get_all_possible_subsidy_remind_days(
        dt=dt)
    LOG.debug("possible_remind_days is %s", possible_remind_days)

    today_date_str = datetime_utils.get_today_date_str()

    valid_remind_days = [
        x for x in possible_remind_days if today_date_str >= x]
    LOG.debug("valid_remind_days is %s", valid_remind_days)
    return valid_remind_days


def get_remind_day():
    """获取最终发送提醒的哪一天

    从获取应该提醒的日期列表中，获取第一个工作日
    """
    remind_day_list = get_remind_day_list()

    for date_str in remind_day_list:
        if not is_huawei_rest_day(date_str=date_str):
            return date_str
