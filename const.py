import logging


class Const:
    LOG_LEVEL = logging.INFO

    class CATEGORY:
        ALL = "All"
        BLURRY = "Blurry"
        ERRORED = "Errored"

        @staticmethod
        def keys():
            return [Const.CATEGORY.ALL, Const.CATEGORY.BLURRY, Const.CATEGORY.ERRORED]

    class STR:
        NOTHING_SCANNED = "(Nothing scanned yet.)"
        PATH = "path"
