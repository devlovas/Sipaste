#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import sublime
import sublime_plugin


# 将当前脚本执行的绝对路径添加至 PY环境变量中
ENV_PATH = os.path.dirname(os.path.realpath(__file__))
not ENV_PATH in sys.path and sys.path.append(ENV_PATH)


############################################################
# Import external resources                                #
############################################################

from SipasteImageUtil import get_image_path
from SipasteImageUtil import get_image_name

from SipastePublicUtil import initialize

class SipasteCommand(sublime_plugin.TextCommand):

  def get_image_name(self): return get_image_name(self)

  def get_image_path(self): return get_image_path(self)

  @initialize
  def run(self, edit):

    print(self.image_name)
    print(self.image_path)
