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
                     to_user=None, body=None, from_nickname=None):
    """发送邮件的函数

    [description]
    """
    LOG.info("entering func send_normal_mail")

    sender = 'from@runoob.com'
    # 接收人列表
    receivers = [to_user, ]

    # 正文 subtype 字符集
    message = MIMEText(body, 'plain', 'utf-8')
    message['From'] = Header("%s <%s>" % (from_nickname, from_user), 'utf-8')
    message['To'] = Header(to_user, 'utf-8')

    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(host, port)
        smtpObj.login(user, password)
        smtpObj.sendmail(sender, receivers, message.as_string())
    except smtplib.SMTPException:
        print "Error: 无法发送邮件"
        traceback.print_exc()
