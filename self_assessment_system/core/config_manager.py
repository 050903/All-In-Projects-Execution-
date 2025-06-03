import json
import os
from typing import Any, Optional

class ConfigManager:
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = {}
        self.load_config()
    
    def load_config(self) -> None:
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            else:
                self._create_default_config()
        except Exception as e:
            print(f"Error loading config: {e}")
            self._create_default_config()
    
    def get(self, key: str, default: Any = None) -> Any:
        try:
            parts = key.split('.')
            value = self.config
            for part in parts:
                value = value[part]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> None:
        parts = key.split('.')
        config = self.config
        for part in parts[:-1]:
            config = config.setdefault(part, {})
        config[parts[-1]] = value
        self.save_config()
    
    def save_config(self) -> None:
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def _create_default_config(self) -> None:
        self.config = {
            "logging": {
                "level": "INFO",
                "file": "app.log"
            },
            "backup": {
                "enabled": True,
                "interval": 24,
                "max_backups": 5
            }
        }
        self.save_config()