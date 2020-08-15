#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import ctypes

# 禁止弹窗指令代码
DETACHED_PROCESS = 0x00000008

CONFIG_FILE_NAME = 'Sipaste.sublime-settings'

ENV_PATH = os.path.split(os.path.realpath(__file__))[0]

CWEBP_EXE = os.path.join(ENV_PATH, 'bin', 'cwebp.exe')
DWEBP_EXE = os.path.join(ENV_PATH, 'bin', 'dwebp.exe')

SET_FILE_SOURCE = os.path.join(ENV_PATH, CONFIG_FILE_NAME)
SET_FILE_BACKUP = os.path.join(ENV_PATH, CONFIG_FILE_NAME + '-backup')

IMAGETOOLS = ctypes.CDLL(os.path.join(ENV_PATH,'lib','IMAGE_TOOLS.dll'))

CONFIG_LIST_ARGS = ['imageSavePath', 'imageTrashPath', 'imageNameInfo', 'imageExts']
