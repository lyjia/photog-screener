from PySide6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QVBoxLayout


class MassDeleteConfirmation(QDialog):
    def __init__(self, target_images):
        super().__init__()

        self.setWindowTitle("Are you ABSOLUTELY sure?")
        self.target_images = target_images

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("You are about to PERMANENTLY DELETE all checked images, are you sure you wish to do this?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)