#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import re
import time
import base64
import hashlib
import subprocess


############################################################
# Import external resources                                #
############################################################

from threading import Thread

from SipasteConst import CWEBP_EXE
from SipasteConst import DWEBP_EXE
from SipasteConst import IMAGETOOLS
from SipasteConst import DETACHED_PROCESS

from SipastePublicUtil import copy_file
from SipastePublicUtil import convert_path


def async(fn):

  """
  给接收到的函数开启新线程

  :return: <function>
  """

  return lambda *args, **kwargs: Thread(target = fn, args = args, kwargs = kwargs).start()



############################################################
# Format conversion                                        #
############################################################

def parse_type_webp(self, primary_file, _webp, _png):

  """
  图像格式转换: webp

  :param primary_file: <string>
  :param _webp: <string>
  :param _png: <string>
  :return:
  """

  if "png" in self.params['imageExts']: return
  subprocess.call('%s -lossless %s -o %s' %(CWEBP_EXE, primary_file, _webp), creationflags=DETACHED_PROCESS)


def parse_type_bmp(self, primary_file, _webp, _png):

  """
  图像格式转换: bmp

  :param primary_file: <string>
  :param _webp: <string>
  :param _png: <string>
  :return:
  """
  _paths = os.path.split(primary_file)
  copy_file(primary_file, _paths[0], new_name=_paths[1]+'.bmp')


def parse_type_png(self, primary_file, _webp, _png):

  """
  图像格式转换: png

  :param primary_file: <string>
  :param _webp: <string>
  :param _png: <string>
  :return:
  """
  subprocess.call('%s -lossless "%s" -o "%s"' %(CWEBP_EXE, primary_file, _webp), creationflags=DETACHED_PROCESS)
  subprocess.call('%s  "%s" -o "%s"' %(DWEBP_EXE, _webp, _png), creationflags=DETACHED_PROCESS)
  not "webp" in self.params['imageExts'] and os.remove(_webp)


def handling_method_image_type():

  """
  图像格式转换接口:

  :return: <function> handling method
  """
  return { "webp" : parse_type_webp, "bmp"  : parse_type_bmp, "png"  : parse_type_png }


@async # 开启新线程执行"外部命令"(cwebp)，防止程序阻塞
def image_format_conversion(self, primary_file):

  """
  图片类型转换:
  通过 CWEBP 和 DWEBP 工具将图片格式转换为配置文件中给定的图片格式
  注意： 目前仅支持 *.* -> *.webp / *.webp -> *.png 图片类型转换

  :param primary_file: <string> 图片存储路径，带名称后缀
  :return:
  """
  try:

    handling = handling_method_image_type()

    for imageExt in self.params['imageExts']:
      handling[imageExt](self, primary_file, primary_file+'.webp', primary_file+'.png')

    os.remove(primary_file)

  except: pass



############################################################
# Image Important method                                   #
############################################################

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

  return [convert_path(abs_save_path), convert_path(rel_save_path)]


def get_image_path(self):

  """
  获取图片路径:
  根据配置文件中给出的"图片存储/回收地址"，得到一个带名称后缀的完整的图片存储路径

  :return: <list> Image paths : 图片绝对/相对路径
  """

  save_path_list = parse_image_path(self, self.file_path, 'imageSavePath')
  trash_path_list = parse_image_path(self, save_path_list[0], 'imageTrashPath')

  return [save_path_list, trash_path_list]


def save_image(self):

  """
  将剪贴板中的图像保存到本地

  :return: <boolean> Save the result of the image
  """

  image_save_path = os.path.join(self.image_path[0][0], self.image_name)    # 图片存储路径

  if not os.path.exists(self.image_path[0][0]): os.makedirs(self.image_path[0][0])                              # 若指定路径不存在则进行路径创建
  result_of_image_saving = IMAGETOOLS.saveImage( image_save_path[:image_save_path.rfind('.')].encode('gbk') )   # 将剪贴板中的图片保存到指定路径


  # 若图片存储失败，则中断程序执行并向用户反馈其失败原因
  if result_of_image_saving == 1: return sublime.error_message('Sipaste::  Error! The contents of the clipboard are not in DIB format ！')
  if result_of_image_saving == 2: return sublime.error_message('Sipaste::  Error! Failed to open clipboard ！')
  if result_of_image_saving == 3: return sublime.error_message('Sipaste::  Error! Path is not accessible ！')
  if result_of_image_saving == 0: print('Sipaste:: Successful! image save address "%s"' % image_save_path)

  image_format_conversion(self, image_save_path[:image_save_path.rfind('.')])     # 根据配置文件中给出的图片类型对图片进行类型转换

  return True
