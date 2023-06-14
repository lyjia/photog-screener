# Python preference interface


import toml
from appdirs import AppDirs
from pathlib import Path, PurePath
import os

prefs = None
def configure(appname=None, appauthor=None, version=None, prefsfilename=None):
    prefs = Preferences(appname, appauthor, version, prefsfilename)

class Preferences:
    def __init__(self, appname, appauthor, version=None, prefsfilename=None):
        if prefsfilename is not None:
            self.prefs_filename = prefsfilename + '.toml'
        else:
            self.prefs_filename = 'config' + '.toml'

        self.app_name = appname
        self.app_author = appauthor

        self.pref_hash = {}

        if version is not None:
            self.appdirs = AppDirs(self.app_name, self.app_author, version=version)
        else:
            self.appdirs = AppDirs(self.app_name, self.app_author)

        self.prefs_fullpath = os.path.join(self.get_user_data_dir(), self.prefs_filename)

        try:
            with open(self.prefs_fullpath) as fil:
                self.prefs_hash = toml.loads(fil.read())
        except FileNotFoundError:
            pass #dont need to do anything

    def get_user_data_dir(self):
        return self.appdirs.user_data_dir

    def get_site_data_dir(self):
        return self.appdirs.site_data_dir

    def get_user_cache_dir(self):
        return self.appdirs.user_cache_dir

    def get_user_log_dir(self):
        return self.appdirs.user_log_dir

    ###################################
    # preference interface
    ###################################

    def get_pref(self, category, keyname, default_value=None):
        if self.prefs_hash[category] or self.prefs_hash[category][keyname] is None:
            return default_value
        return self.prefs_hash[category][keyname]

    def set_pref(self, category, keyname, value, persist=True):
        if self.prefs_hash[category] is None:
            self.prefs_hash[category] = {}

        self.prefs_hash[category][keyname] = value

        if persist is True:
            self.persist()

    def persist(self):
        os.makedirs( self.get_user_data_dir(), exist_ok=True)

        with open(self.prefs_fullpath, 'w') as file:
            file.print( toml.dump( self.prefs_hash ) )
