#!/usr/bin/env python
# coding=utf-8
# author = ruiruige
# email = whx20202@gmail.com
"""
检测天气
"""


from oslo_config import cfg

from myifttt.common.db.do import weather_tasks
from myifttt.common.drivers import weather_driver
from myifttt.common.utils.SMSutils import send_SMS
from myifttt.common.utils.SMTPutils import send_normal_mail
from myifttt.common.config import global_config
from myifttt.common.db.do import users
from myifttt.common.log.log import getLogger
from myifttt.common.utils import datetime_utils

LOG = getLogger(__name__)

# 配置组
email_group = cfg.OptGroup(
    name='EMAIL',
    title='EMAIL options'
)

email_opts = [
    cfg.StrOpt('email_user',
               help='email user of weather account.'),
    cfg.IntOpt('smtp_port',
               default=110,
               help='smtp_port.'),
    cfg.StrOpt('email_password',
               help='email password of weather account.'),
    cfg.StrOpt('smtp_host',
               help='email host of weather account.')
]

CONF = cfg.ConfigOpts()
CONF.register_group(email_group)
CONF.register_opts(email_opts, email_group)
CONF(default_config_files=[
    global_config.get_plugin_conf_abs_fp(name="weather"), ])


def get_all_weather_tasks():
    """获取所有的天气任务

    [description]

    Returns:
        [type] -- [description]
    """
    task_list = weather_tasks.get_all_tasks()
    return task_list


def run_job(task):
    """真正执行核心业务的地方

    [description]
    """
    w_driver = weather_driver.Weather_driver(task=task)
    w_driver.retrieve_2_day_weather()

    if w_driver.is_tomorrow_weather_bad():
        LOG.info(
            "processing task [id: %d], tomorrow is a bad day", task.task_id)
        # 推送
        warning_text = w_driver.generate_warning_text()
        send_warning_text(warning_text=warning_text,
                          method=task.push_method, task_user_name=task.user)

        # 推送之后要执行的函数，主要是生成天气和推送记录
        w_driver.post_push_warning_text()
    else:
        LOG.info(
            "processing task [id: %d], tomorrow is NOT a bad day", task.task_id)


def send_warning_text(warning_text=None, method=None, task_user_name=None):
    """[summary]

    [description]

    Keyword Arguments:
        warning_text {[type]} -- [description] (default: {None})
        method {[type]} -- [description] (default: {None})
    """
    user = users.Users.get_user_by_username(username=task_user_name)
    LOG.debug("push_method is %s", method)

    if method == "EMAIL":
        send_normal_mail(user=CONF.EMAIL.email_user,
                         password=CONF.EMAIL.email_password,
                         port=CONF.EMAIL.smtp_port,
                         host=CONF.EMAIL.smtp_host,
                         subject="%s 天气提醒" % datetime_utils.get_today_day_str(),
                         from_user=CONF.EMAIL.email_user,
                         to_user=user.email,
                         body=warning_text,
                         from_nickname="天气提醒",
                         to_nickname=user.nick_name)
    elif method == "SMS":
        send_SMS(None, None, None,
                 None, None)


def execute_routine():
    """上游调用此模块的唯一入口

    调用后未必会真的执行核心业务
    """
    task_list = get_all_weather_tasks()
    for task in task_list:
        LOG.info("processing task [id: %d]", task.task_id)
        if task.should_run():
            LOG.debug("going to run task [id: %d]", task.task_id)
            run_job(task)
        else:
            LOG.info("task [id: %d, user: %s] should not run",
                     task.task_id, task.user)


if __name__ == '__main__':
    pass
