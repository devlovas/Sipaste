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

  def template_output_name(self):

    """
    得到字符模板中的图片名称:
    根据配置中"outputTemplate"配置项下最后一个值来判断以图片名称或以图片相对路径来输出

    :return: <string> image name / image path
    """
    return self.template_output_path() if self.params["outputTemplate"][2] else self.image_name


  def template_output_path(self):

    """
    得到字符模板中的图片地址:
    根据配置中"outputTemplate"配置项下最后一个值来判断图片路径以什么形式输出 (绝对/相对路径)

    :return: <string> image path
    """
    image_path = self.image_path[0][1] if self.params["outputTemplate"][2] else self.image_path[0][0]
    return os.path.join(image_path, self.image_name).replace(os.sep, self.params["outputTemplate"][1])


  def get_string_template(self):

    """
    获取字符模板:
    将字符模板中的"占位符"($imagepath ...) 替换为实际值

    :return: <string> string template
    """

    string_template = self.params["outputTemplate"][0]
    string_template = string_template.replace('$imagename', self.template_output_name())
    string_template = string_template.replace('$imagepath', self.template_output_path())

    return string_template


  def insert_string_template(self, edit):

    """
    在当前编辑的文档中光标处插入字符模板

    :param edit: <object> edit
    :return:
    """

    # self.view.sel()[0].a :: 当前光标在文档中的X,Y坐标值
    self.view.insert(edit, self.view.sel()[0].a, self.get_string_template())

  @initialize
  def run(self, edit):

    # 若当前非 Win32环境, 则执行Sublime中的原生paste功能
    if sys.platform != "win32": return self.view.run_command('paste')

    # 检查剪贴板中是否存在图像, 若无图片则执行Sublime中的原生paste功能
    if not IMAGETOOLS.isImageExists(): return self.view.run_command('paste')

    # 将图片保存到本地。 存储成功后在当前编辑的文档中光标处插入字符模板
    save_image(self) and self.insert_string_template(edit)
