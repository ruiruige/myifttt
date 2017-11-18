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
    """获取内置插件模块列表

    从对应目录获取文件名，依次导入模块
    最后返回模块的列表
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

    module_list = []
    for path in path_list:
        file_name = os.path.dirname(path)
        module_name = file_name[file_name.rfind(".") + 1:]
        # 从文件名加载模块
        _module = imp.load_source(module_name, path)
        module_list.append(_module)
    return module_list
