#!/usr/bin/env python3
"""
PyK150 - Cross-platform PIC programmer GUI
A modern GUI for K150 compatible PIC programmers using picpro backend
"""

from version import __version__, get_version_info

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import serial
import serial.tools.list_ports
import os
import subprocess
import json
import sys
from pathlib import Path

# Import our custom modules
try:
    from config import Config
    from translations import Translations
    from device_detector import DeviceDetector
    from help_system import HelpSystem
    from chip_database import ChipDatabase
    from chip_placement_guide import ChipPlacementGuide
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please ensure all required files are in the same directory.")
    sys.exit(1)

class PicProgrammerGUI:
    def __init__(self, root):
        self.root = root
        
        # Initialize configuration and translations
        self.config = Config()
        self.tr = Translations()
        self.tr.set_language(self.config.get("language", "en"))
        
        # Initialize device detector
        self.device_detector = DeviceDetector()
        self.device_detector.add_detection_callback(self.on_device_detection)
        
        # Initialize help system
        self.help_system = HelpSystem(root, self.tr)
        
        # Initialize chip database
        self.chip_db = ChipDatabase()
        self.chip_db_loaded = False
        
        self.root.title(f"PyK150 v{__version__} - PIC Programmer GUI")
        geometry = self.config.get("window_geometry", "800x600")
        self.root.geometry(geometry)
        self.root.minsize(600, 500)
        
        # Variables
        self.hex_file_path = tk.StringVar(value=self.config.get("last_hex_file", ""))
        self.output_file_path = tk.StringVar()
        self.selected_port = tk.StringVar(value=self.config.get("last_port", ""))
        self.selected_pic_type = tk.StringVar(value=self.config.get("last_pic_type", "12F675"))
        self.icsp_enabled = tk.BooleanVar(value=self.config.get("icsp_enabled", False))
        self.binary_mode = tk.BooleanVar()
        
        # Auto-detection state
        self.auto_detection_active = False
        
        # Backend executable path
        self.backend_path = self.config.get_backend_executable()
        self.selected_backend = self.config.get("selected_backend", "picpro")
        
        # PIC types - will be loaded from database
        self.pic_types = []
        self.pic_families = {}
        
        # Memory types for dump operations
        self.memory_types = ["rom", "eeprom", "config"]
        
        self.setup_ui()
        self.setup_menu()
        self.refresh_ports()
        
        # Auto-detect devices if enabled
        if self.config.get("auto_detect_programmer", True):
            self.auto_detect_device()
            
        # Auto-detect backend if enabled
        if self.config.get("backend_auto_detect", True):
            self.auto_detect_backend()
            
        # Bind window close event to save configuration
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Start port monitoring
        self.device_detector.monitor_ports(self.on_port_change)
        
        # Load chip database in background
        self.load_chip_database()
        
        # Check backend version on startup
        self.check_backend_version_on_startup()
        
    def setup_ui(self):
        # Main frame with toolbar
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Toolbar
        self.setup_toolbar(main_frame)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        self.notebook = notebook
        
        # Main tab
        main_frame = ttk.Frame(notebook)
        notebook.add(main_frame, text="Programming")
        
        # Dump tab
        dump_frame = ttk.Frame(notebook)
        notebook.add(dump_frame, text="Dump/Read")
        
        # Info tab
        info_frame = ttk.Frame(notebook)
        notebook.add(info_frame, text="Chip Info")
        
        self.setup_main_tab(main_frame)
        self.setup_dump_tab(dump_frame)
        self.setup_info_tab(info_frame)
        
        # Status bar with additional info
        status_frame = ttk.Frame(self.root)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_var = tk.StringVar(value=self.tr("ready"))
        status_bar = ttk.Label(status_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Language indicator
        self.lang_var = tk.StringVar(value=self.tr.current_language.upper())
        lang_label = ttk.Label(status_frame, textvariable=self.lang_var, relief=tk.SUNKEN, width=5)
        lang_label.pack(side=tk.RIGHT)
        
        # Backend status indicator
        self.backend_status_var = tk.StringVar(value=f"Backend: {self.selected_backend}")
        backend_status = ttk.Label(status_frame, textvariable=self.backend_status_var, relief=tk.SUNKEN, width=15)
        backend_status.pack(side=tk.RIGHT)
        
        # Device status indicator
        self.device_status_var = tk.StringVar(value="No device")
        device_status = ttk.Label(status_frame, textvariable=self.device_status_var, relief=tk.SUNKEN, width=20)
        device_status.pack(side=tk.RIGHT)
        
    def setup_main_tab(self, parent):
        # Connection settings frame
        conn_frame = ttk.LabelFrame(parent, text=self.tr("connection_settings"), padding=10)
        conn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Port selection
        ttk.Label(conn_frame, text=self.tr("serial_port")).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        port_combo = ttk.Combobox(conn_frame, textvariable=self.selected_port, width=20)
        port_combo.grid(row=0, column=1, sticky=tk.W, padx=(0, 10))
        self.port_combo = port_combo
        
        ttk.Button(conn_frame, text=self.tr("refresh"), command=self.refresh_ports).grid(row=0, column=2, padx=5)
        ttk.Button(conn_frame, text=self.tr("auto_connect"), command=self.auto_detect_device).grid(row=0, column=3, padx=5)
        
        # PIC type selection
        ttk.Label(conn_frame, text=self.tr("pic_type")).grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        
        # PIC selection frame with search
        pic_frame = ttk.Frame(conn_frame)
        pic_frame.grid(row=1, column=1, columnspan=2, sticky=tk.EW, padx=(0, 10), pady=(10, 0))
        
        self.pic_combo = ttk.Combobox(pic_frame, textvariable=self.selected_pic_type, width=15)
        self.pic_combo.grid(row=0, column=0, sticky=tk.W)
        self.pic_combo.set(self.config.get("last_pic_type", "12F675"))
        
        # Search entry with autocomplete
        ttk.Label(pic_frame, text="Search:").grid(row=0, column=1, padx=(10, 5))
        self.chip_search_var = tk.StringVar()
        self.chip_search_var.trace('w', self.on_chip_search)
        self.search_entry = ttk.Entry(pic_frame, textvariable=self.chip_search_var, width=10)
        self.search_entry.grid(row=0, column=2)
        self.search_entry.bind('<KeyRelease>', self.on_search_keyrelease)
        
        # Family filter
        ttk.Label(pic_frame, text="Family:").grid(row=0, column=3, padx=(10, 5))
        self.family_var = tk.StringVar(value="All")
        self.family_combo = ttk.Combobox(pic_frame, textvariable=self.family_var, width=8, state="readonly")
        self.family_combo.grid(row=0, column=4)
        self.family_combo.bind('<<ComboboxSelected>>', self.on_family_change)
        
        conn_frame.columnconfigure(1, weight=1)
        
        # File selection frame
        file_frame = ttk.LabelFrame(parent, text=self.tr("file_selection"), padding=10)
        file_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # HEX file selection
        ttk.Label(file_frame, text=self.tr("hex_file")).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        ttk.Entry(file_frame, textvariable=self.hex_file_path, width=50).grid(row=0, column=1, sticky=tk.EW, padx=(0, 10))
        ttk.Button(file_frame, text=self.tr("browse"), command=self.browse_hex_file).grid(row=0, column=2)
        
        # Recent files dropdown
        recent_button = ttk.Menubutton(file_frame, text=self.tr("recent_files"))
        recent_button.grid(row=0, column=3, padx=(5, 0))
        self.recent_menu = tk.Menu(recent_button, tearoff=0)
        recent_button.config(menu=self.recent_menu)
        self.update_recent_files_menu()
        
        file_frame.columnconfigure(1, weight=1)
        
        # Options frame
        options_frame = ttk.LabelFrame(parent, text=self.tr("options"), padding=10)
        options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Checkbutton(options_frame, text=self.tr("enable_icsp"), variable=self.icsp_enabled).pack(anchor=tk.W)
        
        # Fuse settings
        fuse_frame = ttk.Frame(options_frame)
        fuse_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(fuse_frame, text=self.tr("fuse_settings")).pack(anchor=tk.W)
        self.fuse_text = tk.Text(fuse_frame, height=3, width=60)
        self.fuse_text.pack(fill=tk.X, pady=(5, 0))
        self.fuse_text.insert("1.0", self.tr("fuse_format"))
        
        # Operations frame
        ops_frame = ttk.LabelFrame(parent, text=self.tr("operations"), padding=10)
        ops_frame.pack(fill=tk.X, padx=10, pady=5)
        
        button_frame = ttk.Frame(ops_frame)
        button_frame.pack()
        
        ttk.Button(button_frame, text=self.tr("program"), command=self.program_chip, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.tr("verify"), command=self.verify_chip, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text=self.tr("erase"), command=self.erase_chip, width=12).pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(parent, mode='indeterminate')
        self.progress.pack(fill=tk.X, padx=10, pady=5)
        
        # Output log
        log_frame = ttk.LabelFrame(parent, text=self.tr("output_log"), padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
    def setup_dump_tab(self, parent):
        # Connection info (reference only)
        info_frame = ttk.LabelFrame(parent, text=self.tr("connection_info"), padding=10)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(info_frame, text=self.tr("uses_connection")).pack()
        
        # Output file selection
        file_frame = ttk.LabelFrame(parent, text=self.tr("output_file"), padding=10)
        file_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(file_frame, text=self.tr("output_file")).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        ttk.Entry(file_frame, textvariable=self.output_file_path, width=50).grid(row=0, column=1, sticky=tk.EW, padx=(0, 10))
        ttk.Button(file_frame, text=self.tr("browse"), command=self.browse_output_file).grid(row=0, column=2)
        
        file_frame.columnconfigure(1, weight=1)
        
        # Memory type selection
        mem_frame = ttk.LabelFrame(parent, text=self.tr("memory_type"), padding=10)
        mem_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.memory_type = tk.StringVar(value="rom")
        for i, mem_type in enumerate(self.memory_types):
            ttk.Radiobutton(mem_frame, text=self.tr(mem_type), variable=self.memory_type, 
                           value=mem_type).pack(side=tk.LEFT, padx=20)
        
        # Options
        dump_options_frame = ttk.LabelFrame(parent, text=self.tr("options"), padding=10)
        dump_options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Checkbutton(dump_options_frame, text=self.tr("binary_format"), variable=self.binary_mode).pack(anchor=tk.W)
        
        # Dump button
        ttk.Button(parent, text=self.tr("dump_memory"), command=self.dump_memory, width=20).pack(pady=20)
        
    def setup_info_tab(self, parent):
        # Create horizontal layout
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left side - Chip info
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Chip selection for info
        sel_frame = ttk.LabelFrame(left_frame, text="Chip Selection", padding=10)
        sel_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(sel_frame, text="Select Chip:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        # Chip info combo with search
        info_chip_frame = ttk.Frame(sel_frame)
        info_chip_frame.grid(row=0, column=1, sticky=tk.EW)
        
        self.info_chip_var = tk.StringVar()
        self.info_chip_combo = ttk.Combobox(info_chip_frame, textvariable=self.info_chip_var, width=20)
        self.info_chip_combo.grid(row=0, column=0, padx=(0, 10))
        self.info_chip_combo.bind('<<ComboboxSelected>>', self.on_info_chip_selected)
        
        ttk.Button(info_chip_frame, text=self.tr("get_chip_info"), command=self.get_chip_info).grid(row=0, column=1)
        
        sel_frame.columnconfigure(1, weight=1)
        
        # Chip info display
        info_display_frame = ttk.LabelFrame(left_frame, text=self.tr("chip_information"), padding=10)
        info_display_frame.pack(fill=tk.BOTH, expand=True)
        
        # Info text area with scrollbar
        text_frame = ttk.Frame(info_display_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.info_text = tk.Text(text_frame, wrap=tk.WORD, height=20)
        info_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=info_scrollbar.set)
        
        self.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        info_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Right side - Chip placement guide
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        
        # Initialize chip placement guide
        self.chip_guide = ChipPlacementGuide(right_frame, self.backend_path, self.selected_backend)
        self.chip_guide.get_frame().pack(fill=tk.BOTH, expand=True)
    
    def on_info_chip_selected(self, event=None):
        """Handle chip selection in info tab"""
        selected_chip = self.info_chip_var.get()
        if selected_chip and hasattr(self, 'chip_guide'):
            self.chip_guide.update_chip_guide(selected_chip)
        
    def refresh_ports(self):
        """Refresh available serial ports"""
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.port_combo['values'] = ports
        
        # Auto-select /dev/ttyUSB0 if available
        if "/dev/ttyUSB0" in ports:
            self.selected_port.set("/dev/ttyUSB0")
            self.log_message("Auto-selected /dev/ttyUSB0")
        elif ports:
            self.selected_port.set(ports[0])
            self.log_message(f"Auto-selected first available port: {ports[0]}")
        else:
            self.log_message("No serial ports found")
            
        self.log_message(f"Found {len(ports)} serial ports: {', '.join(ports)}")
        
    def setup_menu(self):
        """Setup application menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.tr("file"), menu=file_menu)
        file_menu.add_command(label=self.tr("open"), command=self.browse_hex_file, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label=self.tr("exit"), command=self.on_closing, accelerator="Ctrl+Q")
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.tr("tools"), menu=tools_menu)
        tools_menu.add_command(label=self.tr("preferences"), command=self.show_preferences)
        tools_menu.add_command(label=self.tr("auto_connect"), command=self.auto_detect_device)
        
        # Language submenu
        lang_menu = tk.Menu(tools_menu, tearoff=0)
        tools_menu.add_cascade(label="Language", menu=lang_menu)
        lang_menu.add_command(label="English", command=lambda: self.change_language("en"))
        lang_menu.add_command(label="Türkçe", command=lambda: self.change_language("tr"))
        lang_menu.add_command(label="Deutsch", command=lambda: self.change_language("de"))
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.tr("help"), menu=help_menu)
        help_menu.add_command(label=self.tr("user_manual"), command=self.help_system.show_user_manual)
        help_menu.add_separator()
        help_menu.add_command(label=self.tr("about"), command=self.help_system.show_about_dialog)
        
        # Keyboard shortcuts
        self.root.bind('<Control-o>', lambda e: self.browse_hex_file())
        self.root.bind('<Control-q>', lambda e: self.on_closing())
        
    def setup_toolbar(self, parent):
        """Setup toolbar"""
        toolbar = ttk.Frame(parent)
        toolbar.pack(fill=tk.X, padx=10, pady=(10, 0))
        
        # Quick action buttons
        ttk.Button(toolbar, text=self.tr("auto_connect"), command=self.auto_detect_device).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text=self.tr("refresh"), command=self.refresh_ports).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Test Backend", command=self.test_current_backend).pack(side=tk.LEFT, padx=5)
        
        # Separator
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Backend selector
        ttk.Label(toolbar, text="Backend:").pack(side=tk.LEFT, padx=(0, 5))
        backend_combo = ttk.Combobox(toolbar, values=["picpro", "picp", "auto"], width=8, state="readonly")
        backend_combo.set(self.selected_backend)
        backend_combo.bind('<<ComboboxSelected>>', lambda e: self.change_backend(backend_combo.get()))
        backend_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        # Language selector
        ttk.Label(toolbar, text="Lang:").pack(side=tk.LEFT, padx=(0, 5))
        lang_combo = ttk.Combobox(toolbar, values=["en", "tr", "de"], width=5, state="readonly")
        lang_combo.set(self.tr.current_language)
        lang_combo.bind('<<ComboboxSelected>>', lambda e: self.change_language(lang_combo.get()))
        lang_combo.pack(side=tk.LEFT)
        
    def browse_hex_file(self):
        """Browse for HEX file"""
        initial_dir = self.config.get("last_output_dir", str(Path.home()))
        filename = filedialog.askopenfilename(
            title=self.tr("select_hex"),
            initialdir=initial_dir,
            filetypes=[("HEX files", "*.hex"), ("All files", "*.*")]
        )
        if filename:
            self.hex_file_path.set(filename)
            self.config.add_recent_file(filename)
            self.config.set("last_hex_file", filename)
            self.config.set("last_output_dir", str(Path(filename).parent))
            self.update_recent_files_menu()
            
    def browse_output_file(self):
        """Browse for output file"""
        initial_dir = self.config.get("last_output_dir", str(Path.home()))
        filename = filedialog.asksaveasfilename(
            title="Save Output File",
            initialdir=initial_dir,
            filetypes=[("HEX files", "*.hex"), ("Binary files", "*.bin"), ("All files", "*.*")]
        )
        if filename:
            self.output_file_path.set(filename)
            self.config.set("last_output_dir", str(Path(filename).parent))
            
    def update_recent_files_menu(self):
        """Update recent files menu"""
        self.recent_menu.delete(0, tk.END)
        recent_files = self.config.get_recent_files()
        
        if recent_files:
            for file_path in recent_files:
                filename = Path(file_path).name
                self.recent_menu.add_command(
                    label=filename,
                    command=lambda f=file_path: self.load_recent_file(f)
                )
            self.recent_menu.add_separator()
            self.recent_menu.add_command(
                label=self.tr("clear_recent"),
                command=self.clear_recent_files
            )
        else:
            self.recent_menu.add_command(label="No recent files", state=tk.DISABLED)
            
    def load_recent_file(self, filepath):
        """Load a recent file"""
        if os.path.exists(filepath):
            self.hex_file_path.set(filepath)
        else:
            messagebox.showerror(self.tr("error"), f"File not found: {filepath}")
            # Remove from recent files
            recent = self.config.get("recent_files", [])
            if filepath in recent:
                recent.remove(filepath)
                self.config.set("recent_files", recent)
                self.update_recent_files_menu()
                
    def clear_recent_files(self):
        """Clear recent files list"""
        self.config.set("recent_files", [])
        self.update_recent_files_menu()
            
    def log_message(self, message):
        """Add message to log"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def update_status(self, message):
        """Update status bar"""
        self.status_var.set(message)
        self.root.update_idletasks()
        
    def validate_inputs(self, operation):
        """Validate required inputs with enhanced error handling"""
        try:
            if not self.selected_port.get():
                messagebox.showerror(self.tr("error"), self.tr("select_port"))
                return False
                
            if not self.selected_pic_type.get():
                messagebox.showerror(self.tr("error"), self.tr("select_pic"))
                return False
                
            if operation in ["program", "verify"] and not self.hex_file_path.get():
                messagebox.showerror(self.tr("error"), self.tr("select_hex"))
                return False
                
            # Validate HEX file exists
            if operation in ["program", "verify"] and not os.path.exists(self.hex_file_path.get()):
                messagebox.showerror(self.tr("error"), f"HEX file not found: {self.hex_file_path.get()}")
                return False
                
            if operation == "dump" and not self.output_file_path.get():
                messagebox.showerror(self.tr("error"), self.tr("specify_output"))
                return False
                
            # Check if port is accessible
            try:
                with serial.Serial(self.selected_port.get(), timeout=0.1):
                    pass
            except (serial.SerialException, OSError) as e:
                messagebox.showerror(self.tr("error"), f"Cannot access port {self.selected_port.get()}: {str(e)}")
                return False
                
            return True
        except Exception as e:
            messagebox.showerror(self.tr("error"), f"Validation error: {str(e)}")
            return False
        
    def build_command(self, operation):
        """Build backend command"""
        # Use configured backend path or fallback to backend name
        backend_exe = self.backend_path if self.backend_path else self.selected_backend
        cmd = [backend_exe, operation]
        
        # Add port
        cmd.extend(["-p", self.selected_port.get()])
        
        # Add PIC type
        cmd.extend(["-t", self.selected_pic_type.get()])
        
        # Add file parameters
        if operation in ["program", "verify"]:
            cmd.extend(["-i", self.hex_file_path.get()])
        elif operation == "dump":
            cmd.extend([self.memory_type.get(), "-o", self.output_file_path.get()])
            if self.binary_mode.get():
                cmd.append("--binary")
                
        # Add ICSP if enabled
        if self.icsp_enabled.get():
            cmd.append("--icsp")
            
        # Add fuse settings for program operation
        if operation == "program":
            fuse_content = self.fuse_text.get("1.0", tk.END).strip()
            for line in fuse_content.split('\n'):
                line = line.strip()
                if line and not line.startswith('#') and ':' in line:
                    cmd.extend(["--fuse", line])
                    
        return cmd
        
    def run_command_async(self, cmd, operation):
        """Run command in separate thread"""
        def run():
            try:
                self.progress.start()
                self.update_status(f"Running {operation}...")
                self.log_message(f"Executing: {' '.join(cmd)}")
                
                # Run the command
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                
                # Log output
                if result.stdout:
                    self.log_message(f"Output: {result.stdout}")
                if result.stderr:
                    self.log_message(f"Error: {result.stderr}")
                    
                # Check for actual operation success by analyzing output content
                operation_success = self._check_operation_success(operation, result)
                
                if result.returncode == 0 and operation_success:
                    self.log_message(f"{operation.capitalize()} completed successfully!")
                    self.update_status(f"{operation.capitalize()} completed")
                    messagebox.showinfo(self.tr("success"), self.tr("operation_completed"))
                    # Save successful settings
                    self.save_current_settings()
                else:
                    if result.returncode == 0 and not operation_success:
                        self.log_message(f"{operation.capitalize()} completed with errors (see output above)")
                        self.update_status(f"{operation.capitalize()} failed")
                        messagebox.showerror(self.tr("error"), self.tr("operation_failed"))
                    else:
                        self.log_message(f"{operation.capitalize()} failed with return code {result.returncode}")
                        self.update_status(f"{operation.capitalize()} failed")
                        messagebox.showerror(self.tr("error"), self.tr("operation_failed"))
                    
            except subprocess.TimeoutExpired:
                self.log_message(f"{operation.capitalize()} timed out")
                self.update_status(self.tr("operation_timeout"))
                messagebox.showerror(self.tr("error"), self.tr("operation_timeout"))
            except FileNotFoundError:
                backend_name = self.selected_backend
                self.log_message(f"{backend_name} command not found. Please install {backend_name} first.")
                self.update_status(f"{backend_name} not found")
                messagebox.showerror(self.tr("error"), f"{backend_name} command not found.\nPlease install {backend_name} first.")
            except Exception as e:
                self.log_message(f"Error: {str(e)}")
                self.update_status("Error occurred")
                messagebox.showerror(self.tr("error"), f"An error occurred: {str(e)}")
            finally:
                self.progress.stop()
                
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()
    
    def _check_operation_success(self, operation, result):
        """Check if operation actually succeeded by analyzing output content"""
        output = result.stdout.lower() if result.stdout else ""
        
        # Common failure indicators
        failure_indicators = [
            "failed", "error", "verification failed", "programming failed",
            "unable to", "timeout", "not found", "invalid", "locked"
        ]
        
        # Operation-specific success indicators
        success_indicators = {
            "program": ["programming rom", "done!"],
            "verify": ["verifying rom", "verification successful"],
            "erase": ["erasing", "done!"],
            "dump": ["dumping", "saved to"]
        }
        
        # Check for failure indicators first
        for indicator in failure_indicators:
            if indicator in output:
                return False
        
        # Check for operation-specific success
        if operation in success_indicators:
            required_indicators = success_indicators[operation]
            for indicator in required_indicators:
                if indicator in output:
                    # For verify operation, also check that no verification failed
                    if operation == "verify" and "verification failed" in output:
                        return False
                    return True
        
        # Default: if no specific indicators found, trust return code
        return result.returncode == 0
        
    def program_chip(self):
        """Program the chip"""
        if self.validate_inputs("program"):
            # Validate HEX file size before programming
            hex_file = self.hex_file_path.get()
            chip_type = self.selected_pic_type.get()
            
            if hex_file and chip_type:
                is_valid, message = self.chip_db.validate_hex_file_size(hex_file, chip_type)
                if not is_valid:
                    messagebox.showerror(
                        self.tr("error"),
                        f"{self.tr('hex_file_too_large')}\n\n{message}"
                    )
                    self.log_message(f"HEX file validation failed: {message}")
                    return
                else:
                    self.log_message(f"HEX file validation: {message}")
            
            cmd = self.build_command("program")
            self.run_command_async(cmd, "program")
            
    def verify_chip(self):
        """Verify the chip"""
        if self.validate_inputs("verify"):
            cmd = self.build_command("verify")
            self.run_command_async(cmd, "verify")
            
    def erase_chip(self):
        """Erase the chip"""
        if self.validate_inputs("erase"):
            cmd = self.build_command("erase")
            self.run_command_async(cmd, "erase")
            
    def dump_memory(self):
        """Dump memory from chip"""
        if self.validate_inputs("dump"):
            cmd = self.build_command("dump")
            self.run_command_async(cmd, "dump")
            
    def auto_detect_device(self):
        """Auto-detect programmer device"""
        if self.auto_detection_active:
            return
            
        self.auto_detection_active = True
        self.update_status(self.tr("detecting_devices"))
        
        def on_detection_complete(device_info, error):
            self.auto_detection_active = False
            if device_info:
                self.selected_port.set(device_info['port'])
                self.device_status_var.set(f"{device_info['device_type']}")
                self.update_status(self.tr("device_found"))
                self.log_message(f"Auto-detected: {device_info['port']} - {device_info['device_type']}")
            else:
                self.device_status_var.set("No device")
                self.update_status(self.tr("no_device_found"))
                self.log_message(f"Auto-detection failed: {error}")
                
        self.device_detector.auto_detect_programmer(on_detection_complete)
        
    def auto_detect_backend(self):
        """Auto-detect best available backend"""
        # Check if user has explicitly selected a backend
        selected_backend = self.config.get("selected_backend", "picpro")
        
        if selected_backend == "auto":
            # Auto-detect best available backend
            picpro_path = self.config.find_picpro_executable()
            picp_path = self.config.find_picp_executable()
            
            if picp_path:
                # Prefer picp if available
                self.selected_backend = "picp"
                self.backend_path = picp_path
                self.log_message("Auto-detected picp backend")
            elif picpro_path:
                # Fallback to picpro
                self.selected_backend = "picpro"
                self.backend_path = picpro_path
                self.log_message("Auto-detected picpro backend")
            else:
                # No backend found
                self.selected_backend = "picpro"  # Default
                self.backend_path = ""
                self.log_message("No backend found, using picpro as default")
        else:
            # Use user-selected backend
            self.selected_backend = selected_backend
            if selected_backend == "picpro":
                self.backend_path = self.config.find_picpro_executable()
            elif selected_backend == "picp":
                self.backend_path = self.config.find_picp_executable()
            else:
                self.backend_path = ""
            
            self.log_message(f"Using selected backend: {self.selected_backend}")
            
        # Update status
        self.backend_status_var.set(f"Backend: {self.selected_backend}")
        self.config.set("selected_backend", self.selected_backend)
        
    def on_device_detection(self, event, data):
        """Handle device detection events"""
        if event == 'detection_started':
            self.device_status_var.set("Detecting...")
        elif event == 'device_found':
            self.device_status_var.set(data['device_type'])
        elif event == 'no_devices_found':
            self.device_status_var.set("No device")
        elif event == 'testing_port':
            self.device_status_var.set(f"Testing {data['port']}")
            
    def on_port_change(self, all_ports, added_ports, removed_ports):
        """Handle port changes"""
        if added_ports:
            self.log_message(f"New ports detected: {', '.join(added_ports)}")
            self.refresh_ports()
        if removed_ports:
            self.log_message(f"Ports disconnected: {', '.join(removed_ports)}")
            self.refresh_ports()
            
    def change_backend(self, backend):
        """Change backend selection"""
        self.selected_backend = backend
        self.config.set("selected_backend", backend)
        self.backend_path = self.config.get_backend_executable()
        self.backend_status_var.set(f"Backend: {backend}")
        
        # Update chip placement guide with new backend
        if hasattr(self, 'chip_guide'):
            self.chip_guide.update_backend(self.backend_path, self.selected_backend)
        
        # Log the change
        self.log_message(f"Backend changed to: {backend}")
        
    def test_current_backend(self):
        """Test current backend"""
        if not self.backend_path:
            messagebox.showerror(self.tr("error"), self.tr("backend_not_set"))
            return
            
        is_valid, message = self.config.validate_backend_path(self.backend_path)
        if is_valid:
            messagebox.showinfo(self.tr("success"), f"{self.tr('backend_valid')}\n\nBackend: {self.selected_backend}\nPath: {self.backend_path}")
        else:
            messagebox.showerror(self.tr("error"), f"{self.tr('backend_invalid')}\n\nError: {message}")
        
    def change_language(self, language):
        """Change application language"""
        self.tr.set_language(language)
        self.config.set("language", language)
        self.lang_var.set(language.upper())
        
        # Show restart message
        messagebox.showinfo(
            "Language Changed",
            "Language has been changed. Please restart the application to see all changes."
        )
        
    def show_preferences(self):
        """Show preferences dialog"""
        prefs_window = tk.Toplevel(self.root)
        prefs_window.title(self.tr("preferences"))
        prefs_window.geometry("400x300")
        prefs_window.transient(self.root)
        prefs_window.grab_set()
        
        # Center the window
        prefs_window.geometry("+%d+%d" % (
            self.root.winfo_rootx() + 50,
            self.root.winfo_rooty() + 50
        ))
        
        notebook = ttk.Notebook(prefs_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # General tab
        general_frame = ttk.Frame(notebook)
        notebook.add(general_frame, text="General")
        
        ttk.Label(general_frame, text="Language:").pack(anchor=tk.W, pady=(10, 5))
        lang_var = tk.StringVar(value=self.config.get("language", "en"))
        lang_combo = ttk.Combobox(general_frame, textvariable=lang_var, values=["en", "tr"], state="readonly")
        lang_combo.pack(anchor=tk.W, fill=tk.X, padx=(0, 10))
        
        auto_detect_var = tk.BooleanVar(value=self.config.get("auto_detect_programmer", True))
        ttk.Checkbutton(general_frame, text="Auto-detect programmer on startup", variable=auto_detect_var).pack(anchor=tk.W, pady=10)
        
        # Backend tab
        backend_frame = ttk.Frame(notebook)
        notebook.add(backend_frame, text="Backend")
        
        # Backend selection
        ttk.Label(backend_frame, text=self.tr("select_backend")).pack(anchor=tk.W, pady=(10, 5))
        
        backend_selection_frame = ttk.Frame(backend_frame)
        backend_selection_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.backend_var = tk.StringVar(value=self.config.get("selected_backend", "picpro"))
        backend_combo = ttk.Combobox(backend_selection_frame, textvariable=self.backend_var, 
                                   values=["picpro", "picp", "auto"], state="readonly", width=15)
        backend_combo.pack(side=tk.LEFT, padx=(0, 10))
        backend_combo.bind('<<ComboboxSelected>>', self.on_backend_change)
        
        # Auto-detect option
        auto_detect_var = tk.BooleanVar(value=self.config.get("backend_auto_detect", True))
        ttk.Checkbutton(backend_selection_frame, text=self.tr("auto_detect_backend"), variable=auto_detect_var).pack(side=tk.LEFT)
        
        # Backend path setting
        ttk.Label(backend_frame, text=self.tr("backend_path")).pack(anchor=tk.W, pady=(10, 5))
        
        path_frame = ttk.Frame(backend_frame)
        path_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Initialize backend path based on selected backend
        backend = self.backend_var.get()
        if backend == "picpro":
            self.backend_path_var = tk.StringVar(value=self.config.get("picpro_path", ""))
        elif backend == "picp":
            self.backend_path_var = tk.StringVar(value=self.config.get("picp_path", ""))
        else:
            self.backend_path_var = tk.StringVar(value="")
        path_entry = ttk.Entry(path_frame, textvariable=self.backend_path_var)
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        ttk.Button(path_frame, text=self.tr("browse_backend"), command=self.browse_backend_path).pack(side=tk.LEFT, padx=5)
        ttk.Button(path_frame, text=self.tr("test_backend"), command=self.test_backend_path).pack(side=tk.LEFT)
        
        # Auto-find option
        auto_find_var = tk.BooleanVar(value=self.config.get("auto_find_picpro", True))
        ttk.Checkbutton(backend_frame, text=self.tr("auto_find_backend"), variable=auto_find_var).pack(anchor=tk.W, pady=5)
        
        # Status label
        self.backend_status_var = tk.StringVar()
        self.update_backend_status()
        status_label = ttk.Label(backend_frame, textvariable=self.backend_status_var, foreground="blue")
        status_label.pack(anchor=tk.W, pady=5)
        
        # Save button
        def save_prefs():
            self.config.set("language", lang_var.get())
            self.config.set("auto_detect_programmer", auto_detect_var.get())
            self.config.set("selected_backend", self.backend_var.get())
            self.config.set("backend_auto_detect", auto_detect_var.get())
            
            # Update backend-specific settings
            backend = self.backend_var.get()
            if backend == "picpro":
                self.config.set("picpro_path", self.backend_path_var.get())
                self.config.set("auto_find_picpro", auto_find_var.get())
            elif backend == "picp":
                self.config.set("picp_path", self.backend_path_var.get())
                self.config.set("auto_find_picp", auto_find_var.get())
            
            # Update current backend path
            self.selected_backend = backend
            self.backend_path = self.config.get_backend_executable()
            self.backend_status_var.set(f"Backend: {backend}")
            
            # Update chip placement guide with new backend
            if hasattr(self, 'chip_guide'):
                self.chip_guide.update_backend(self.backend_path, self.selected_backend)
                
            prefs_window.destroy()
            
        ttk.Button(prefs_window, text="Save", command=save_prefs).pack(pady=10)
        
    def save_current_settings(self):
        """Save current settings to config"""
        self.config.set("last_port", self.selected_port.get())
        self.config.set("last_pic_type", self.selected_pic_type.get())
        self.config.set("icsp_enabled", self.icsp_enabled.get())
        self.config.set("window_geometry", self.root.geometry())
        
    def on_backend_change(self, event=None):
        """Handle backend selection change"""
        backend = self.backend_var.get()
        
        # Update path variable based on selected backend
        if backend == "picpro":
            self.backend_path_var.set(self.config.get("picpro_path", ""))
        elif backend == "picp":
            self.backend_path_var.set(self.config.get("picp_path", ""))
        elif backend == "auto":
            self.backend_path_var.set("")
        
        self.update_backend_status()
    
    def browse_backend_path(self):
        """Browse for backend executable"""
        filename = filedialog.askopenfilename(
            title=self.tr("browse_backend"),
            filetypes=[("Executable files", "*"), ("All files", "*.*")]
        )
        if filename:
            self.backend_path_var.set(filename)
            self.update_backend_status()
            
    def test_backend_path(self):
        """Test backend executable"""
        path = self.backend_path_var.get()
        backend = self.backend_var.get()
        
        if not path:
            if backend == "picpro":
                path = self.config.find_picpro_executable()
            elif backend == "picp":
                path = self.config.find_picp_executable()
            else:
                path = self.config.get_backend_executable()
            
        if not path:
            messagebox.showerror(self.tr("error"), self.tr("backend_not_set"))
            return
            
        is_valid, message = self.config.validate_backend_path(path)
        if is_valid:
            messagebox.showinfo(self.tr("success"), f"{self.tr('backend_valid')}\n\nPath: {path}")
        else:
            messagebox.showerror(self.tr("error"), f"{self.tr('backend_invalid')}\n\nError: {message}")
            
        self.update_backend_status()
        
    def update_backend_status(self):
        """Update backend status display"""
        if hasattr(self, 'backend_status_var'):
            backend = self.backend_var.get() if hasattr(self, 'backend_var') else self.selected_backend
            path = self.backend_path_var.get() if hasattr(self, 'backend_path_var') else self.backend_path
            
            if not path:
                if backend == "picpro":
                    path = self.config.find_picpro_executable()
                elif backend == "picp":
                    path = self.config.find_picp_executable()
                else:
                    path = self.config.get_backend_executable()
                
            if path:
                is_valid, message = self.config.validate_backend_path(path)
                if is_valid:
                    self.backend_status_var.set(f"✓ Valid {backend}: {path}")
                else:
                    self.backend_status_var.set(f"✗ Invalid {backend}: {message}")
            else:
                self.backend_status_var.set(f"✗ {backend.capitalize()} not found")
    
    def browse_picpro_path(self):
        """Browse for picpro executable (legacy)"""
        filename = filedialog.askopenfilename(
            title=self.tr("browse_picpro"),
            filetypes=[("Executable files", "*"), ("All files", "*.*")]
        )
        if filename:
            self.picpro_path_var.set(filename)
            self.update_picpro_status()
            
    def test_picpro_path(self):
        """Test picpro executable (legacy)"""
        path = self.picpro_path_var.get()
        if not path:
            path = self.config.find_picpro_executable()
            
        if not path:
            messagebox.showerror(self.tr("error"), self.tr("picpro_not_set"))
            return
            
        is_valid, message = self.config.validate_picpro_path(path)
        if is_valid:
            messagebox.showinfo(self.tr("success"), f"{self.tr('picpro_valid')}\n\nPath: {path}")
        else:
            messagebox.showerror(self.tr("error"), f"{self.tr('picpro_invalid')}\n\nError: {message}")
            
        self.update_picpro_status()
        
    def update_picpro_status(self):
        """Update picpro status display (legacy)"""
        if hasattr(self, 'picpro_status_var'):
            path = self.picpro_path_var.get() if hasattr(self, 'picpro_path_var') else self.picpro_path
            if not path:
                path = self.config.find_picpro_executable()
                
            if path:
                is_valid, message = self.config.validate_picpro_path(path)
                if is_valid:
                    self.picpro_status_var.set(f"✓ Valid: {path}")
                else:
                    self.picpro_status_var.set(f"✗ Invalid: {message}")
            else:
                self.picpro_status_var.set("✗ Picpro not found")

    def load_chip_database(self):
        """Load chip database in background thread"""
        def load():
            try:
                self.update_status("Loading chip database...")
                success = self.chip_db.initialize()
                if success:
                    self.chip_db_loaded = True
                    self.pic_types = self.chip_db.get_all_chips()
                    self.pic_families = self.chip_db.get_chips_by_family()
                    
                    # Update GUI in main thread
                    self.root.after(0, self.update_chip_lists)
                    self.log_message(f"Loaded {len(self.pic_types)} PIC chips from database")
                    self.update_status(self.tr("ready"))
                else:
                    # Fallback to basic chip list
                    self.pic_types = [
                        "12F675", "12F683", "12F1840", "16F84A", "16F628A", "16F648A",
                        "16F88", "16F877A", "16F887", "16F1827", "16F1847", "18F2550",
                        "18F4550", "18F25K50", "18F45K50", "18F2580", "18F4580"
                    ]
                    self.root.after(0, self.update_chip_lists)
                    self.log_message("Using fallback chip list")
                    self.update_status(self.tr("ready"))
            except Exception as e:
                self.log_message(f"Error loading chip database: {e}")
                # Use fallback list
                self.pic_types = [
                    "12F675", "12F683", "12F1840", "16F84A", "16F628A", "16F648A",
                    "16F88", "16F877A", "16F887", "16F1827", "16F1847", "18F2550",
                    "18F4550", "18F25K50", "18F45K50", "18F2580", "18F4580"
                ]
                self.root.after(0, self.update_chip_lists)
                self.update_status(self.tr("ready"))
                
        thread = threading.Thread(target=load)
        thread.daemon = True
        thread.start()
        
    def update_chip_lists(self):
        """Update chip combo boxes with loaded data"""
        if hasattr(self, 'pic_combo'):
            # Update main PIC combo
            self.pic_combo['values'] = self.pic_types
            
            # Update family combo
            if hasattr(self, 'family_combo') and self.pic_families:
                families = ["All"] + sorted(self.pic_families.keys())
                self.family_combo['values'] = families
                
            # Update info tab combo
            if hasattr(self, 'info_chip_combo'):
                self.info_chip_combo['values'] = self.pic_types
                
    def on_chip_search(self, *args):
        """Handle chip search"""
        if not self.chip_db_loaded:
            return
            
        search_text = self.chip_search_var.get()
        if len(search_text) < 2:
            # Show all chips if search is too short
            filtered_chips = self.pic_types
        else:
            # Search in chip database
            filtered_chips = self.chip_db.search_chips(search_text)
            
        # Apply family filter if set
        selected_family = self.family_var.get()
        if selected_family != "All" and selected_family in self.pic_families:
            family_chips = self.pic_families[selected_family]
            filtered_chips = [chip for chip in filtered_chips if chip in family_chips]
            
        # Update combo box
        if hasattr(self, 'pic_combo'):
            self.pic_combo['values'] = filtered_chips[:50]  # Limit to 50 results
            
    def on_family_change(self, event=None):
        """Handle family filter change"""
        if not self.chip_db_loaded:
            return
            
        selected_family = self.family_var.get()
        
        if selected_family == "All":
            filtered_chips = self.pic_types
        else:
            filtered_chips = self.pic_families.get(selected_family, [])
            
        # Apply search filter if set
        search_text = self.chip_search_var.get()
        if len(search_text) >= 2:
            search_results = self.chip_db.search_chips(search_text)
            filtered_chips = [chip for chip in filtered_chips if chip in search_results]
            
        # Update combo box
        if hasattr(self, 'pic_combo'):
            self.pic_combo['values'] = filtered_chips[:50]  # Limit to 50 results
            
    def on_search_keyrelease(self, event):
        """Handle search entry key release for smart autocomplete"""
        if not self.chip_db_loaded:
            return
            
        search_text = self.chip_search_var.get().upper()
        
        # Smart autocomplete for partial chip names
        if len(search_text) >= 2:
            # Find chips that start with the search text
            matching_chips = []
            for chip in self.pic_types:
                if chip.upper().startswith(search_text):
                    matching_chips.append(chip)
            
            # If we have matches and user pressed Tab or Enter, auto-complete to first match
            if matching_chips and event.keysym in ['Tab', 'Return']:
                first_match = matching_chips[0]
                self.chip_search_var.set(first_match)
                self.selected_pic_type.set(first_match)
                # Move cursor to end
                self.search_entry.icursor(tk.END)
                return "break"  # Prevent default Tab behavior
            
            # For partial matches like "16F", show suggestions in combo
            if len(search_text) >= 3:
                # Apply family filter if set
                selected_family = self.family_var.get()
                if selected_family != "All" and selected_family in self.pic_families:
                    family_chips = self.pic_families[selected_family]
                    matching_chips = [chip for chip in matching_chips if chip in family_chips]
                
                # Update combo with suggestions
                if hasattr(self, 'pic_combo'):
                    self.pic_combo['values'] = matching_chips[:20]  # Show top 20 matches
                    
    def check_backend_version_on_startup(self):
        """Check backend version on application startup"""
        def check():
            try:
                backend_path = self.config.get_backend_executable()
                if backend_path:
                    is_valid, message = self.config.validate_backend_path(backend_path)
                    
                    # Schedule GUI update in main thread
                    self.root.after(0, lambda: self.handle_version_check_result(is_valid, message, backend_path))
                else:
                    self.root.after(0, lambda: self.handle_version_check_result(False, "Backend not found", ""))
            except Exception as e:
                self.root.after(0, lambda: self.handle_version_check_result(False, f"Version check error: {e}", ""))
                
        # Run in background thread
        thread = threading.Thread(target=check)
        thread.daemon = True
        thread.start()
        
    def handle_version_check_result(self, is_valid, message, backend_path):
        """Handle version check result in main thread"""
        if not is_valid and "version" in message.lower() and "too old" in message.lower():
            # Show version warning dialog
            self.show_version_warning(message, backend_path)
        elif not is_valid and backend_path:
            # Log other validation issues
            self.log_message(f"Backend validation: {message}")
            
    def show_version_warning(self, message, backend_path):
        """Show version warning dialog"""
        backend_name = self.selected_backend
        min_version = "0.3.0" if backend_name == "picpro" else "1.0.0"
        
        warning_msg = (
            f"⚠️ {backend_name.capitalize()} Version Warning\n\n"
            f"Found {backend_name} at: {backend_path}\n"
            f"Issue: {message}\n\n"
            f"PyK150 requires {backend_name} version {min_version} or higher for optimal compatibility.\n"
            f"Some features may not work correctly with older versions.\n\n"
            f"Please update {backend_name} to the latest version:\n"
            f"• Visit: https://github.com/Salamek/{backend_name}\n"
            f"• Or run: pip install --upgrade {backend_name}\n\n"
            f"Continue anyway?"
        )
        
        result = messagebox.askyesno(
            f"{backend_name.capitalize()} Version Warning",
            warning_msg,
            icon="warning"
        )
        
        if not result:
            # User chose not to continue
            self.log_message(f"Application closed due to {backend_name} version incompatibility")
            self.on_closing()

    def get_chip_info(self):
        """Get chip information"""
        # Use chip from info tab if available, otherwise main selection
        chip_name = self.info_chip_var.get() if hasattr(self, 'info_chip_var') and self.info_chip_var.get() else self.selected_pic_type.get()
        
        if not chip_name:
            messagebox.showerror(self.tr("error"), self.tr("select_pic"))
            return
            
        def run():
            try:
                self.update_status("Getting chip info...")
                backend_exe = self.backend_path if self.backend_path else self.selected_backend
                cmd = [backend_exe, "chipinfo", chip_name]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    self.info_text.delete("1.0", tk.END)
                    try:
                        # Try to format JSON nicely
                        info_data = json.loads(result.stdout)
                        formatted_info = json.dumps(info_data, indent=2)
                        self.info_text.insert("1.0", formatted_info)
                    except json.JSONDecodeError:
                        self.info_text.insert("1.0", result.stdout)
                    self.update_status("Chip info retrieved")
                else:
                    self.info_text.delete("1.0", tk.END)
                    self.info_text.insert("1.0", f"Error: {result.stderr}")
                    self.update_status("Failed to get chip info")
                    
            except Exception as e:
                self.info_text.delete("1.0", tk.END)
                self.info_text.insert("1.0", f"Error: {str(e)}")
                self.update_status("Error occurred")
                
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()
        
    def get_hex_info(self):
        """Get HEX file information"""
        if not self.hex_file_path.get():
            messagebox.showerror(self.tr("error"), self.tr("select_hex"))
            return
            
        if not self.selected_pic_type.get():
            messagebox.showerror(self.tr("error"), self.tr("select_pic"))
            return
            
        def run():
            try:
                self.update_status("Getting HEX info...")
                backend_exe = self.backend_path if self.backend_path else self.selected_backend
                cmd = [backend_exe, "hexinfo", self.hex_file_path.get(), self.selected_pic_type.get()]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    self.info_text.delete("1.0", tk.END)
                    self.info_text.insert("1.0", result.stdout)
                    self.update_status("HEX info retrieved")
                else:
                    self.info_text.delete("1.0", tk.END)
                    self.info_text.insert("1.0", f"Error: {result.stderr}")
                    self.update_status("Failed to get HEX info")
                    
            except Exception as e:
                self.info_text.delete("1.0", tk.END)
                self.info_text.insert("1.0", f"Error: {str(e)}")
                self.update_status("Error occurred")
                
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()

    def on_closing(self):
        """Handle application closing"""
        try:
            # Stop device monitoring
            if hasattr(self, 'device_detector'):
                self.device_detector.stop_monitoring()
            
            # Save settings
            self.save_current_settings()
            
            # Force quit any background threads
            import os
            import sys
            
            # Destroy the window
            self.root.quit()
            self.root.destroy()
            
            # Force exit if needed
            os._exit(0)
            
        except Exception as e:
            print(f"Error during closing: {e}")
            import os
            os._exit(0)
        
    def save_current_settings(self):
        """Save current settings to config"""
        self.config.set("last_hex_file", self.hex_file_path.get())
        self.config.set("last_port", self.selected_port.get())
        self.config.set("last_pic_type", self.selected_pic_type.get())
        self.config.set("icsp_enabled", self.icsp_enabled.get())
        self.config.set("window_geometry", self.root.geometry())
        self.config.save()

def main():
    root = tk.Tk()
    app = PicProgrammerGUI(root)
    
    # Set application icon (if available)
    try:
        root.iconbitmap("icon.ico")
    except:
        pass  # Icon file not found, continue without it
        
    root.mainloop()

if __name__ == "__main__":
    main()
