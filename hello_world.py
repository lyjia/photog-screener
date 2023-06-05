import sys
from PySide6.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout, QTableWidget,QTableWidgetItem
from PySide6.QtGui import QColor

colors = [("Red", "#FF0000"),
          ("Green", "#00FF00"),
          ("Blue", "#0000FF"),
          ("Black", "#000000"),
          ("White", "#FFFFFF"),
          ("Electric Green", "#41CD52"),
          ("Dark Blue", "#222840"),
          ("Yellow", "#F9E56d")]

def get_rgb_from_hex(code):
    code_hex = code.replace("#", "")
    rgb = tuple(int(code_hex[i:i+2], 16) for i in (0, 2, 4))
    return QColor.fromRgb(rgb[0], rgb[1], rgb[2])

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("My Form")

        # Create widgets
        table = QTableWidget()
        table.setRowCount(len(colors))
        table.setColumnCount(len(colors[0]) + 1)
        table.setHorizontalHeaderLabels(["Name", "Hex Code", "Color"])

        for i, (name, code) in enumerate(colors):
            item_name = QTableWidgetItem(name)
            item_code = QTableWidgetItem(code)
            item_color = QTableWidgetItem()
            item_color.setBackground(get_rgb_from_hex(code))
            table.setItem(i, 0, item_name)
            table.setItem(i, 1, item_code)
            table.setItem(i, 2, item_color)

        # Create layout and add widgets
        layout = QVBoxLayout(self)
        layout.addWidget(table)




if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)

    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec())
