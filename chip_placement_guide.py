#!/usr/bin/env python3
"""
Chip Placement Guide Widget for PyK150
Provides visual guidance for placing PIC chips on the K150 programmer socket
"""

import tkinter as tk
from tkinter import ttk
import math

class ChipPlacementGuide:
    def __init__(self, parent):
        self.parent = parent
        self.current_chip = None
        self.setup_gui()
        
    def setup_gui(self):
        # Main frame for the chip placement guide
        self.frame = ttk.LabelFrame(self.parent, text="Chip Placement Guide", padding=10)
        
        # Canvas for drawing the socket and chip
        self.canvas = tk.Canvas(self.frame, width=300, height=400, bg='#2c2c2c')
        self.canvas.pack(pady=5)
        
        # Info label
        self.info_label = ttk.Label(self.frame, text="Select a chip to see placement guide", 
                                   font=('Arial', 9), foreground='blue')
        self.info_label.pack(pady=5)
        
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
            self.info_label.config(text=f"Place {chip_type} with Pin 1 at top-left corner")
        else:
            self.info_label.config(text=f"Chip guide for {chip_type} not available")
    
    def get_chip_info(self, chip_type):
        """Get chip package information"""
        # Common PIC chip packages
        chip_packages = {
            # 8-pin chips
            '12F675': {'pins': 8, 'package': 'DIP-8'},
            '12F683': {'pins': 8, 'package': 'DIP-8'},
            
            # 14-pin chips  
            '16F84A': {'pins': 14, 'package': 'DIP-14'},
            '16F628A': {'pins': 14, 'package': 'DIP-14'},
            
            # 18-pin chips
            '16F84': {'pins': 18, 'package': 'DIP-18'},
            '16F628': {'pins': 18, 'package': 'DIP-18'},
            
            # 20-pin chips
            '16F690': {'pins': 20, 'package': 'DIP-20'},
            '16F88': {'pins': 20, 'package': 'DIP-20'},
            
            # 28-pin chips
            '16F876A': {'pins': 28, 'package': 'DIP-28'},
            '16F877A': {'pins': 28, 'package': 'DIP-28'},
            
            # 40-pin chips
            '18F2550': {'pins': 40, 'package': 'DIP-40'},
            '18F4550': {'pins': 40, 'package': 'DIP-40'},
        }
        
        return chip_packages.get(chip_type)
    
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
            # Left side pins
            pin_y = chip_y + pin_spacing * (i + 1) - 3
            self.canvas.create_rectangle(chip_x - 8, pin_y, chip_x, pin_y + 6,
                                       fill='#c0c0c0', outline='#808080')
            
            # Pin numbers (left side)
            pin_num = i + 1
            self.canvas.create_text(chip_x - 15, pin_y + 3, text=str(pin_num), 
                                  fill='yellow', font=('Arial', 7))
            
            # Right side pins
            self.canvas.create_rectangle(chip_x + chip_width, pin_y, chip_x + chip_width + 8, pin_y + 6,
                                       fill='#c0c0c0', outline='#808080')
            
            # Pin numbers (right side)
            pin_num = pins - i
            self.canvas.create_text(chip_x + chip_width + 15, pin_y + 3, text=str(pin_num), 
                                  fill='yellow', font=('Arial', 7))
        
        # Chip label
        self.canvas.create_text(chip_x + chip_width//2, chip_y + chip_height//2,
                              text=self.current_chip, fill='white', font=('Arial', 8, 'bold'))
        
        # Package info
        self.canvas.create_text(chip_x + chip_width//2, chip_y + chip_height + 15,
                              text=package, fill='cyan', font=('Arial', 8))
        
        # Pin 1 highlight
        self.canvas.create_oval(chip_x - 12, chip_y + pin_spacing - 6, 
                              chip_x - 4, chip_y + pin_spacing + 2,
                              fill='red', outline='darkred', width=2)
        
        # Placement instructions
        instructions = [
            "1. Open ZIF socket lever",
            "2. Insert chip with notch at top",
            "3. Pin 1 goes to top-left",
            "4. Close lever to secure chip"
        ]
        
        for i, instruction in enumerate(instructions):
            self.canvas.create_text(150, 370 + i * 15, text=instruction, 
                                  fill='lightgreen', font=('Arial', 8))

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
