from PySide6.QtWidgets import (QWidget, QVBoxLayout,
                              QFormLayout, QGroupBox, QLabel, 
                              QLineEdit, QPushButton, QMessageBox)
from config import SITE_URL
from .config_manager import ConfigManager


class ConfigScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        
        # Setup UI components
        self.setup_ui()
        
        # Load saved configuration if it exists
        self.load_config()
    
    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        auth_group = QGroupBox("WordPress Authentication")
        auth_layout = QFormLayout()
        
        self.username_input = QLineEdit()
        self.application_password_input = QLineEdit()
        
        auth_layout.addRow("Username:", self.username_input)
        auth_layout.addRow("Application Password:", self.application_password_input)

        help_text = (
            "Note: For WordPress REST API, you typically need to use an Application Password.\n"
            "You can create one in your WordPress admin under Users → Profile → Application Passwords."
        )
        help_label = QLabel(help_text)
        help_label.setWordWrap(True)
        auth_layout.addRow("", help_label)
        
        auth_group.setLayout(auth_layout)

        site_info_group = QGroupBox("Site Information")
        info_layout = QVBoxLayout()
        self.site_label = QLabel(f"Site URL: {SITE_URL}")
        info_layout.addWidget(self.site_label)
        site_info_group.setLayout(info_layout)

        self.save_button = QPushButton("Save Configuration")
        self.save_button.clicked.connect(self.save_config)

        main_layout.addWidget(site_info_group)
        main_layout.addWidget(auth_group)
        main_layout.addWidget(self.save_button)
        
    def get_auth_data(self):
        """Get authentication data from the config screen"""
        username = self.username_input.text().strip()
        application_password = self.application_password_input.text().strip()
        
        return {
            "username": username,
            "application_password": application_password
        }
        
    def save_config(self):
        """Save configuration to JSON file"""
        try:
            config_data = self.get_auth_data()
            self.config_manager.save_config(config_data)
            
            QMessageBox.information(
                self,
                "Configuration Saved",
                "Authentication settings have been saved successfully."
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error Saving Configuration",
                f"Could not save configuration: {str(e)}"
            )
    
    def load_config(self):
        """Load configuration from JSON file if it exists"""
        try:
            config_data = self.config_manager.get_config()
            if not config_data:
                return

            if "username" in config_data:
                self.username_input.setText(config_data["username"])
            
            # Only use application_password
            if "application_password" in config_data:
                self.application_password_input.setText(config_data["application_password"])

        except Exception as e:
            print(f"Error loading configuration: {str(e)}")
