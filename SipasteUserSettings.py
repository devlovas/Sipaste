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

class SipasteUserSettingsCommand(sublime_plugin.TextCommand):

  def run(self, edit):

    name = os.path.basename(SET_FILE_BACKUP)
    target = os.path.dirname(SET_FILE_BACKUP)

    file_exists = os.path.exists(SET_FILE_BACKUP)
    if not file_exists: copy_file(SET_FILE_SOURCE, target, name)

    self.view.window().open_file(SET_FILE_SOURCE, sublime.TRANSIENT)
