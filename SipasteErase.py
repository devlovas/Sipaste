#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import re
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

from SipastePublicUtil import initialize



############################################################
# Define Sublime commands                                  #
############################################################

class SipasteEraseCommand(sublime_plugin.TextCommand):

  def get_view_selected(self):

    """
    获取被鼠标选中的字符串内容

    :return: <string> selected
    """

    return self.view.substr(self.view.sel()[0]).strip()


  def parse_image_name(self, regEx_str):

    """
    按当前匹配规则解析图片名称

    :param regEx_str: <regEx> 路径匹配规则
    :return: <string> image absolute path
    """

    path_result = re.findall(regEx_str, self.get_view_selected())
    if path_result: return os.path.basename(path_result[0])


  def get_image_name(self):

    """
    从图片模板中获取存储图片的路径:

    判断当前被选中的文字是否为输出的字符模板
    条件成立则以该模板的匹配规则解析图片路径

    :return: <string> image name
    """

    # 被选中的文字
    _selected = self.get_view_selected()

    if re.findall('!\[.*?\]\(.*?\)', _selected): return self.parse_image_name('!\[.*?\]\((.*?)\)')
    if re.findall('<img.*?>', _selected): return self.parse_image_name("<img.*?src='(.*?)'.*?")


  def get_image_path(self): return get_image_path(self)


  @initialize
  def run(self, edit):

    try:

      self.source_file = os.path.join(self.image_path[0][0], self.image_name)
      self.target_file = os.path.join(self.image_path[1][0], self.image_name)

      print(self.source_file)
      print(self.target_file)

    except: pass
