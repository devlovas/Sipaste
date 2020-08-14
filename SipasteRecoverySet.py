import os
import sublime
import sublime_plugin


############################################################
# Import external resources                                #
############################################################

from SipasteConst import SET_FILE_SOURCE
from SipasteConst import SET_FILE_BACKUP

from SipastePublicUtil import copy_file



############################################################
# Define Sublime commands                                  #
############################################################

class SipasteRecoverySetCommand(sublime_plugin.TextCommand):
  
  def run(self, edit):

    name = os.path.basename(SET_FILE_SOURCE)
    target = os.path.dirname(SET_FILE_SOURCE)

    sel_result = sublime.ok_cancel_dialog('Sipaste:: You will restore the configuration, Do you want to continue?')
    sel_result and copy_file(SET_FILE_BACKUP, target, name)
