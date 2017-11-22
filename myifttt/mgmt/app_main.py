#!/usr/bin/env python
# coding=utf-8
# author = ruiruige
# email = whx20202@gmail.com
# pylint: disable=E1101
"""
app入口文件
"""

import os
import traceback


from myifttt.common.utils import plugin_utils


def run():
    """
    用于真正运行业务代码的方法
    """
    from myifttt.mgmt.scheduler import Scheduler

    scheduler = Scheduler()
    # 加载插件模块
    module_list = plugin_utils.get_plugin_modules()
    for _module in module_list:
        scheduler.add_module(_module)

    scheduler.run()


def start_procs():
    """
    执行函数的入口点，用于拉起fork进程
    """
    try:
        pid = os.fork()

        if pid == 0:
            run()

    except OSError as exception:
        print(exception)
        print(traceback.format_exc())


if __name__ == '__main__':
    start_procs()
