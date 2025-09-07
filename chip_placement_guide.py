#!/usr/bin/env python3
"""
Chip Placement Guide Widget for PyK150
Provides visual guidance for placing PIC chips on the K150 programmer socket
"""

import tkinter as tk
from tkinter import ttk
import math
import subprocess
import json
import threading

class ChipPlacementGuide:
    def __init__(self, parent, backend_path=None, selected_backend="picpro"):
        self.parent = parent
        self.current_chip = None
        self.backend_path = backend_path
        self.selected_backend = selected_backend
        self.chip_pin_info = {}  # Cache for pin information
        self.setup_gui()
        
    def setup_gui(self):
        # Main frame for the chip placement guide
        self.frame = ttk.LabelFrame(self.parent, text="Chip Placement Guide", padding=10)
        
        # Canvas for drawing the socket and chip
        self.canvas = tk.Canvas(self.frame, width=300, height=450, bg='#2c2c2c')
        self.canvas.pack(pady=5)
        
        # Info label
        self.info_label = ttk.Label(self.frame, text="Select a chip to see placement guide", 
                                   font=('Arial', 9), foreground='blue')
        self.info_label.pack(pady=5)
        
        # Pin info label
        self.pin_info_label = ttk.Label(self.frame, text="", 
                                       font=('Arial', 9, 'bold'), foreground='#FF6600', wraplength=280)
        self.pin_info_label.pack(pady=2)
        
        # Draw the default socket
        self.draw_socket()
        
    def draw_socket(self):
        """Draw the K150 programmer socket"""
        self.canvas.delete("all")
        
        # Socket outline (ZIF socket representation)
        socket_x = 50
        socket_y = 50
        socket_width = 200
        socket_height = 300
        
        # Main socket body
        self.canvas.create_rectangle(socket_x, socket_y, socket_x + socket_width, socket_y + socket_height,
                                   fill='#404040', outline='#606060', width=2)
        
        # Socket lever
        lever_x = socket_x + socket_width + 5
        lever_y = socket_y + 20
        self.canvas.create_rectangle(lever_x, lever_y, lever_x + 15, lever_y + 60,
                                   fill='#808080', outline='#a0a0a0', width=1)
        
        # Socket label
        self.canvas.create_text(socket_x + socket_width//2, socket_y - 20, 
                              text="K150 ZIF Socket", fill='white', font=('Arial', 10, 'bold'))
        
        # Pin 1 indicator
        self.canvas.create_oval(socket_x + 10, socket_y + 10, socket_x + 20, socket_y + 20,
                              fill='red', outline='darkred', width=1)
        self.canvas.create_text(socket_x + 30, socket_y + 15, text="Pin 1", fill='red', font=('Arial', 8))
        
        # Socket pins representation
        for i in range(20):  # 40-pin socket, 20 pins each side
            # Left side pins
            pin_y = socket_y + 30 + (i * 12)
            self.canvas.create_rectangle(socket_x - 5, pin_y, socket_x + 5, pin_y + 8,
                                       fill='#c0c0c0', outline='#808080')
            
            # Right side pins
            self.canvas.create_rectangle(socket_x + socket_width - 5, pin_y, 
                                       socket_x + socket_width + 5, pin_y + 8,
                                       fill='#c0c0c0', outline='#808080')
        
    def update_chip_guide(self, chip_type):
        """Update the guide for a specific chip type"""
        self.current_chip = chip_type
        self.draw_socket()
        
        if not chip_type:
            self.info_label.config(text="Select a chip to see placement guide")
            return
            
        # Get chip info
        chip_info = self.get_chip_info(chip_type)
        
        if chip_info:
            self.draw_chip(chip_info)
            # Determine ZIF socket based on pin count
            pins = chip_info.get('pins', 0)
            if pins >= 40:
                zif_pin = "ZIF Pin 1"
            else:
                zif_pin = "ZIF Pin 2"
            self.info_label.config(text=f"Place {chip_type} with Pin 1 at {zif_pin} position")
        else:
            self.info_label.config(text=f"Chip guide for {chip_type} not available")
    
    def get_chip_info_from_backend(self, chip_type):
        """Get chip information from backend (picpro/picp)"""
        if chip_type in self.chip_pin_info:
            return self.chip_pin_info[chip_type]
            
        def fetch_info():
            try:
                backend_exe = self.backend_path if self.backend_path else self.selected_backend
                cmd = [backend_exe, "chipinfo", chip_type]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    try:
                        # Try to parse JSON response
                        info = json.loads(result.stdout)
                        self.chip_pin_info[chip_type] = info
                        return info
                    except json.JSONDecodeError:
                        # Fallback to text parsing
                        return self.parse_text_chipinfo(result.stdout, chip_type)
                else:
                    return None
            except Exception as e:
                print(f"Error getting chip info: {e}")
                return None
        
        # Run in background thread
        thread = threading.Thread(target=fetch_info)
        thread.daemon = True
        thread.start()
        
        # Return cached info or fallback
        return self.get_chip_info_fallback(chip_type)
    
    def parse_text_chipinfo(self, text, chip_type):
        """Parse text-based chip info from backend"""
        lines = text.split('\n')
        info = {'pins': 0, 'package': 'Unknown', 'pin_functions': {}}
        
        for line in lines:
            line = line.strip()
            if 'pins' in line.lower() or 'pin count' in line.lower():
                # Try to extract pin count
                import re
                match = re.search(r'(\d+)\s*pins?', line, re.IGNORECASE)
                if match:
                    info['pins'] = int(match.group(1))
            elif 'package' in line.lower():
                # Try to extract package type
                if 'dip' in line.lower():
                    info['package'] = 'DIP'
                elif 'soic' in line.lower():
                    info['package'] = 'SOIC'
                elif 'qfn' in line.lower():
                    info['package'] = 'QFN'
        
        # If no pin count found, use fallback
        if info['pins'] == 0:
            fallback = self.get_chip_info_fallback(chip_type)
            if fallback:
                info.update(fallback)
        
        return info
    
    def get_chip_info_fallback(self, chip_type):
        """Fallback chip package information"""
        # Common PIC chip packages
        chip_packages = {
            # 8-pin chips
            '12F675': {'pins': 8, 'package': 'DIP-8'},
            '12F683': {'pins': 8, 'package': 'DIP-8'},
            '12F1840': {'pins': 8, 'package': 'DIP-8'},
            
            # 14-pin chips  
            '16F84A': {'pins': 14, 'package': 'DIP-14'},
            '16F628A': {'pins': 14, 'package': 'DIP-14'},
            '16F648A': {'pins': 14, 'package': 'DIP-14'},
            
            # 18-pin chips
            '16F84': {'pins': 18, 'package': 'DIP-18'},
            '16F628': {'pins': 18, 'package': 'DIP-18'},
            '16F1827': {'pins': 18, 'package': 'DIP-18'},
            '16F1847': {'pins': 18, 'package': 'DIP-18'},
            
            # 20-pin chips
            '16F690': {'pins': 20, 'package': 'DIP-20'},
            '16F88': {'pins': 20, 'package': 'DIP-20'},
            
            # 40-pin chips
            '16F887': {'pins': 40, 'package': 'DIP-40'},
            
            # 28-pin chips
            '16F876A': {'pins': 28, 'package': 'DIP-28'},
            '16F877A': {'pins': 28, 'package': 'DIP-28'},
            
            # 40-pin chips
            '18F2550': {'pins': 40, 'package': 'DIP-40'},
            '18F4550': {'pins': 40, 'package': 'DIP-40'},
            '18F25K50': {'pins': 40, 'package': 'DIP-40'},
            '18F45K50': {'pins': 40, 'package': 'DIP-40'},
            '18F2580': {'pins': 40, 'package': 'DIP-40'},
            '18F4580': {'pins': 40, 'package': 'DIP-40'},
        }
        
        return chip_packages.get(chip_type)
    
    def get_chip_info(self, chip_type):
        """Get chip package information (main function)"""
        # Try to get info from backend first
        backend_info = self.get_chip_info_from_backend(chip_type)
        if backend_info:
            return backend_info
        
        # Fallback to static info
        return self.get_chip_info_fallback(chip_type)
    
    def draw_chip(self, chip_info):
        """Draw the chip on the socket"""
        pins = chip_info['pins']
        package = chip_info['package']
        
        # Calculate chip dimensions based on pin count
        if pins <= 8:
            chip_width = 60
            chip_height = 80
            pins_per_side = pins // 2
        elif pins <= 14:
            chip_width = 60
            chip_height = 100
            pins_per_side = pins // 2
        elif pins <= 20:
            chip_width = 60
            chip_height = 140
            pins_per_side = pins // 2
        elif pins <= 28:
            chip_width = 60
            chip_height = 180
            pins_per_side = pins // 2
        else:  # 40-pin
            chip_width = 60
            chip_height = 260
            pins_per_side = pins // 2
        
        # Center the chip in the socket
        socket_x = 50
        socket_y = 50
        socket_width = 200
        
        chip_x = socket_x + (socket_width - chip_width) // 2
        chip_y = socket_y + 40
        
        # Draw chip body
        self.canvas.create_rectangle(chip_x, chip_y, chip_x + chip_width, chip_y + chip_height,
                                   fill='#1a1a1a', outline='#ffffff', width=2)
        
        # Draw chip notch (Pin 1 indicator)
        notch_size = 8
        self.canvas.create_arc(chip_x + chip_width//2 - notch_size, chip_y - notch_size//2,
                             chip_x + chip_width//2 + notch_size, chip_y + notch_size//2,
                             start=0, extent=180, fill='#1a1a1a', outline='white', width=2)
        
        # Draw pins
        pin_spacing = chip_height / (pins_per_side + 1)
        
        for i in range(pins_per_side):
            # Left side pins (1-9)
            pin_y = chip_y + pin_spacing * (i + 1) - 3
            self.canvas.create_rectangle(chip_x - 8, pin_y, chip_x, pin_y + 6,
                                       fill='#c0c0c0', outline='#808080')
            
            # Pin numbers (left side) - Normal chip standard: 1-9
            pin_num = i + 1  # Start from pin 1
            self.canvas.create_text(chip_x - 15, pin_y + 3, text=str(pin_num), 
                                  fill='yellow', font=('Arial', 7))
            
            # Right side pins (10-18)
            self.canvas.create_rectangle(chip_x + chip_width, pin_y, chip_x + chip_width + 8, pin_y + 6,
                                       fill='#c0c0c0', outline='#808080')
            
            # Pin numbers (right side) - Normal chip standard: 10-18 (bottom to top)
            pin_num = pins - i  # Start from pin 18 (bottom) and go up
            self.canvas.create_text(chip_x + chip_width + 15, pin_y + 3, text=str(pin_num), 
                                  fill='yellow', font=('Arial', 7))
        
        # Chip label
        self.canvas.create_text(chip_x + chip_width//2, chip_y + chip_height//2,
                              text=self.current_chip, fill='white', font=('Arial', 8, 'bold'))
        
        # Package info
        self.canvas.create_text(chip_x + chip_width//2, chip_y + chip_height + 15,
                              text=package, fill='cyan', font=('Arial', 8))
        
        # Pin 1 highlight (first pin on left side)
        self.canvas.create_oval(chip_x - 12, chip_y + pin_spacing - 6, 
                              chip_x - 4, chip_y + pin_spacing + 2,
                              fill='red', outline='darkred', width=2)
        # Add "Pin 1" label next to the highlight
        self.canvas.create_text(chip_x - 20, chip_y + pin_spacing - 2, text="Pin 1", 
                              fill='red', font=('Arial', 8, 'bold'))
        # Add ZIF pin indicator based on pin count
        if pins >= 40:
            zif_pin_text = "ZIF Pin 1"
        else:
            zif_pin_text = "ZIF Pin 2"
        self.canvas.create_text(chip_x - 15, chip_y + pin_spacing + 10, text=zif_pin_text, 
                              fill='cyan', font=('Arial', 7))
        
        # Show pin information if available
        if 'pin_functions' in chip_info and chip_info['pin_functions']:
            pin_info_text = "Pin functions: "
            for pin, func in list(chip_info['pin_functions'].items())[:3]:  # Show first 3 pins
                pin_info_text += f"Pin{pin}:{func} "
            self.pin_info_label.config(text=pin_info_text)
        else:
            # Show common pin functions for known chips
            pin_info = self.get_common_pin_functions(self.current_chip)
            if pin_info:
                self.pin_info_label.config(text=pin_info)
            else:
                self.pin_info_label.config(text="")
        
        # Placement instructions
        if pins >= 40:
            zif_pin_instruction = "3. Chip Pin 1 goes to ZIF Pin 1"
        else:
            zif_pin_instruction = "3. Chip Pin 1 goes to ZIF Pin 2"
        
        instructions = [
            "1. Open ZIF socket lever",
            "2. Insert chip with notch at top", 
            zif_pin_instruction,
            "4. Close lever to secure chip"
        ]
        
        for i, instruction in enumerate(instructions):
            self.canvas.create_text(150, 400 + i * 15, text=instruction, 
                                  fill='#00FF00', font=('Arial', 9, 'bold'))

    def get_common_pin_functions(self, chip_type):
        """Get common pin functions for known chips"""
        common_pins = {
            '16F84': "Pin1:VDD | Pin2:RA5 | Pin3:RA4 | Pin4:MCLR | Pin5:VSS | Pin6:RB0 | Pin7:RB1 | Pin8:RB2 | Pin9:RB3 | Pin10:RB4 | Pin11:RB5 | Pin12:RB6 | Pin13:RB7 | Pin14:OSC1 | Pin15:OSC2 | Pin16:VDD | Pin17:RA0 | Pin18:RA1",
            '16F84A': "Pin1:VDD | Pin2:RA5 | Pin3:RA4 | Pin4:MCLR | Pin5:VSS | Pin6:RB0 | Pin7:RB1 | Pin8:RB2 | Pin9:RB3 | Pin10:RB4 | Pin11:RB5 | Pin12:RB6 | Pin13:RB7 | Pin14:OSC1 | Pin15:OSC2 | Pin16:VDD | Pin17:RA0 | Pin18:RA1",
            '12F675': "Pin1:VDD | Pin2:GP5 | Pin3:GP4 | Pin4:MCLR | Pin5:GP3 | Pin6:GP2 | Pin7:GP1 | Pin8:VSS",
            '16F628A': "Pin1:VDD | Pin2:RA5 | Pin3:RA4 | Pin4:MCLR | Pin5:VSS | Pin6:RB0 | Pin7:RB1 | Pin8:RB2 | Pin9:RB3 | Pin10:RB4 | Pin11:RB5 | Pin12:RB6 | Pin13:RB7 | Pin14:OSC1 | Pin15:OSC2 | Pin16:VDD | Pin17:RA0 | Pin18:RA1",
            '16F887': "Pin1:MCLR | Pin2:RA0 | Pin3:RA1 | Pin4:RA2 | Pin5:RA3 | Pin6:RA4 | Pin7:RA5 | Pin8:RE0 | Pin9:RE1 | Pin10:RE2 | Pin11:VDD | Pin12:VSS | Pin13:RA7 | Pin14:RA6 | Pin15:RC0 | Pin16:RC1 | Pin17:RC2 | Pin18:RC3 | Pin19:RD0 | Pin20:RD1 | Pin21:RD2 | Pin22:RD3 | Pin23:RC4 | Pin24:RC5 | Pin25:RC6 | Pin26:RC7 | Pin27:RD4 | Pin28:RD5 | Pin29:RD6 | Pin30:RD7 | Pin31:VSS | Pin32:VDD | Pin33:RB0 | Pin34:RB1 | Pin35:RB2 | Pin36:RB3 | Pin37:RB4 | Pin38:RB5 | Pin39:RB6 | Pin40:RB7",
            '18F2550': "Pin1:VDD | Pin2:RA0 | Pin3:RA1 | Pin4:RA2 | Pin5:RA3 | Pin6:RA4 | Pin7:RA5 | Pin8:VSS | Pin9:RB0 | Pin10:RB1 | Pin11:RB2 | Pin12:RB3 | Pin13:RB4 | Pin14:RB5 | Pin15:RB6 | Pin16:RB7 | Pin17:RC0 | Pin18:RC1 | Pin19:RC2 | Pin20:RC3 | Pin21:RC4 | Pin22:RC5 | Pin23:RC6 | Pin24:RC7 | Pin25:VDD | Pin26:OSC1 | Pin27:OSC2 | Pin28:MCLR | Pin29:VSS | Pin30:RD0 | Pin31:RD1 | Pin32:RD2 | Pin33:RD3 | Pin34:RD4 | Pin35:RD5 | Pin36:RD6 | Pin37:RD7 | Pin38:VDD | Pin39:RE0 | Pin40:RE1"
        }
        
        return common_pins.get(chip_type, "")
    
    def update_backend(self, backend_path, selected_backend):
        """Update backend information"""
        self.backend_path = backend_path
        self.selected_backend = selected_backend
        # Clear cache when backend changes
        self.chip_pin_info.clear()
    
    def get_frame(self):
        """Return the main frame widget"""
        return self.frame

# Test the widget
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Chip Placement Guide Test")
    root.geometry("400x600")
    root.configure(bg='#f0f0f0')
    
    guide = ChipPlacementGuide(root)
    guide.get_frame().pack(fill='both', expand=True, padx=10, pady=10)
    
    # Test with different chips
    def test_chip(chip_type):
        guide.update_chip_guide(chip_type)
    
    # Test buttons
    button_frame = ttk.Frame(root)
    button_frame.pack(pady=10)
    
    ttk.Button(button_frame, text="16F84A", command=lambda: test_chip("16F84A")).pack(side='left', padx=5)
    ttk.Button(button_frame, text="18F2550", command=lambda: test_chip("18F2550")).pack(side='left', padx=5)
    ttk.Button(button_frame, text="12F675", command=lambda: test_chip("12F675")).pack(side='left', padx=5)
    ttk.Button(button_frame, text="Clear", command=lambda: test_chip(None)).pack(side='left', padx=5)
    
    root.mainloop()
