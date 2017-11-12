#!/usr/bin/env python
# coding=utf-8
# author = ruiruige
# email = whx20202@gmail.com
"""管理插件的utils

[description]
"""

import os
import imp

from myifttt import plugins


def get_plugin_modules():
    """导入内置插件

    [description]
    """
    plugins_path = plugins.__path__[0]

    path_list = os.listdir(plugins_path)
    # 过滤掉下划线开头的
    path_list = [x for x in path_list if not x.startswith("_")]
    # 生成绝对路径
    path_list = [os.path.join(plugins_path, x) for x in path_list]
    # 过滤掉文件夹
    path_list = [x for x in path_list if os.path.isfile(x)]
    # 保留.py结尾的
    path_list = [x for x in path_list if x.endswith(".py")]

    for path in path_list:
        file_name = os.path.dirname(path)
        module_name = file_name[file_name.rfind(".") + 1:]
        _module = imp.load_source(module_name, path)
        print(_module)
        print(dir(_module))
