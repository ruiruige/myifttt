#!/usr/bin/env python
# coding=utf-8
# author = ruiruige
# email = whx20202@gmail.com
import sys

import web
from oslo_config import cfg, types
from oslo_context import context

from jx3wj.common.log import log as logging

LOG = logging.getLogger(__name__)


class view(object):

    def __init__(self):
        pass


class Error(Exception):
    """Base class for view exceptions."""

    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        return self.msg
