#!/usr/bin/env python
# coding=utf-8
# author = ruiruige
# email = whx20202@gmail.com
# pylint: disable=W0621
"""http工具类

[description]
"""

from requests import Request, Session


def http_get(url=None, params=None, headers=None, verify=True,
             timeout=10, encoding="utf-8"):
    """[summary]

    [description]

    Keyword Arguments:
        url {[type]} -- [description] (default: {None})
        params {[type]} -- [description] (default: {None})
        headers {[type]} -- [description] (default: {None})
        verify {bool} -- [description] (default: {True})
        timeout {number} -- [description] (default: {10})

    Returns:
        [type] -- [description]
    """
    session = Session()
    preparedRequest = Request('GET', url,
                              params=params,
                              headers=headers).prepare()
    resp = session.send(preparedRequest,
                        verify=verify,
                        timeout=timeout)
    resp.encoding = encoding
    return resp


if __name__ == '__main__':
    resp = http_get(url="https://www.baidu.com")
    print resp.status_code
    print resp.text
