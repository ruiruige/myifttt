#!/usr/bin/env python
# coding=utf-8
# author = ruiruige
# email = whx20202@gmail.com

import web

from jx3wj.common.rest.rest_base import resources
from jx3wj.common.rest.dto.dto import deco_dump_to_str
from jx3wj.common.log import log as logging
from jx3wj.common.db.crud import select
from jx3wj.common.db.do.item import Item
from jx3wj.common.db.do.base_do import Base_do
from jx3wj.common.utils.web_utils import not_found_utils
from jx3wj.common.utils.web_utils import redirect_utils
from jx3wj.common.rest.response_control import assemble_response
from jx3wj.mgmt.items import items_view


LOG = logging.getLogger(__name__)

# 这两段放在前面以便被引用到
# 处理api相关的url
api_urls = (
    "/items", "items"
)
# api相关的子应用
api_app = web.application(api_urls, locals())


# url入口点
urls = (
    # 要按顺序，否则"/api/items"这种请求，就走"/"不走"/api"了
    "/api", api_app,
    "(.*)", not_found_utils.not_found_app,
    "/", items_view.app,
    "", redirect_utils.add_backslash_app,
)


class reitems(object):

    def GET(self):
        raise web.seeother('/')


class items(resources):

    @assemble_response
    @Base_do.deco_sqlalchemy_obj_to_dict
    @resources.manage_rest_api()
    def GET(self):
        rst = select(cls=Item)
        return rst

    def before_response(self, session=None):
        """Do some preparations before response to the REST request.

        inherited from super, This function is run before the doGet doPost etc is run.

                :see: super.before_response
        :raises: None
        """
        cls_name = self.__class__.__name__

        # 类的初始化顺序遵循MRO(Method Resolution Order)，即方法解析序列
        super(items, self).__init__()
        LOG.debug("running before_response of class : %s" % cls_name)

# 入口点应用
app = web.application(urls, locals())
