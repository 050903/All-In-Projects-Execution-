import os
import shutil
import json
import datetime
import zipfile
from typing import Optional, List

class BackupManager:
    def __init__(self, backup_dir: str = 'backups'):
        self.backup_dir = backup_dir
        self.ensure_backup_dir()
    
    def ensure_backup_dir(self) -> None:
        """Create backup directory if it doesn't exist"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    def create_backup(self, data: dict, name: str) -> str:
        """Create a backup with timestamp"""
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{name}_{timestamp}.zip"
        backup_path = os.path.join(self.backup_dir, filename)
        
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr('data.json', json.dumps(data, indent=2))
        
        return backup_path
    
    def restore_backup(self, backup_file: str) -> Optional[dict]:
        """Restore data from a backup file"""
        try:
            with zipfile.ZipFile(os.path.join(self.backup_dir, backup_file), 'r') as zf:
                with zf.open('data.json') as f:
                    return json.loads(f.read())
        except Exception as e:
            raise ValueError(f"Failed to restore backup: {str(e)}")
    
    def list_backups(self) -> List[str]:
        """List all available backups"""
        return [f for f in os.listdir(self.backup_dir) if f.endswith('.zip')]
    
    def delete_backup(self, backup_file: str) -> bool:
        """Delete a specific backup file"""
        try:
            os.remove(os.path.join(self.backup_dir, backup_file))
            return True
        except Exception:
            return False