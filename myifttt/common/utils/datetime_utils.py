#!/usr/bin/env python
# coding=utf-8
# author = ruiruige
# email = whx20202@gmail.com
"""日期时间的工具类

[description]
"""

import time


def get_today_date_str():
    """返回本日的日期字符串

    如：2017-11-13

    Returns:
        string -- [description]
    """
    return time.strftime("%Y-%m-%d", time.localtime())


def datetime_to_date_str(dt):
    """把datetime格式转为日期字符串

    [description]

    Arguments:
        dt {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    datetime_str = str(dt)
    segments = datetime_str.split(" ")
    return segments[0]


def date_str_to_int_formatted(date_str):
    """把日期字符串转成数字格式的

    eg:
        date_str_to_int_formatted(2017-11-13) -> 20171113

    Arguments:
        date_str {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    return date_str.replace("-", "")


def int_formatted_date_str_to_standard(date_str):
    """将数字格式的日期字符串转换为标准格式的

    eg:
        int_formatted_date_str_to_standard(20171113) -> 2017-11-13

    Arguments:
        date_str {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    return date_str[:4] + "-" + date_str[4:6] + "-" + date_str[6:]


def split_date_str(date_str):
    """将日期字符串分割成年月日三个字符串

    [description]

    Arguments:
        date_str {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    segments = date_str.split("-")
    return segments[0], segments[1], segments[2]
