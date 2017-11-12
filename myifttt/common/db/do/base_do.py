#!/usr/bin/env python
# coding=utf-8
# author = ruiruige
# email = whx20202@gmail.com
# pylint: disable=W1402,C0123
"""domain object基类

[description]
"""
from myifttt.error.common.db.do.SqlalchemyConvertToDictError import SqlalchemyConvertToDictError
from myifttt.common.db.db import Base


class Base_do(object):
    """[summary]

    [description]
    """

    @staticmethod
    def deco_sqlalchemy_obj_to_dict(func):
        """装饰器，将sqlalchemy的结果变成

        通过调用sqlalchemy_obj_to_dict实现
        """
        def wrapper(*args, **kwargs):
            """装饰器的wrapper

            [description]

            Arguments:
                *args {list} -- args
                **kwargs {dict} -- kwargs

            Returns:
                dict -- Base_do.sqlalchemy_obj_to_dict(rst)
            """
            rst = func(*args, **kwargs)
            dct = Base_do.sqlalchemy_obj_to_dict(rst)
            return dct
        return wrapper

    @staticmethod
    def sqlalchemy_obj_to_dict(obj):
        """
        把SqlAlchemy的查询结果转换为dict对象
        SqlAlchemy的查询结果，是由list和dict以及Do组合成的类型
        """
        rtn = None

        if obj is None:
            rtn = None
        else:
            # 按照list处理
            if type(obj) == type([]):
                containner = [Base_do.sqlalchemy_obj_to_dict(
                    item) for item in obj]
                rtn = containner

            # 按照字典处理
            elif type(obj) == type({}):
                containner = {
                    k: Base_do.sqlalchemy_obj_to_dict(k) for k in obj}
                rtn = containner

            # 按照sqlalchemy类处理
            elif isinstance(obj, Base):
                rtn = Base_do.do_to_dict(obj)

            else:
                raise SqlalchemyConvertToDictError(
                    msg="sqlalchemy obj can not be converted to dict")

        return rtn

    @staticmethod
    def do_to_dict(obj):
        """
        把SqlAlchemy对象转换成一个dict对象

        eg : 
        (Pdb) obj.__dict__
        {'_sa_instance_state': 
            <sqlalchemy.orm.state.InstanceState object at 0x7f81bc6d1310>, 
            'description': u'\u6d4b\u8bd5\u7528\u7684\u91d1\u53d1', 
            'created_at': datetime.datetime(2017, 6, 11, 13, 7, 19), 
            'updated_at': datetime.datetime(2017, 6, 11, 13, 7, 15), 
            'item_type': u'\u5934\u53d1', 
            'alias_obj_str': None, 
            'item_id': 1, 
            'main_color': None, 
            'launched_at': datetime.datetime(2017, 6, 11, 13, 7, 25), 
            'name': u'\u6d4b\u8bd5\u91d1\u53d1'}
        """

        obj_dct = obj.__dict__
        rtn_dict = {}

        for k in obj_dct:
            if k in ["_sa_instance_state", ]:
                continue
            else:
                rtn_dict[k] = obj_dct[k]

        return rtn_dict
