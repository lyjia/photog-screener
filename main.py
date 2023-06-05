import sys
from PySide6.QtWidgets import QApplication
from windows.MainWindow import MainWindow

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)

    # Create and show the form
    form = MainWindow()
    form.show()

    # Run the main Qt loop
    sys.exit(app.exec())
