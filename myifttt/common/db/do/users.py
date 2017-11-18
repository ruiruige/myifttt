#!/usr/bin/env python
# coding=utf-8
# author = ruiruige
# email = whx20202@gmail.com
"""用户Object表

[description]
"""
from sqlalchemy import Column, INT, Text
from myifttt.common.db.do.base_do import Base_do
from myifttt.common.db.db import Base
from myifttt.common.db import db


class Users(Base, Base_do):
    """[summary]

    [description]

    Extends:
        Base
        Base_do

    Variables:
        user_id {[type]} -- [description]
        nick_name {[type]} -- [description]
        mobile_num {[type]} -- [description]
        email {[type]} -- [description]
        username {[type]} -- [description]
    """

    # 表的名字:
    __tablename__ = 'users'

    # 表的结构:
    user_id = Column("id", INT, primary_key=True)
    nick_name = Column("nick_name", Text)
    mobile_num = Column("mobile_num", Text)
    email = Column("email", Text)
    username = Column("username", Text)

    @staticmethod
    def get_user_by_username(username=None):
        """根据用户名获取用户

        [description]

        Keyword Arguments:
            username {[type]} -- [description] (default: {None})

        Returns:
            [type] -- [description]
        """
        try:
            session = db.get_session()
            user = session.query(Users).filter(
                Users.username == username).one()
            return user
        finally:
            session.close()
