#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sublime


############################################################
# Import external resources                                #
############################################################

from SipasteConst import CONFIG_FILE_NAME
from SipasteConst import CONFIG_LIST_ARGS


def convert_path(path):

  """
  根据当前系统平台将路径中的分隔符
  转换为当前系统所支持的路径分隔符

  :param path: <string>
  :return: <string> path
  """

  sep_path = r'\/'.replace(os.sep, '')
  return path.replace(sep_path, os.sep) if sep_path in path else path

def load_settings(self):

  """
  将加载的配置值添至主类 params属性中

  :return:
  """

  settings = sublime.load_settings(CONFIG_FILE_NAME)
  for item in CONFIG_LIST_ARGS: self.params.update({ item: settings.get(item) })


def initialize(fn):

  """
  加载程序所需的配置信息

  :param fn: <function> run 函数
  :retrun: <function> wrapper
  """

  def wrapper(*args, **kwargs):

    """
    加载程序所需的配置参数

    :return: <any> fn => run func result
    """

    try:

      args[0].params = {}
      load_settings(args[0])

      args[0].file_path = os.path.dirname(args[0].view.file_name())       # 当前编辑的文件路径
      args[0].file_name = os.path.basename(args[0].view.file_name())      # 当前编辑的文件名称

      args[0].image_name = args[0].get_image_name()    # 获取图片名称
      args[0].image_path = args[0].get_image_path()    # 获取图片路径

      return fn(*args, **kwargs)  # 执行 "run"方法

    except: pass

  return wrapper



def copy_file(source_path, target_path, new_name=None, binary=True):

  """
  拷贝文件：

  :param source_path: <string>  : 原始文件路径
  :param target_path: <string>  : 目标文件路径
  :param [binary (:True)]: <boolean>  : 文件是否以二进制方式打开
  :param [new_name (:None)]: <string> : 指定新的名称，默认为源文件名
  :return: <boolean> file copy result
  """

  try:
    if not os.path.exists(target_path): os.makedirs(target_path)                                         # 目标目录不存在则创建
    target_path = os.path.join(target_path, new_name if new_name else os.path.split(source_path)[1])     # 包含文件名的目标目录

    with open(source_path, 'rb' if binary else 'r') as fs:
      with open(target_path, 'wb' if binary else 'w') as ft: ft.write(fs.read())                         # 将文件移动到目标目录

    return True

  except: return False


def move_file(source_path, target_path, new_name=None, binary=True):

  """
  移动文件：

  :param source_path: <string>  : 源文件路径
  :param target_path: <string>  : 目标地路径
  :param [binary (:True)]: <boolean>  : 文件是否以二进制方式打开
  :param [new_name (:None)]: <string> : 指定新的名称，默认为源文件名
  :return: <boolean> file move result
  """

  try:

    result = copy_file(source_path, target_path, new_name, binary)
    result = os.remove(source_path) if result else result                                                # 删除已拷贝的原始文件

    return result is None

  except: return False
