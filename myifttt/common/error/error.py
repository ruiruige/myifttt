#!/usr/bin/env python
# coding=utf-8
# author = ruiruige
# email = whx20202@gmail.com
"""[summary]

[description]
"""


class Error(Exception):
    """[summary]

    [description]

    Extends:
        Exception
    """

    def __init__(self, msg=None):
        self.msg = msg
        super(Error, self).__init__(msg)

    def __str__(self):
        return self.msg
