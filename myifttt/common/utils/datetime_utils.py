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
