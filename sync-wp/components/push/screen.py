from .wp_content_pusher import WPContentPusher
from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QCheckBox, 
                              QPushButton, QTextEdit, QLabel, QLineEdit, 
                              QFormLayout, QGroupBox, QRadioButton, QMessageBox)
from pathlib import Path
from config import SITE_URL, OUTPUT_DIR

class PushScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.pusher = WPContentPusher()
        
        # Create UI components
        self.setup_ui()
        
        # Connect signals
        self.push_button.clicked.connect(self.on_push_clicked)
        
    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Auth group box
        auth_group = QGroupBox("WordPress Authentication")
        auth_layout = QFormLayout()
        
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        
        auth_layout.addRow("Username:", self.username_input)
        auth_layout.addRow("Password:", self.password_input)
        
        # Auth method selection
        auth_method_layout = QHBoxLayout()
        self.basic_auth_radio = QRadioButton("Basic Auth")
        self.app_password_radio = QRadioButton("Application Password")
        self.app_password_radio.setChecked(True)  # Recommended option
        
        auth_method_layout.addWidget(self.basic_auth_radio)
        auth_method_layout.addWidget(self.app_password_radio)
        
        auth_layout.addRow("Auth Method:", auth_method_layout)
        
        # Help text
        help_text = (
            "Note: For WordPress REST API, you typically need to use an Application Password.\n"
            "You can create one in your WordPress admin under Users → Profile → Application Passwords."
        )
        help_label = QLabel(help_text)
        help_label.setWordWrap(True)
        auth_layout.addRow("", help_label)
        
        auth_group.setLayout(auth_layout)
        
        # Checkboxes for content types
        content_group = QGroupBox("Content to Push")
        checkbox_layout = QHBoxLayout()
        
        self.posts_check = QCheckBox("posts")
        self.pages_check = QCheckBox("pages")
        
        checkbox_layout.addWidget(self.posts_check)
        checkbox_layout.addWidget(self.pages_check)
        content_group.setLayout(checkbox_layout)
        
        # Site info
        info_layout = QVBoxLayout()
        self.site_label = QLabel(f"Site URL: {SITE_URL}")
        self.output_label = QLabel(f"Content directory: {OUTPUT_DIR}")
        info_layout.addWidget(self.site_label)
        info_layout.addWidget(self.output_label)
        
        # Push button
        self.push_button = QPushButton("Push to WordPress")
        
        # Text area for output
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        
        # Add all components to main layout
        main_layout.addLayout(info_layout)
        main_layout.addWidget(auth_group)
        main_layout.addWidget(content_group)
        main_layout.addWidget(self.push_button)
        main_layout.addWidget(self.text_area)
    
    def on_push_clicked(self):
        # Validate credentials
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            self.text_area.append("Error: WordPress username and password are required.")
            return
            
        # Get authentication method
        auth_method = "application" if self.app_password_radio.isChecked() else "basic"
            
        selected = []
        if self.posts_check.isChecked():
            selected.append("posts")
        if self.pages_check.isChecked():
            selected.append("pages")
            
        if not selected:
            self.text_area.append("Error: No content type selected.")
            return
            
        # Push content to WordPress
        self.text_area.append(f"Pushing: {', '.join(selected)} to {SITE_URL}")
        
        for content_type in selected:
            try:
                self.text_area.append(f"Processing {content_type}...")
                count, folder = self.pusher.push_items(content_type, username, password, auth_method)
                self.text_area.append(f"Successfully pushed {count} {content_type} from {folder}")
            except Exception as e:
                self.text_area.append(f"Error pushing {content_type}: {str(e)}")
                
                # Show more helpful error message for authentication issues
                if "401" in str(e):
                    QMessageBox.warning(
                        self,
                        "Authentication Error",
                        "WordPress authentication failed. Please make sure you're using an Application Password " 
                        "generated from your WordPress profile, not your regular login password."
                    )
                
        self.text_area.append("Push operation completed.")
