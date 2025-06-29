from .wp_content_puller import WPContentPuller
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QCheckBox, QPushButton, QTextEdit
from pathlib import Path
from config import SITE_URL, OUTPUT_DIR

class PullScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.puller = WPContentPuller()
        # Checkboxes
        self.posts_check = QCheckBox("posts")
        self.pages_check = QCheckBox("pages")
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
            selected.append("posts")
        if self.pages_check.isChecked():
            selected.append("pages")
        if not selected:
            self.text_area.append("No option selected.")
        else:
            self.text_area.append(f"Pulling: {', '.join(selected)}")
            for content_type in selected:
                try:
                    count, folder = self.puller.pull_items(content_type)
                    self.text_area.append(f"Pulled {count} {content_type}. Files saved to {folder}")
                except Exception as e:
                    self.text_area.append(f"Error pulling {content_type}: {e}")


