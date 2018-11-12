#!/usr/bin/env python
# coding=utf-8
# author = ruiruige
# email = whx20202@gmail.com
"""[summary]

[description]
"""

from myifttt.common.error.error import Error


class interface_not_impl(Error):
    """子类接口尚未实现，就会自动抛出的异常

    [description]

    Extends:
        Exception
    """

    def __init__(self, interface_name=None):
        self.interface_name = interface_name
        self.msg = self.__msg__()
        super(interface_not_impl, self).__init__(msg=self.msg)

    def __str__(self):
        return self.msg

    def __msg__(self):
        return "function: %s has not been implemented" % self.interface_name
