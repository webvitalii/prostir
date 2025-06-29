from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QCheckBox, QPushButton, QTextEdit

class PullScreen(QWidget):
    def __init__(self):
        super().__init__()
        # Checkboxes
        self.posts_check = QCheckBox("Posts")
        self.pages_check = QCheckBox("Pages")
        # Pull button
        self.pull_button = QPushButton("Pull")
        # Text area for output
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        # Layouts
        checkbox_layout = QHBoxLayout()
        checkbox_layout.addWidget(self.posts_check)
        checkbox_layout.addWidget(self.pages_check)
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(checkbox_layout)
        main_layout.addWidget(self.pull_button)
        main_layout.addWidget(self.text_area)
        # Signal
        self.pull_button.clicked.connect(self.on_pull_clicked)

    def on_pull_clicked(self):
        selected = []
        if self.posts_check.isChecked():
            selected.append("Posts")
        if self.pages_check.isChecked():
            selected.append("Pages")
        if not selected:
            self.text_area.append("No option selected.")
        else:
            self.text_area.append(f"Pulling: {', '.join(selected)}")
            # TODO: implement pull logic using WP REST API
