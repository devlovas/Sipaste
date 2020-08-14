#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import sublime
import sublime_plugin


# 将当前脚本执行的绝对路径添加至 PY环境变量中
ENV_PATH = os.path.dirname(os.path.realpath(__file__))
not ENV_PATH in sys.path and sys.path.append(ENV_PATH)


class SipasteCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    pass
