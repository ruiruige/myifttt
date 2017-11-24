#!/usr/bin/env python
# coding=utf-8
# author = ruiruige
# email = whx20202@gmail.com
"""
调度器方法
"""

from oslo_config import cfg
from apscheduler.schedulers.blocking import BlockingScheduler

from myifttt.common.config import global_config

opts = [
    cfg.IntOpt('main_thread_check_interval', default=5)
]

# 如果用类变量，那么在fork之前，就会执行，导致fork进程和原进程d都持有文件
CONF = cfg.ConfigOpts()
CONF.register_opts(opts)
CONF(default_config_files=[global_config.DEFAULT_CONF_ABS_FP, ])


class Scheduler(object):
    """[summary]

    [description]

    Extends:
        Object
    """

    def __init__(self):
        self.module_list = []

    def add_module(self, module):
        """[summary]

        [description]

        Arguments:
            module {[type]} -- [description]
        """
        if module:
            self.module_list.append(module)

    def run(self):
        """[summary]

        [description]
        """
        sched = BlockingScheduler()

        for _module in self.module_list:
            sched.add_job(_module.execute_routine, 'interval',
                          seconds=CONF.main_thread_check_interval)

        sched.start()
