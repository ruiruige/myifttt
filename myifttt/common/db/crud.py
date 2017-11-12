#!/usr/bin/env python
# coding=utf-8
# author = ruiruige
# email = whx20202@gmail.com

from jx3wj.common.db.db import get_session

def select(cls=None, limit=10, offset=0, group_by=None, order_by=None):
    session = get_session()

    # start statement
    stmt = session.query(cls)
    # filter
    pass

    # group by
    pass

    # limit
    result_set = stmt.limit(limit).all()
    
    return result_set
