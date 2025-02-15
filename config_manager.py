import json
import os
from pathlib import Path

class ConfigManager:
    def __init__(self):
        self.config_dir = Path.home() / '.config' / 'gh-repo-pruner'
        self.config_file = self.config_dir / 'config.json'
        self._ensure_config_exists()
        
    def _ensure_config_exists(self):
        """Ensure config directory and file exist"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        if not self.config_file.exists():
            self._save_config({'base_path': None})
    
    def _save_config(self, config_data):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(config_data, f, indent=2)
    
    def _load_config(self):
        """Load configuration from file"""
        with open(self.config_file, 'r') as f:
            return json.load(f)
    
    def get_base_path(self):
        """Get the configured base path"""
        config = self._load_config()
        return config.get('base_path')
    
    def set_base_path(self, path):
        """Set the base path"""
        if path and not os.path.isdir(path):
            raise ValueError("Path does not exist or is not a directory")
        config = self._load_config()
        config['base_path'] = path
        self._save_config(config)