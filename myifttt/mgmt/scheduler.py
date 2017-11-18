#!/usr/bin/env python
# coding=utf-8
# author = ruiruige
# email = whx20202@gmail.com
"""
调度器方法
"""

from oslo_config import cfg

from myifttt.common.config import global_config

opts = [
    cfg.FloatOpt('main_thread_check_interval', default=1.0)
]

CONF = cfg.CONF
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
        for _module in self.module_list:
            _module.execute_routine()
