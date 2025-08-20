#!/usr/bin/env python3
"""
Configuration management for PyK150
"""

import json
import os
import subprocess
from pathlib import Path

class Config:
    def __init__(self):
        self.config_dir = Path.home() / ".pyk150"
        self.config_file = self.config_dir / "config.json"
        self.config_dir.mkdir(exist_ok=True)
        
        # Default configuration
        self.defaults = {
            "last_port": "",
            "last_pic_type": "12F675",
            "last_hex_file": "",
            "last_output_dir": str(Path.home()),
            "icsp_enabled": False,
            "window_geometry": "800x600",
            "language": "en",
            "theme": "default",
            "auto_detect_programmer": True,
            "programmer_timeout": 5,
            "recent_files": [],
            "max_recent_files": 10,
            "picpro_path": "",
            "auto_find_picpro": True,
            "picpro_search_paths": [
                "/usr/local/bin/picpro",
                "/usr/bin/picpro",
                "~/.local/bin/picpro",
                "picpro"
            ]
        }
        
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # Merge with defaults to ensure all keys exist
                merged_config = self.defaults.copy()
                merged_config.update(config)
                return merged_config
            except (json.JSONDecodeError, IOError):
                return self.defaults.copy()
        return self.defaults.copy()
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except IOError:
            pass  # Fail silently
    
    def save(self):
        """Alias for save_config() for backward compatibility"""
        self.save_config()
    
    def get(self, key, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Set configuration value"""
        self.config[key] = value
        self.save_config()
    
    def add_recent_file(self, filepath):
        """Add file to recent files list"""
        recent = self.config.get("recent_files", [])
        if filepath in recent:
            recent.remove(filepath)
        recent.insert(0, filepath)
        recent = recent[:self.config.get("max_recent_files", 10)]
        self.set("recent_files", recent)
    
    def get_recent_files(self):
        """Get list of recent files"""
        recent = self.config.get("recent_files", [])
        # Filter out files that no longer exist
        existing_files = [f for f in recent if os.path.exists(f)]
        if len(existing_files) != len(recent):
            self.set("recent_files", existing_files)
        return existing_files
    
    def find_picpro_executable(self):
        """Find picpro executable automatically"""
        import shutil
        import subprocess
        
        # First check if user has set a custom path
        custom_path = self.get("picpro_path")
        if custom_path and os.path.exists(custom_path):
            return custom_path
            
        # If auto-find is disabled, return empty
        if not self.get("auto_find_picpro", True):
            return ""
            
        # Try to find picpro using 'which' command
        try:
            result = subprocess.run(['which', 'picpro'], capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip():
                path = result.stdout.strip()
                if os.path.exists(path):
                    return path
        except:
            pass
            
        # Try using shutil.which
        try:
            path = shutil.which('picpro')
            if path and os.path.exists(path):
                return path
        except:
            pass
            
        # Try predefined search paths
        search_paths = self.get("picpro_search_paths", [])
        for path in search_paths:
            expanded_path = os.path.expanduser(path)
            if os.path.exists(expanded_path):
                return expanded_path
                
        # Try Python module path
        try:
            import picpro
            module_path = os.path.dirname(picpro.__file__)
            potential_paths = [
                os.path.join(module_path, 'picpro'),
                os.path.join(module_path, '..', 'bin', 'picpro'),
                os.path.join(module_path, '..', 'Scripts', 'picpro.exe'),  # Windows
            ]
            for path in potential_paths:
                if os.path.exists(path):
                    return path
        except ImportError:
            pass
            
        return ""
    
    def validate_picpro_path(self, path):
        """Validate picpro executable path and version"""
        if not path or not os.path.exists(path):
            return False, "Path does not exist"
            
        if not os.access(path, os.X_OK):
            return False, "File is not executable"
            
        try:
            # Test if it's actually picpro by running --help
            result = subprocess.run([path, "--help"], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=10)
            
            if result.returncode == 0 and "picpro" in result.stdout.lower():
                # Check version
                version_valid, version_msg = self.check_picpro_version(path)
                if version_valid:
                    return True, "Valid picpro executable"
                else:
                    return False, f"Valid picpro but {version_msg}"
            else:
                return False, "Not a valid picpro executable"
                
        except subprocess.TimeoutExpired:
            return False, "Command timed out"
        except Exception as e:
            return False, f"Error testing executable: {str(e)}"
            
    def check_picpro_version(self, path):
        """Check picpro version and validate minimum requirement"""
        try:
            # Try to get version with --version flag
            result = subprocess.run([path, "--version"], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=10)
            
            if result.returncode == 0:
                version_text = result.stdout.strip()
                version = self.parse_version(version_text)
                
                if version:
                    min_version = (0, 3, 0)  # Minimum required version 0.3.0
                    if version >= min_version:
                        return True, f"Version {'.'.join(map(str, version))} (OK)"
                    else:
                        return False, f"version {'.'.join(map(str, version))} is too old (minimum: 0.3.0)"
                else:
                    return False, "could not parse version"
            else:
                # Try alternative method - check help output for version info
                help_result = subprocess.run([path, "--help"], 
                                           capture_output=True, 
                                           text=True, 
                                           timeout=10)
                
                if help_result.returncode == 0:
                    version = self.parse_version(help_result.stdout)
                    if version:
                        min_version = (0, 3, 0)
                        if version >= min_version:
                            return True, f"Version {'.'.join(map(str, version))} (OK)"
                        else:
                            return False, f"version {'.'.join(map(str, version))} is too old (minimum: 0.3.0)"
                
                # If no version found, assume it's compatible but warn
                return True, "version unknown (assuming compatible)"
                
        except subprocess.TimeoutExpired:
            return False, "version check timed out"
        except Exception as e:
            return False, f"error checking version: {str(e)}"
            
    def parse_version(self, text):
        """Parse version string from picpro output"""
        import re
        
        # Look for version patterns like "0.3.0", "v0.3.0", "version 0.3.0"
        patterns = [
            r'(?:version\s+)?v?(\d+)\.(\d+)\.(\d+)',
            r'picpro\s+v?(\d+)\.(\d+)\.(\d+)',
            r'v?(\d+)\.(\d+)\.(\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    return (int(match.group(1)), int(match.group(2)), int(match.group(3)))
                except ValueError:
                    continue
                    
        return None
