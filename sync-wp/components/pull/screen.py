from .wp_content_puller import WPContentPuller
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QCheckBox, QPushButton, QTextEdit, QMessageBox, QGroupBox
from ..config.config_manager import ConfigManager


class PullScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.puller = WPContentPuller()
        self.config_manager = ConfigManager()
        
        # Set up UI components
        self.setup_ui()
        
        # Signal
        self.pull_button.clicked.connect(self.on_pull_clicked)
        
    def setup_ui(self):
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

        content_group = QGroupBox("Content to Pull")
        content_group.setLayout(checkbox_layout)
        
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(content_group)
        main_layout.addWidget(self.pull_button)
        main_layout.addWidget(self.text_area)


    def on_pull_clicked(self):
        # Load auth data from config file
        config_data = self.config_manager.get_config()
        if not config_data:
            self.text_area.append("Error: No configuration found.")
            QMessageBox.warning(
                self,
                "Configuration Missing",
                "Please configure your WordPress authentication credentials in the Config screen."
            )
            return
            
        username = config_data.get('username', '')
        password = config_data.get('password', '')
        auth_method = config_data.get('auth_method', 'application')
        
        selected = []
        if self.posts_check.isChecked():
            selected.append("posts")
        if self.pages_check.isChecked():
            selected.append("pages")
            
        if not selected:
            self.text_area.append("No option selected.")
            return
            
        if not username or not password:
            self.text_area.append("Error: WordPress username and password are required.")
            QMessageBox.warning(
                self,
                "Authentication Missing",
                "Please configure your WordPress authentication credentials in the Config screen."
            )
            return
            
        self.text_area.append(f"Pulling: {', '.join(selected)}")
        for content_type in selected:
            try:
                count, folder = self.puller.pull_items(content_type, username, password, auth_method)
                self.text_area.append(f"Pulled {count} {content_type}. Files saved to {folder}")
            except Exception as e:
                self.text_area.append(f"Error pulling {content_type}: {e}")


