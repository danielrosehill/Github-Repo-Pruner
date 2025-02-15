import os
import random
from pathlib import Path
import shutil

class RepoManager:
    def __init__(self, base_path=None):
        self.base_path = Path(base_path) if base_path else None
        self._repos_list = []
        self._current_index = 0
        self._random_mode = False
        
    def set_base_path(self, path):
        """Set the base path and refresh repository list"""
        self.base_path = Path(path)
        self.refresh_repos()
    
    def refresh_repos(self):
        """Refresh the list of repositories"""
        if not self.base_path or not self.base_path.exists():
            self._repos_list = []
            return
            
        self._repos_list = [
            d for d in self.base_path.iterdir()
            if d.is_dir() and (d / '.git').exists()
        ]
        
        if not self._random_mode:
            self._repos_list.sort()
        else:
            random.shuffle(self._repos_list)
            
        self._current_index = 0
    
    def set_random_mode(self, enabled):
        """Set random mode and refresh repository list"""
        self._random_mode = enabled
        self.refresh_repos()
    
    def get_total_count(self):
        """Get total number of repositories"""
        return len(self._repos_list)
    
    def get_current_repo(self):
        """Get current repository info"""
        if not self._repos_list or self._current_index >= len(self._repos_list):
            return None
            
        repo_path = self._repos_list[self._current_index]
        return {
            'name': self._prettify_name(repo_path.name),
            'path': str(repo_path.relative_to(self.base_path)),
            'full_path': str(repo_path)
        }
    
    def _prettify_name(self, name):
        """Convert repository folder name to pretty format"""
        # Replace hyphens and underscores with spaces
        name = name.replace('-', ' ').replace('_', ' ')
        # Capitalize words
        return ' '.join(word.capitalize() for word in name.split())
    
    def delete_current_repo(self):
        """Delete current repository and move to next"""
        if not self._repos_list or self._current_index >= len(self._repos_list):
            return False
            
        repo_path = self._repos_list[self._current_index]
        try:
            shutil.rmtree(repo_path)
            self._repos_list.pop(self._current_index)
            # Don't increment index as the next repo slides into current position
            return True
        except Exception as e:
            print(f"Error deleting repository: {e}")
            return False
    
    def next_repo(self):
        """Move to next repository"""
        if self._random_mode and self._repos_list:
            # In random mode, shuffle remaining repos when reaching the end
            if self._current_index >= len(self._repos_list) - 1:
                random.shuffle(self._repos_list)
                self._current_index = 0
            else:
                self._current_index += 1
        else:
            self._current_index += 1
        
        return self.get_current_repo()
    
    def has_next(self):
        """Check if there are more repositories"""
        if self._random_mode:
            return bool(self._repos_list)
        return self._current_index < len(self._repos_list) - 1