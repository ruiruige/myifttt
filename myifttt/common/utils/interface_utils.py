#!/usr/bin/env python
# coding=utf-8
# author = ruiruige
# email = whx20202@gmail.com
"""[summary]

[description]
"""

from myifttt.common.error.interface_not_impl import interface_not_impl


def interface(func):
    """[summary]

    [description]

    Arguments:
        func {[type]} -- [description]

    Returns:
        [type] -- [description]

    Raises:
        interface_not_impl -- [description]
    """

    def wrapper(*args, **kwargs):
        """[summary]

        [description]

        Arguments:
            *args {[type]} -- [description]
            **kwargs {[type]} -- [description]

        Raises:
            interface_not_impl -- [description]
        """
        funcname = func.__name__
        raise interface_not_impl(interface_name=funcname)

    return wrapper
