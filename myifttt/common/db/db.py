#!/usr/bin/env python
# coding=utf-8
# author = ruiruige
# email = whx20202@gmail.com
"""数据库总的入口文件

[description]
"""
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from oslo_config import cfg
from oslo_log import log as logging

from myifttt.common.config import global_config


LOG = logging.getLogger(__name__)

# 数据库的配置项
db_opts = [
    cfg.StrOpt('db_username',
               default='myifttt',
               help='user name for db'),
    cfg.StrOpt('db_passwd',
               help='password'),
    cfg.IntOpt('port',
               help='port'),
    cfg.StrOpt('host',
               help='host'),
    cfg.StrOpt('db_name',
               help='db_name')
]


CONF = cfg.CONF
# 注册默认组的配置项
CONF.register_opts(db_opts)


# 设置默认的日志文件名
db_conf_abs_fp = global_config.get_db_conf_abs_fp()
CONF(sys.argv[1:], default_config_files=[db_conf_abs_fp, ])

# 创建对象的基类:
Base = declarative_base()

# 初始化数据库连接:
engine = create_engine(
    'postgresql://%s:%s@%s:%d/%s' % (CONF.db_username,
                                     CONF.db_passwd,
                                     CONF.host, CONF.port, CONF.db_name))

# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)


def get_session():
    """Get DB session

    Returns a DBSession object, by default the session is managed by the default QueuePool.

    :param None: None args
    :returns: a DBSession object by which one can exe sql
    :raises: None

    """
    return DBSession()
