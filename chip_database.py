#!/usr/bin/env python3
"""
Chip database parser and manager for PyK150
"""

import re
import requests
import os
from pathlib import Path

class ChipDatabase:
    def __init__(self):
        self.chips = []
        self.chip_families = {}
        self.chipdata_url = "https://raw.githubusercontent.com/Salamek/picpro/master/usr/share/picpro/chipdata.cid"
        self.cache_file = Path.home() / ".pyk150" / "chipdata.cache"
        
    def download_chipdata(self):
        """Download chipdata.cid file"""
        try:
            response = requests.get(self.chipdata_url, timeout=30)
            response.raise_for_status()
            
            # Ensure cache directory exists
            self.cache_file.parent.mkdir(exist_ok=True)
            
            # Save to cache
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
                
            return response.text
        except Exception as e:
            print(f"Error downloading chipdata: {e}")
            return None
            
    def load_chipdata(self):
        """Load chipdata from cache or download"""
        # Try to load from cache first
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return f.read()
            except:
                pass
                
        # Download if cache doesn't exist or failed to load
        return self.download_chipdata()
        
    def parse_chipdata(self, data):
        """Parse chipdata.cid content"""
        if not data:
            return
            
        self.chips = []
        self.chip_families = {}
        
        # Split by chip entries
        chip_blocks = data.split('\n\nCHIPname=')
        
        for i, block in enumerate(chip_blocks):
            if i == 0:
                # First block starts with CHIPname= already
                if block.startswith('CHIPname='):
                    block = block[9:]  # Remove 'CHIPname='
                else:
                    continue
            
            lines = block.strip().split('\n')
            if not lines:
                continue
                
            chip_name = lines[0].split('\r')[0].strip()
            if not chip_name:
                continue
                
            chip_info = {'name': chip_name}
            
            # Parse chip properties
            for line in lines[1:]:
                line = line.strip()
                if '=' in line and not line.startswith('LIST'):
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().rstrip('\r')
                    chip_info[key] = value
                    
            # Only include chips that are marked for inclusion
            if chip_info.get('INCLUDE', 'N') == 'Y':
                self.chips.append(chip_info)
                
                # Categorize by family
                family = self.get_chip_family(chip_name)
                if family not in self.chip_families:
                    self.chip_families[family] = []
                self.chip_families[family].append(chip_name)
                
        # Add PIC16F887 manually if not found in database
        if not any(chip['name'].upper() == '16F887' for chip in self.chips):
            pic16f887_info = {
                'name': '16F887',
                'INCLUDE': 'Y',
                'ROMSIZE': '001C00',  # 7168 words in hex
                'FAMILY': 'PIC16F'
            }
            self.chips.append(pic16f887_info)
            
            # Add to family
            family = self.get_chip_family('16F887')
            if family not in self.chip_families:
                self.chip_families[family] = []
            self.chip_families[family].append('16F887')
        
        # Sort chips and families
        self.chips.sort(key=lambda x: x['name'])
        for family in self.chip_families:
            self.chip_families[family].sort()
            
    def get_chip_family(self, chip_name):
        """Determine chip family from name"""
        chip_name = chip_name.upper()
        
        # PIC10F series
        if chip_name.startswith('10F'):
            return 'PIC10F'
        # PIC12 series
        elif chip_name.startswith('12'):
            if 'C' in chip_name:
                return 'PIC12C'
            elif 'F' in chip_name:
                return 'PIC12F'
            else:
                return 'PIC12'
        # PIC16 series
        elif chip_name.startswith('16'):
            if 'C' in chip_name:
                return 'PIC16C'
            elif 'F' in chip_name:
                return 'PIC16F'
            else:
                return 'PIC16'
        # PIC18 series
        elif chip_name.startswith('18'):
            return 'PIC18F'
        # dsPIC series
        elif chip_name.startswith('30F') or chip_name.startswith('33F'):
            return 'dsPIC'
        # PIC24 series
        elif chip_name.startswith('24'):
            return 'PIC24'
        else:
            return 'Other'
            
    def get_all_chips(self):
        """Get list of all chip names"""
        return [chip['name'] for chip in self.chips]
        
    def get_chips_by_family(self, family=None):
        """Get chips by family"""
        if family:
            return self.chip_families.get(family, [])
        else:
            return dict(self.chip_families)
            
    def search_chips(self, query):
        """Search chips by name"""
        query = query.upper()
        results = []
        
        for chip in self.chips:
            if query in chip['name'].upper():
                results.append(chip['name'])
                
        return sorted(results)
        
    def get_chip_info(self, chip_name):
        """Get detailed info for a specific chip"""
        for chip in self.chips:
            if chip['name'].upper() == chip_name.upper():
                return chip
        return None
    
    def get_chip_rom_size(self, chip_name):
        """Get ROM size in words for a specific chip"""
        chip_info = self.get_chip_info(chip_name)
        if chip_info:
            # Try different possible ROM size field names
            for field in ['ROMSIZE', 'ROMsize', 'romsize']:
                if field in chip_info:
                    try:
                        rom_size_str = chip_info[field]
                        # Handle hexadecimal format (like '001000')
                        if rom_size_str.isdigit():
                            return int(rom_size_str, 16)  # Parse as hex
                        else:
                            return int(rom_size_str)
                    except ValueError:
                        continue
        
        # Fallback: hardcoded ROM sizes for common chips
        rom_sizes = {
            '16F690': 4096,
            '16F84A': 1024,
            '16F84': 1024,  # Add PIC16F84
            '16F628A': 2048,
            '16F877A': 8192,
            '16F887': 7168,  # Add PIC16F887 (14KB = 7168 words)
            '12F675': 1024,
            '12F683': 2048,
            '18F2550': 16384,
            '18F4550': 16384,
            '10F200': 256,
            '10F202': 512,
        }
        
        chip_upper = chip_name.upper()
        if chip_upper in rom_sizes:
            return rom_sizes[chip_upper]
            
        return None
    
    def validate_hex_file_size(self, hex_file_path, chip_name):
        """Validate if HEX file fits in chip ROM"""
        try:
            rom_size = self.get_chip_rom_size(chip_name)
            if rom_size is None:
                return True, f"Unknown ROM size for {chip_name}"
            
            # Parse HEX file to count program words
            hex_data_size = self._parse_hex_file_size(hex_file_path)
            if hex_data_size is None:
                return True, "Could not parse HEX file"
            
            if hex_data_size > rom_size:
                return False, f"HEX file too large: {hex_data_size} words > {rom_size} words ROM capacity"
            else:
                return True, f"HEX file size OK: {hex_data_size} words <= {rom_size} words ROM capacity"
                
        except Exception as e:
            return True, f"Error validating HEX file: {str(e)}"
    
    def _parse_hex_file_size(self, hex_file_path):
        """Parse Intel HEX file to determine program size in words"""
        try:
            max_address = 0
            with open(hex_file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line.startswith(':'):
                        continue
                    
                    # Parse Intel HEX record
                    byte_count = int(line[1:3], 16)
                    address = int(line[3:7], 16)
                    record_type = int(line[7:9], 16)
                    
                    # Only count data records (type 00) in program memory area
                    if record_type == 0 and byte_count > 0:
                        # For PIC, program memory typically starts at 0x0000
                        # Configuration memory is usually at 0x2000+ or 0x4000+
                        # Only count program memory (typically 0x0000-0x1FFF for 16F84)
                        if address < 0x2000:  # Program memory area
                            # For PIC, each instruction is 14-bit stored in 2 bytes
                            # Address is in bytes, convert to words
                            word_address = address // 2
                            word_count = byte_count // 2
                            max_address = max(max_address, word_address + word_count)
            
            return max_address
            
        except Exception:
            return None
        
    def get_popular_chips(self):
        """Get list of commonly used chips"""
        popular = [
            # PIC10F series
            '10F200', '10F202', '10F204', '10F206', '10F220', '10F222',
            
            # PIC12F series  
            '12F508', '12F509', '12F629', '12F635', '12F675', '12F683', 
            '12F1501', '12F1822', '12F1840',
            
            # PIC16F series
            '16F84A', '16F88', '16F628A', '16F648A', '16F877A', '16F887', 
            '16F1827', '16F1847', '16F1936', '16F1937',
            
            # PIC18F series
            '18F2550', '18F4550', '18F25K50', '18F45K50', '18F2580', 
            '18F4580', '18F26K80', '18F46K80'
        ]
        
        # Filter to only include chips that exist in our database
        available_chips = self.get_all_chips()
        return [chip for chip in popular if chip in available_chips]
        
    def initialize(self):
        """Initialize the chip database"""
        print("Loading chip database...")
        data = self.load_chipdata()
        if data:
            self.parse_chipdata(data)
            print(f"Loaded {len(self.chips)} PIC chips")
            return True
        else:
            print("Failed to load chip database")
            return False
            
    def get_chip_count_by_family(self):
        """Get chip count statistics by family"""
        stats = {}
        for family, chips in self.chip_families.items():
            stats[family] = len(chips)
        return stats
