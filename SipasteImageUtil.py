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
