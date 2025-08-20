#!/usr/bin/env python3
"""
Help system for PyK150
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import webbrowser

class HelpSystem:
    def __init__(self, parent, translations):
        self.parent = parent
        self.tr = translations
        
    def show_about_dialog(self):
        """Show about dialog"""
        about_window = tk.Toplevel(self.parent)
        about_window.title(self.tr("about"))
        about_window.geometry("400x300")
        about_window.resizable(False, False)
        about_window.transient(self.parent)
        about_window.grab_set()
        
        # Center the window
        about_window.geometry("+%d+%d" % (
            self.parent.winfo_rootx() + 50,
            self.parent.winfo_rooty() + 50
        ))
        
        # Content frame
        content_frame = ttk.Frame(about_window, padding=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(content_frame, text="PyK150", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Version
        version_label = ttk.Label(content_frame, text="Version 1.0.0")
        version_label.pack()
        
        # Description
        desc_text = """PIC Microcontroller Programmer GUI

A modern graphical interface for programming PIC microcontrollers using K150/K128/K149/K182 programmers.

Features:
• Multi-language support (English/Turkish)
• Auto device detection
• Progress tracking
• Configuration management
• Comprehensive error handling"""
        
        desc_label = ttk.Label(content_frame, text=desc_text, justify=tk.LEFT)
        desc_label.pack(pady=10)
        
        # Credits
        credits_label = ttk.Label(content_frame, text="Based on picpro by Salamek\nGUI developed for enhanced usability")
        credits_label.pack(pady=10)
        
        # Close button
        ttk.Button(content_frame, text="Close", command=about_window.destroy).pack(pady=10)
        
    def show_user_manual(self):
        """Show user manual window"""
        manual_window = tk.Toplevel(self.parent)
        manual_window.title(self.tr("user_manual"))
        manual_window.geometry("700x500")
        manual_window.transient(self.parent)
        
        # Center the window
        manual_window.geometry("+%d+%d" % (
            self.parent.winfo_rootx() + 50,
            self.parent.winfo_rooty() + 50
        ))
        
        # Create notebook for different help sections
        notebook = ttk.Notebook(manual_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Getting Started tab
        self._create_getting_started_tab(notebook)
        
        # Programming tab
        self._create_programming_tab(notebook)
        
        # Troubleshooting tab
        self._create_troubleshooting_tab(notebook)
        
        # FAQ tab
        self._create_faq_tab(notebook)
        
    def _create_getting_started_tab(self, notebook):
        """Create getting started help tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Getting Started")
        
        text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        content = """GETTING STARTED WITH PyK150

1. HARDWARE SETUP
   • Connect your K150/K128/K149/K182 programmer to USB port
   • Install programmer drivers if needed
   • Connect your PIC chip to the programmer socket

2. SOFTWARE SETUP
   • Ensure Python 3.6+ is installed
   • Install required dependencies: pip install -r requirements.txt
   • Install picpro: pip install picpro

3. FIRST USE
   • Launch PyK150: python3 pyk150_gui.py
   • Click "Refresh" to detect serial ports
   • Select your programmer port from dropdown
   • Choose your PIC type (e.g., 12F675, 16F84A)
   • Load your HEX file using "Browse" button

4. BASIC PROGRAMMING
   • Click "Program" to write HEX file to chip
   • Use "Verify" to check programming was successful
   • "Erase" will clear the chip memory

5. ADVANCED FEATURES
   • Enable ICSP for in-circuit programming
   • Set custom fuse values in the fuse settings area
   • Use Dump/Read tab to backup chip contents
   • Check Chip Info tab for detailed chip information

SUPPORTED PROGRAMMERS:
• K128 - Basic PIC programmer
• K149 (versions A to F) - Enhanced programmer
• K150 - Most common, fully tested
• K182 - Advanced programmer

NOTE: Programmer must have latest firmware with P18A protocol support."""

        text_widget.insert("1.0", content)
        text_widget.config(state=tk.DISABLED)
        
    def _create_programming_tab(self, notebook):
        """Create programming help tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Programming Guide")
        
        text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        content = """PROGRAMMING GUIDE

PROGRAMMING OPERATIONS:

1. PROGRAM
   • Writes HEX file data to PIC chip
   • Automatically programs ROM, EEPROM, and configuration
   • Use fuse settings to override configuration values

2. VERIFY
   • Compares chip contents with HEX file
   • Ensures programming was successful
   • Always verify after programming

3. ERASE
   • Clears all chip memory
   • Required before programming some chip types
   • Use when chip appears corrupted

4. DUMP/READ
   • ROM: Read program memory
   • EEPROM: Read data memory
   • CONFIG: Read configuration bits
   • Save as HEX or binary format

FUSE CONFIGURATION:
Format: FUSE_NAME:FUSE_VALUE
Example:
CONFIG1:0x3F4A
CONFIG2:0x1E00

Common fuses:
• FOSC - Oscillator selection
• WDTE - Watchdog timer enable
• PWRTE - Power-up timer enable
• MCLRE - Master clear enable
• CP - Code protection
• CPD - Data code protection

ICSP (In-Circuit Serial Programming):
• Enable for programming chips in circuit
• Requires ICSP-compatible circuit design
• Uses fewer pins than normal programming
• Useful for production programming

TIPS:
• Always verify after programming
• Use correct PIC type selection
• Check chip orientation in socket
• Ensure stable power supply
• Keep HEX files organized"""

        text_widget.insert("1.0", content)
        text_widget.config(state=tk.DISABLED)
        
    def _create_troubleshooting_tab(self, notebook):
        """Create troubleshooting help tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Troubleshooting")
        
        text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        content = """TROUBLESHOOTING GUIDE

COMMON PROBLEMS:

1. "No serial ports found"
   • Check USB connection
   • Install programmer drivers
   • Try different USB port
   • Check Device Manager (Windows) or lsusb (Linux)

2. "picpro command not found"
   • Install picpro: pip install picpro
   • Check Python PATH
   • Try: python -m pip install picpro

3. "Programming failed"
   • Check chip orientation in socket
   • Verify chip type selection
   • Ensure chip is not damaged
   • Try erasing chip first
   • Check power supply stability

4. "Verification failed"
   • Programming may have failed
   • Try programming again
   • Check for chip damage
   • Verify HEX file integrity

5. "Device not responding"
   • Check programmer firmware version
   • Try different baud rate
   • Reset programmer (unplug/replug USB)
   • Check for driver conflicts

6. "Permission denied" (Linux)
   • Add user to dialout group: sudo usermod -a -G dialout $USER
   • Log out and back in
   • Or run with sudo (not recommended)

HARDWARE CHECKS:
• LED indicators on programmer
• Chip properly seated in socket
• No bent pins on chip
• Clean socket contacts
• Stable USB connection

SOFTWARE CHECKS:
• Latest Python version
• All dependencies installed
• Correct picpro version
• HEX file not corrupted
• Sufficient disk space

GETTING HELP:
• Check output log for error details
• Enable debug mode if available
• Document exact error messages
• Note chip type and programmer model
• Check online forums and documentation"""

        text_widget.insert("1.0", content)
        text_widget.config(state=tk.DISABLED)
        
    def _create_faq_tab(self, notebook):
        """Create FAQ help tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="FAQ")
        
        text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        content = """FREQUENTLY ASKED QUESTIONS

Q: Which programmer should I buy?
A: K150 is the most popular and well-tested. Ensure it has the latest firmware with P18A protocol support.

Q: Can I program chips while they're in circuit?
A: Yes, enable ICSP mode. Your circuit must be designed for ICSP programming.

Q: What's the difference between HEX and binary files?
A: HEX files contain address information and are standard for PIC programming. Binary files are raw data dumps.

Q: Why do I need to select the correct PIC type?
A: Different PICs have different memory layouts, programming algorithms, and timing requirements.

Q: Can I backup a programmed chip?
A: Yes, use the Dump/Read tab to save ROM, EEPROM, and CONFIG to files.

Q: What are fuses/configuration bits?
A: Settings that control chip behavior like oscillator type, watchdog timer, code protection, etc.

Q: My chip seems corrupted, what should I do?
A: Try erasing the chip first, then reprogram. If that fails, the chip may be damaged.

Q: Can I use this with other programmers?
A: This GUI is designed for K150/K128/K149/K182 series. Other programmers may not work.

Q: Is this software free?
A: Yes, PyK150 is open source. The underlying picpro library is also free.

Q: How do I update the programmer firmware?
A: Check your programmer manufacturer's website for firmware updates and tools.

Q: Can I program multiple chips automatically?
A: This version doesn't support batch programming, but you can program chips one by one.

Q: What operating systems are supported?
A: Windows, Linux, and macOS with Python 3.6+ and tkinter support.

Q: Where are my settings saved?
A: Configuration is saved in ~/.pyk150/config.json on your system.

Q: How do I report bugs or request features?
A: Check the project repository or contact the developer through the about dialog."""

        text_widget.insert("1.0", content)
        text_widget.config(state=tk.DISABLED)
