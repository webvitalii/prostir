from .wp_content_pusher import WPContentPusher
from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QCheckBox, 
                              QPushButton, QTextEdit, QLabel, QMessageBox, QGroupBox)
from config import SITE_URL, OUTPUT_DIR
from ..config.config_manager import ConfigManager

class PushScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.pusher = WPContentPusher()
        self.config_manager = ConfigManager()

        # Create UI components
        self.setup_ui()
        
        # Connect signals
        self.push_button.clicked.connect(self.on_push_clicked)
        
    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Checkboxes for content types
        content_group = QGroupBox("Content to Push")
        checkbox_layout = QHBoxLayout()
        
        self.posts_check = QCheckBox("posts")
        self.pages_check = QCheckBox("pages")
        
        checkbox_layout.addWidget(self.posts_check)
        checkbox_layout.addWidget(self.pages_check)
        content_group.setLayout(checkbox_layout)
        
        # Output directory info
        info_layout = QVBoxLayout()
        self.output_label = QLabel(f"Content directory: {OUTPUT_DIR}")
        info_layout.addWidget(self.output_label)
        
        # Push button
        self.push_button = QPushButton("Push to WordPress")
        
        # Text area for output
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        
        # Add all components to main layout
        main_layout.addLayout(info_layout)
        main_layout.addWidget(content_group)
        main_layout.addWidget(self.push_button)
        main_layout.addWidget(self.text_area)


    def on_push_clicked(self):
        # Load auth data from config file
        config_data = self.config_manager.get_config()
        if not config_data:
            return
            
        username = config_data.get('username', '')
        password = config_data.get('password', '')
        auth_method = config_data.get('auth_method', 'application')
        
        if not username or not password:
            self.text_area.append("Error: WordPress username and password are required.")
            QMessageBox.warning(
                self,
                "Authentication Missing",
                "Please configure your WordPress authentication credentials in the Config screen."
            )
            return
            
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
