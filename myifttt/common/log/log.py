#!/usr/bin/env python
# coding=utf-8
# author = ruiruige
# email = whx20202@gmail.com
import sys
import logging as ori_logging

from oslo_config import cfg
from oslo_log import log as logging
from oslo_context import context


LOG = logging.getLogger(__name__)
CONF = cfg.CONF
DOMAIN = "log"

logging.register_options(CONF)

# 获取重载的配置
override_conf = cfg.ConfigOpts()

# override log default opts
log_opts = [
    cfg.StrOpt('log_dir', help='log file dir'),
    cfg.StrOpt('log_file', help='log file name'),
    cfg.BoolOpt('debug', help='log debug level switch'),
]

# extend group
extend_group = cfg.OptGroup(
    name='EXTEND',
    title='EXT options'
)

# extend opts
extend_opts = [
    cfg.StrOpt('enable_console_log', help='open it to print to screen'),
]

# start to load options from file
override_conf.register_opts(log_opts)
# register extend group
override_conf.register_group(extend_group)
# register extend options
override_conf.register_opts(extend_opts, extend_group)

override_conf(sys.argv[1:], default_config_files=[
              "/root/code/jx3wj/jx3wj/conf/common/log/log.conf"])
opts_not_override = ["config_dir", "config_file"]

# 从重载配置项里覆盖配置到oslo_log
for override_opt in override_conf.items():
    k, v = override_opt
    if k in opts_not_override:
        continue
    # if it is a Non-DEFAULT-GROUP, pass it
    elif "EXTEND" == k:
        pass
    else:
        CONF.set_override(name=override_opt[0], override=override_opt[1])

logging.setup(CONF, DOMAIN)
# 使得生成的日志带request-id
context.RequestContext()


# 初始化其他功能
enable_console_log = False
console = None
if override_conf.EXTEND.enable_console_log:
    console = ori_logging.StreamHandler()
    console.setLevel(ori_logging.DEBUG)
    formatter = ori_logging.Formatter(
        '%(asctime)s %(filename)s [line:%(lineno)d] [%(funcName)s] %(levelname)s %(message)s')
    console.setFormatter(formatter)


# 根据扩展配置项应用自定义功能
def getLogger(name):
    LOG = logging.getLogger(name)
    if console:
        LOG.handlers.append(console)
    return LOG
