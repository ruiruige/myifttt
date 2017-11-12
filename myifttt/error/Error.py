#!/usr/bin/env python
# coding=utf-8
# author = ruiruige
# email = whx20202@gmail.com

class Error(Exception):
    """Base class for all exceptions."""

    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        return self.msg