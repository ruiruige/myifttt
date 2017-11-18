#!/usr/bin/env python
# coding=utf-8
# author = ruiruige
# email = whx20202@gmail.com
"""天气接口的底层driver

[description]
"""

from oslo_config import cfg

from myifttt.common.config import global_config
from myifttt.common.utils import httputils
from myifttt.common.db import db
from myifttt.common.db.do import weather_info, push_log
from myifttt.common.log.log import getLogger

LOG = getLogger(__name__)

opts = [
    cfg.StrOpt('weather_api_key', default="jwrkgdhyjsvbojsg"),
    cfg.StrOpt('weather_api_user_id', default="UA0BBE5D4F"),
]


class Weather_driver(object):
    """天气driver

    暂时抽象出来只是为了代码简洁
    如果以后有多API接口的想法可以做正规

    Variables:
        ] {[type]} -- [description]
    """

    CONF = global_config.get_plugin_conf_from_file(
        name="weather", opts=opts)
    bad_text_list = [
        "雷阵雨", "雷阵雨伴有冰雹", "小雨", "中雨", "大雨", "暴雨", "大暴雨",
        "特大暴雨", "冻雨", "雨夹雪", "阵雪", "小雪", "中雪", "大雪", "暴雪",
        "浮尘", "扬沙", "雾", "霾"]

    def __init__(self, task=None):

        self.weather_api_key = Weather_driver.CONF.weather_api_key
        self.url = "https://api.seniverse.com/v3/weather/daily.json"
        self.today_data = None
        self.tomorrow_data = None
        self.city_id = None
        # 城市别名，给人看的名字
        self.city_alias = None
        self.task = task

    def retrieve_2_day_weather(self):
        """按地点获取今明两天天气

        [description]

        Returns:
            dict -- 今天天气数据
            dict -- 明天天气数据
        Raises:
            Exception -- [description]
        """

        params = {
            'key': self.weather_api_key,
            'location': self.task.city_id,
            'language': "zh-Hans",
            'unit': "c",
            'start': 0,
            'days': 2
        }
        resp = httputils.http_get(url=self.url, params=params)
        if resp.status_code not in [200]:
            raise Exception("API返回非200状态码")

        resp_json = resp.json()
        print resp_json
        daily_data = resp_json["results"][0]["daily"]

        # 保存解析出来的变量
        self.today_data = daily_data[0]
        self.tomorrow_data = daily_data[1]
        self.city_alias = resp_json["results"][0]["location"]["name"]
        self.city_id = resp_json["results"][0]["location"]["id"]

        LOG.info("明日夜间天气%s", self.get_tomorrow_night_text())
        LOG.info("明日白天天气%s", self.get_tomorrow_day_text())
        LOG.info("明日最高温度%d", self.get_tomorrow_high())
        LOG.info("明日最低温度%d", self.get_tomorrow_low())
        LOG.info("今日最高温度%d", self.get_today_high())
        LOG.info("今日最低温度%d", self.get_today_low())

    def get_tomorrow_day_text(self):
        """明日白天天气

        [description]

        Returns:
            [type] -- [description]
        """
        return self.tomorrow_data["text_day"].encode('utf-8')

    def get_tomorrow_night_text(self):
        """明日晚上天气

        [description]

        Returns:
            [type] -- [description]
        """
        return self.tomorrow_data["text_night"].encode('utf-8')

    def get_tomorrow_high(self):
        """[summary]

        [description]
        """
        return int(self.tomorrow_data["high"])

    def get_tomorrow_low(self):
        """[summary]

        [description]
        """
        return int(self.tomorrow_data["low"])

    def get_today_high(self):
        """[summary]

        [description]
        """
        return int(self.today_data["high"])

    def get_today_low(self):
        """[summary]

        [description]
        """
        return int(self.today_data["low"])

    def is_tomorrow_weather_bad(self):
        """[summary]

        [description]

        Keyword Arguments:
            task {[type]} -- [description] (default: {None})

        Returns:
            bool -- [description]
        """
        tomorrow_high = self.get_tomorrow_high()
        tomorrow_low = self.get_tomorrow_low()

        today_high = self.get_today_high()
        today_low = self.get_today_low()

        # 第二天高温大于第一天
        if tomorrow_high - today_high >= self.task.ge_high_delta_watermark:
            return True
        # 第二天高温低于第一天
        elif today_high - tomorrow_high >= self.task.le_high_delta_watermark:
            return True
        # 第二天低温大于第一天
        elif tomorrow_low - today_low >= self.task.ge_low_delta_watermark:
            return True
        # 第二天低温小于第一天
        elif today_low - tomorrow_low >= self.task.le_low_delta_watermark:
            return True
        elif self.get_tomorrow_day_text in Weather_driver.bad_text_list or \
                self.get_tomorrow_night_text in Weather_driver.bad_text_list:
            return True

        return False

    def generate_warning_text(self):
        """[summary]

        [description]
        """
        text = """尊敬的%s, 今天最高气温%d, 最低气温%d, 明日最高气温%d, 最低气温%d, 明日早晨天气%s,
        明日夜间天气%s。请注意天气，安排出行"""
        text_template = ("尊敬的%s, 今天最高气温%d, 最低气温%d, 明日最高气温%d,"
                         " 最低气温%d, 明日早晨天气%s,明日夜间天气%s。请注意天气，安排出行")
        text = text_template % (
            self.task.user,
            self.get_today_high(),
            self.get_today_low(),
            self.get_tomorrow_high(),
            self.get_tomorrow_low(),
            self.get_tomorrow_day_text(),
            self.get_tomorrow_night_text()
        )

        LOG.info(text)
        return text

    def pre_push_warning_text(self):
        """推送天气告警之前要执行的函数

        主要分为保存天气日志和保存推送记录
        """
        # 保存天气日志
        info = weather_info.Weather_info()
        info.city_alias = self.city_alias
        info.city_id = self.city_id
        info.city_name = self.city_alias
        info.today_temperature_high = self.get_today_high()
        info.today_temperature_low = self.get_today_low()
        info.tomorrow_temperature_high = self.get_tomorrow_high()
        info.tomorrow_temperature_low = self.get_tomorrow_low()
        info.text_day = self.get_tomorrow_day_text()
        info.text_night = self.get_tomorrow_night_text()

        pushlog = push_log.Push_log()
        pushlog.push_method = self.task.push_method
        pushlog.push_user = self.task.user
        pushlog.push_plugin = "weather"
        pushlog.plugin_push_reason = "bad weather"
        pushlog.task_id = self.task.task_id

        session = db.get_session()
        try:
            session.add(info)
            session.add(pushlog)
            session.commit()
        finally:
            session.close()
