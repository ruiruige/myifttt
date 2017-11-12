#!/usr/bin/env python
# coding=utf-8
# author = ruiruige
# email = whx20202@gmail.com

import web

from jx3wj.common.view.view_base import view
from jx3wj.common.log import log as logging
from jx3wj.common.utils.web_utils import redirect_utils

LOG = logging.getLogger(__name__)

urls = (
    "", "items_view",
)


class items_view(view):

    def GET(self):
        main = web.template.frender('templates/items/items.html')
        LOG.debug("loading template of templates/items/items.html")
        return main


app = web.application(urls, locals())
