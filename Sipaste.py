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

from SipasteImageUtil import save_image 
from SipasteImageUtil import get_image_path
from SipasteImageUtil import get_image_name

from SipasteConst import IMAGETOOLS
from SipastePublicUtil import initialize


############################################################
# Define Sublime commands                                  #
############################################################

class SipasteCommand(sublime_plugin.TextCommand):

  def get_image_name(self): return get_image_name(self)

  def get_image_path(self): return get_image_path(self)

  @initialize
  def run(self, edit):

    # 若当前非 Win32环境, 则执行Sublime中的原生paste功能
    if sys.platform != "win32": return self.view.run_command('paste')

    # 检查剪贴板中是否存在图像, 若无图片则执行Sublime中的原生paste功能
    if not IMAGETOOLS.isImageExists(): return self.view.run_command('paste')

    # 将图片保存到本地。 存储成功后在当前编辑的文档中光标处插入字符模板
    save_image(self)
