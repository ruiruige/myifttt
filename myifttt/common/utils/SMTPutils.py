#!/usr/bin/env python
# coding=utf-8
# author = ruiruige
# email = whx20202@gmail.com
"""通过SMTP来发邮件的的utils

[description]
"""


import smtplib
from email.mime.text import MIMEText
from email.header import Header
import traceback

from myifttt.common.log.log import getLogger

LOG = getLogger(__name__)


def send_normal_mail(user=None, password=None, port=None,
                     host=None, subject=None, from_user=None,
                     to_user=None, body=None, from_nickname=None, to_nickname=None):
    """[summary]

    [description]

    Keyword Arguments:
        user {[type]} -- 邮箱用户名 (default: {None})
        password {[type]} -- 邮箱密码 (default: {None})
        port {[type]} -- SMTP服务器端口 (default: {None})
        host {[type]} -- SMTP服务器地址 (default: {None})
        subject {[type]} -- 邮件标题 (default: {None})
        from_user {[type]} -- from的邮箱地址 (default: {None})
        to_user {[type]} -- to的邮箱地址 (default: {None})
        body {[type]} -- 邮件正文 (default: {None})
        from_nickname {[type]} -- 发送者的昵称 (default: {None})
        to_nickname {[type]} -- 接受者的昵称 (default: {None})
    """

    LOG.info("entering func send_normal_mail")

    # 接收人列表
    receivers = [to_user, ]

    # 正文 subtype 字符集
    message = MIMEText(body, 'plain', 'utf-8')
    message['From'] = Header("%s <%s>" % (from_nickname, from_user), 'utf-8')
    message['To'] = Header("%s <%s>" % (to_nickname, to_user), 'utf-8')

    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(host, port)
        smtpObj.login(user, password)
        smtpObj.sendmail(from_user, receivers, message.as_string())
    except smtplib.SMTPException:
        print "Error: 无法发送邮件"
        traceback.print_exc()
