# Python preference interface


import toml
from appdirs import AppDirs
from pathlib import Path, PurePath
import os
import logging
import const

logging.basicConfig(level=const.LOG_LEVEL)

_prefs_internal = None


def configure(appname=None, appauthor=None, version=None, prefsfilename=None):
    global _prefs_internal
    _prefs_internal = Preferences(appname, appauthor, version, prefsfilename)


def prefs():
    return _prefs_internal


class Preferences:
    def __init__(self, appname, appauthor, version=None, prefsfilename=None):
        if prefsfilename is not None:
            self.prefs_filename = prefsfilename + '.toml'
        else:
            self.prefs_filename = 'config' + '.toml'

        self.app_name = appname
        self.app_author = appauthor

        self.prefs_hash = {}

        if version is not None:
            self.appdirs = AppDirs(self.app_name, self.app_author, version=version)
        else:
            self.appdirs = AppDirs(self.app_name, self.app_author)

        self.prefs_fullpath = os.path.join(self.get_user_data_dir(), self.prefs_filename)

        try:
            with open(self.prefs_fullpath) as fil:
                self.prefs_hash = toml.loads(fil.read())
        except FileNotFoundError:
            pass  # dont need to do anything

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
        if category not in self.prefs_hash:
            self.prefs_hash[category] = {}

        if keyname not in self.prefs_hash[category]:
            self.prefs_hash[category][keyname] = None

        if self.prefs_hash[category][keyname] is None:
            logging.info("Preference lookup for '%s'.'%s' has no value, returning default value: %s (%s)" % (
                category, keyname, default_value, default_value.__class__.__name__))
            return default_value

        value = self.prefs_hash[category][keyname]
        logging.info("Preference lookup for '%s'.'%s', returning value: %s (%s)" % (category, keyname, value, value.__class__.__name__))
        return value

    def set_pref(self, category, keyname, value, persist=True):
        if self.prefs_hash[category] is None:
            self.prefs_hash[category] = {}

        logging.info("Preference '%s'.'%s' set to: %s (%s)" % (category, keyname, value, value.__class__.__name__))
        self.prefs_hash[category][keyname] = value

        if persist is True:
            self.persist()

    def persist(self):
        os.makedirs(self.get_user_data_dir(), exist_ok=True)

        with open(self.prefs_fullpath, 'w') as file:
            file.write(toml.dumps(self.prefs_hash))
