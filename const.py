import logging
import os

LOG_LEVEL = logging.INFO


class CATEGORY:
    ALL = "All"
    BLURRY = "Blurry"
    ERRORED = "Errored"

    @staticmethod
    def keys():
        return [CATEGORY.ALL, CATEGORY.BLURRY, CATEGORY.ERRORED]


class STR:
    NOTHING_SCANNED = "(Nothing scanned yet.)"
    PATH = "path"
    if os.name == 'nt':
        TRASH = "Recycle Bin"
    else:
        TRASH = "Trash"


class APP:
    NAME = "PhotogScreener"
    AUTHOR = "Lyjia"
    EXIT_CODE_RESTART = 42069


class PREFS:
    class GLOBAL:
        NAME = "global"
        APPSTYLE = "app style"
        ON_REMOVAL_ACTION = "on removal"


class MENU:
    class ON_REMOVAL:
        TO_TRASH = "Send to %s" % STR.TRASH
        DELETE = "Delete"

        @staticmethod
        def keys():
            return [MENU.ON_REMOVAL.TO_TRASH, MENU.ON_REMOVAL.DELETE]
