import sys

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication
from windows.MainWindow import MainWindow
from const import APP, PREFS
from preferences import configure, prefs

if __name__ == '__main__':
    # Create the Qt Application
    while True:

        try:
            app = QApplication(sys.argv)
        except RuntimeError:
            app = QCoreApplication.instance()

        configure( APP.NAME, APP.AUTHOR )

        style = prefs().get_pref(PREFS.GLOBAL.NAME, PREFS.GLOBAL.APPSTYLE)
        if style is not None:
            app.setStyle( style )

        # Create and show the form
        form = MainWindow( style=app.style() )
        form.show()

        # Run the main Qt loop
        exit_code = app.exec()
        if exit_code != APP.EXIT_CODE_RESTART:
            sys.exit(exit_code)
        else:
            del app
