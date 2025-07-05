import json
from pathlib import Path

class ConfigManager:
    def __init__(self):
        self.config_path = Path(__file__).resolve().parent.parent.parent / "config.json"

    def get_config(self):
        """Load configuration from JSON file."""
        if not self.config_path.exists():
            return {}
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_config(self, config_data):
        """Save configuration to JSON file."""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2)
