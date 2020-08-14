#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os

CONFIG_FILE_NAME = 'Sipaste.sublime-settings'

ENV_PATH = os.path.split(os.path.realpath(__file__))[0]

SET_FILE_SOURCE = os.path.join(ENV_PATH, CONFIG_FILE_NAME)
SET_FILE_BACKUP = os.path.join(ENV_PATH, CONFIG_FILE_NAME + '-backup')
