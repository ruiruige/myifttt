#!/usr/bin/env python
# coding=utf-8
# author = ruiruige
# email = whx20202@gmail.com
"""日志模块

[description]
"""

import logging as ori_logging

from oslo_config import cfg
from oslo_log import log as logging

LOG = logging.getLogger(__name__)
CONF = cfg.ConfigOpts()
DOMAIN = "demo"

# 注册扩展配置项
extend_opts = [
    cfg.BoolOpt('enable_console_log',
                help='open it to print to screen')
]

# extend group
extend_group = cfg.OptGroup(
    name='EXTEND',
    title='EXT options'
)

CONF.register_group(extend_group)
CONF.register_opts(extend_opts, extend_group)


logging.register_options(CONF)
CONF(default_config_files=[
    "/root/code/test/myifttt/conf/common/log/log.conf", ])
logging.setup(CONF, DOMAIN)


# 初始化其他功能
console = None
if CONF.EXTEND.enable_console_log:
    console = ori_logging.StreamHandler()
    console.setLevel(ori_logging.DEBUG)
    formatter = ori_logging.Formatter(
        '%(asctime)s %(filename)s [line:%(lineno)d] [%(funcName)s] %(levelname)s %(message)s')
    console.setFormatter(formatter)
    LOG.handlers.append(console)


# 根据扩展配置项应用自定义功能
def getLogger(name):
    """[summary]

    [description]

    Arguments:
        name {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    named_logger = logging.getLogger(name)
    if console:
        named_logger.handlers.append(console)
    return named_logger
