from windows.MainWindow import MainWindow
from windows.components.FilterBar import FilterBar


class MainWindowController():
    def __init__(self, app):
        self.main_win = None
        self.filter_bar = None
        self.progress_bar = None
        self.progress_label = None

        self.qapp = app

    def start_er_up(self):
        self.main_win = MainWindow( style=self.qapp.style() )
        self.main_win.show()


