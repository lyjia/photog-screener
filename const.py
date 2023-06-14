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
