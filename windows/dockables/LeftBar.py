import sys
from PySide6.QtWidgets import QMainWindow, QWidget, QLineEdit, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem, \
    QDockWidget
from PySide6.QtGui import QColor, Qt


class LeftBar(QWidget):
    def __init__(self):
        super().__init__()
