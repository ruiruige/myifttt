#!/usr/bin/env python
# coding=utf-8
# author = ruiruige
# email = whx20202@gmail.com
"""
检测天气
"""


from oslo_config import cfg

from myifttt.common.config import global_config
from myifttt.common.utils import httputils
from myifttt.common.db import db
from myifttt.common.db.do.weather_info import Weather_info

opts = [
    cfg.StrOpt('weather_key', default="jwrkgdhyjsvbojsg"),
    cfg.StrOpt('weather_user_id', default="UA0BBE5D4F"),
]


def has_already_run():
    """[summary]

    [description]
    """
    pass


def check_should_run():
    """[summary]

    [description]
    """
    session = db.get_session()
    info = session.query(Weather_info).first()
    print info
    session.close()


def run_job():
    """[summary]

    [description]
    """
    pass


def get_weather():
    """[summary]

    [description]
    """
    CONF = global_config.get_conf_from_file(name="weather.conf", opts=opts)

    url = "https://api.seniverse.com/v3/weather/daily.json"
    params = {
        'key': CONF.weather_key,
        'location': "WQJ6YY8MHZP0",
        'language': "zh-Hans",
        'unit': "c"
    }
    resp = httputils.http_get(url=url, params=params)

    check_should_run()


if __name__ == '__main__':
    get_weather()
