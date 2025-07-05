from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout,
                              QFormLayout, QGroupBox, QRadioButton, QLabel, 
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
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Auth group box
        auth_group = QGroupBox("WordPress Authentication")
        auth_layout = QFormLayout()
        
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()

        
        auth_layout.addRow("Username:", self.username_input)
        auth_layout.addRow("Application Password:", self.password_input)
        

        
        # Help text
        help_text = (
            "Note: For WordPress REST API, you typically need to use an Application Password.\n"
            "You can create one in your WordPress admin under Users → Profile → Application Passwords."
        )
        help_label = QLabel(help_text)
        help_label.setWordWrap(True)
        auth_layout.addRow("", help_label)
        
        auth_group.setLayout(auth_layout)
        
        # Site info
        site_info_group = QGroupBox("Site Information")
        info_layout = QVBoxLayout()
        self.site_label = QLabel(f"Site URL: {SITE_URL}")
        info_layout.addWidget(self.site_label)
        site_info_group.setLayout(info_layout)
        
        # Save button
        self.save_button = QPushButton("Save Configuration")
        self.save_button.clicked.connect(self.save_config)
        
        # Add components to main layout
        main_layout.addWidget(site_info_group)
        main_layout.addWidget(auth_group)
        main_layout.addWidget(self.save_button)
        
    def get_auth_data(self):
        """Get authentication data from the config screen"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        auth_method = "application"
        
        return {
            "username": username,
            "password": password,
            "auth_method": auth_method
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
            if "password" in config_data:
                self.password_input.setText(config_data["password"])

        except Exception as e:
            print(f"Error loading configuration: {str(e)}")
