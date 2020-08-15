#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import re
import time
import base64
import hashlib


def get_image_name(self, _name = ''):

  """
  获取图片名称:
  通过当前时间戳得到一个指定类型的图片名称

  :return: <string> image name : 带后缀的图上名称
  """
  _basename = self.params['imageNameInfo']
  timestamp = str(time.time()).split('.')[0]

  if _basename[1][0] == 'md5': _name = hashlib.md5(timestamp.encode('utf-8')).hexdigest()
  if _basename[1][0] == 'base64': _name = re.sub("b'|'", '', str( base64.b64encode(timestamp.encode('utf-8'))))
  if _basename[1][0] == 'datetime': _name = time.strftime("%Y%m%d%H%M%S", time.localtime(int(timestamp)))
  if _basename[1][0] == 'timestamp': _name = timestamp

  return _basename[0].replace('$basename', _name[0:_basename[1][1]] +'.'+ self.params['imageExts'][0])


def parse_image_path(self, _path, type):

  """
  得到图片完整路径

  :param _path: <string> Current edit file path
  :param type: <string> Image path type
  :return: <list> Full path of image
  """

  file_name = self.file_name                              # 当前编辑的文件名称
  file_path = _path.split(os.sep)                         # 文件路径(列表形式)

  rel_save_path = self.params[type].replace('^./', '')    # 删除路径前缀标识符
  rel_save_path = rel_save_path.replace('$filename', file_name[:file_name.rfind('.')])    # 将路径中的占位符替换为当前编辑的文件名称
  abs_save_path = os.sep.join(file_path[:len(file_path) - rel_save_path.count('../')])    # 以当前给出的路径作为参考计算该路径的相对地址
  abs_save_path = os.path.join(abs_save_path, rel_save_path.replace('../', ''))           # 按配置中给出的路径与计算得到的相对地址进行拼接，得绝对存储路径

  return [abs_save_path, rel_save_path]


def get_image_path(self):

  """
  获取图片路径:
  根据配置文件中给出的"图片存储/回收地址"，得到一个带名称后缀的完整的图片存储路径

  :return: <list> Image paths : 图片绝对/相对路径
  """

  save_path_list = parse_image_path(self, self.file_path, 'imageSavePath')
  trash_path_list = parse_image_path(self, save_path_list[0], 'imageTrashPath')

  return [save_path_list, trash_path_list]
