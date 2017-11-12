#!/usr/bin/env python
# coding=utf-8
# author = ruiruige
# email = whx20202@gmail.com
"""[summary]

[description]
"""
from myifttt.error.Error import Error


class SqlalchemyConvertToDictError(Error):
    """raises when converting a SqlAlchemy obj to dict obj"""

    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        return self.msg
