#!/usr/bin/env python
# coding=utf-8
# author = ruiruige
# email = whx20202@gmail.com
# pylint: disable=W0603
"""
配置文件的全局信息
"""

import os
import ConfigParser

from oslo_config import cfg

DEFAULT_CONF_DIR = None
DEFAULT_CONF_ABS_FP = None


def init_global_const():
    """
    从元数据配置文件的ini里面，读取配置文件的名称
    再计算出配置文件的绝对路径
    """
    global DEFAULT_CONF_DIR
    global DEFAULT_CONF_ABS_FP

    self_abs_fp = os.path.abspath(__file__)

    DEFAULT_CONF_DIR = os.path.join(
        os.path.dirname(self_abs_fp), "..", "..", "conf", "common")
    DEFAULT_CONF_DIR = os.path.abspath(DEFAULT_CONF_DIR)

    # 读取元配置文件
    meta_conf_parser = ConfigParser.ConfigParser()
    meta_conf_parser.read(os.path.join(DEFAULT_CONF_DIR, "base.ini"))

    # 从元配置文件中读到默认配置文件的文件名
    default_conf_file_name = meta_conf_parser.get(
        "default", "default_config_filename")

    DEFAULT_CONF_ABS_FP = os.path.abspath(os.path.join(
        DEFAULT_CONF_DIR, default_conf_file_name))

init_global_const()


def get_plugin_conf_abs_fp(name=None):
    """根据插件名称，返回插件配置文件绝对路径

    [description]

    Keyword Arguments:
        name {[type]} -- [description] (default: {None})
    """
    file_name = "%s.conf" % name
    return os.path.join(DEFAULT_CONF_DIR, "plugins", file_name)


def get_plugin_conf_from_file(name=None, opts=None):
    """
    解析配置文件，并且返回一个oslo_config.cfg.CONF对象
    对象默认是DEFAULT section的
    """
    CONF = cfg.ConfigOpts()
    CONF.register_opts(opts)
    CONF(default_config_files=[get_plugin_conf_abs_fp(name=name), ])
    return CONF


def get_db_conf_abs_fp():
    """获取数据库配置文件路径

    为绝对值
    """
    self_abs_fp = os.path.abspath(__file__)

    db_conf_fp = os.path.join(
        os.path.dirname(self_abs_fp),
        "..", "..", "conf", "common", "db",
        "db.conf")

    db_conf_abs_fp = os.path.abspath(db_conf_fp)
    return db_conf_abs_fp
