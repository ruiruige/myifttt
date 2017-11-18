#!/usr/bin/env python
# coding=utf-8
# author = ruiruige
# email = whx20202@gmail.com
"""日期时间的工具类

[description]
"""

import time


def get_today_day_str():
    """返回本日的日期字符串

    如：2017-11-13

    Returns:
        string -- [description]
    """
    return time.strftime("%Y-%m-%d", time.localtime())
