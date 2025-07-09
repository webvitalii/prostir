from .wp_content_puller import WPContentPuller
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QCheckBox, QPushButton, QTextEdit, QMessageBox, QGroupBox
from ..config.config_manager import ConfigManager
from config import CONTENT_TYPES


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
        # Content type checkboxes
        self.content_type_checkboxes = {}
        
        # Pull button
        self.pull_button = QPushButton("Pull")
        
        # Text area for output
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        
        # Layouts
        checkbox_layout = QHBoxLayout()
        
        # Create checkboxes dynamically based on config
        for content_type in CONTENT_TYPES:
            # Capitalize first letter for display
            display_name = content_type.capitalize()
            checkbox = QCheckBox(display_name)
            self.content_type_checkboxes[content_type] = checkbox
            checkbox_layout.addWidget(checkbox)

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
        application_password = config_data.get('application_password', '')
        
        selected = []
        for content_id, checkbox in self.content_type_checkboxes.items():
            if checkbox.isChecked():
                selected.append(content_id)
            
        if not selected:
            self.text_area.append("No option selected.")
            return
            
        if not username or not application_password:
            self.text_area.append("Error: WordPress username and application password are required.")
            QMessageBox.warning(
                self,
                "Authentication Missing",
                "Please configure your WordPress authentication credentials in the Config screen."
            )
            return
            
        self.text_area.append(f"Pulling: {', '.join(selected)}")
        for content_type in selected:
            try:
                count, folder = self.puller.pull_items(content_type, username, application_password)
                self.text_area.append(f"Pulled {count} {content_type}. Files saved to {folder}")
            except Exception as e:
                self.text_area.append(f"Error pulling {content_type}: {e}")


