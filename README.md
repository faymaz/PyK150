# PyK150 - PIC Programmer GUI

A modern, feature-rich graphical user interface for programming PIC microcontrollers using K150/K128/K149/K182 programmers.

## Features

- **Modern GUI**: Clean, intuitive interface built with tkinter
- **Serial Port Detection**: Automatic detection and selection of available ports
- **Comprehensive PIC Support**: Complete database of PIC microcontrollers from official chipdata
- **Smart Chip Selection**: Search and filter functionality for easy chip selection
- **Family-based Organization**: Chips organized by families (PIC10F, PIC12F, PIC16F, PIC18F, etc.)
- **File Management**: Easy HEX file selection with file dialogs
- **Programming Operations**: Program, verify, erase, and dump operations
- **ICSP Support**: In-Circuit Serial Programming capability
- **Progress Tracking**: Real-time progress indicators and logging
- **Multi-language Support**: English, Turkish, and German language options
- **Device Auto-detection**: Automatic detection of K150/K128/K149/K182 programmers
- **Configuration Management**: Persistent settings and preferences
- **Help System**: Built-in user manual and troubleshooting guide
- **Recent Files** - Quick access to recently used HEX files
- **Progress Tracking** - Real-time progress indicators and status updates
- **Enhanced Error Handling** - Comprehensive error detection and recovery
- **Port Monitoring** - Automatic detection of device connections/disconnections

## Supported Programmers
- **Modern UI** - Clean, intuitive interface with toolbar and status bar
- **Keyboard Shortcuts** - Ctrl+O (Open), Ctrl+Q (Quit)
- **Comprehensive Help** - Built-in user manual and troubleshooting guide
- **Preferences Dialog** - Customizable settings and options

## 🔧 Supported Programmers

- **K128** - Basic PIC programmer
- **K149** (versions A to F) - Enhanced programmer  
- **K150** (Tested) - Most common, fully supported
- **K182** - Advanced programmer

**Note:** Programmer must have latest firmware with P18A protocol support.

## 📦 Installation

### Quick Install
```bash
python3 install.py
```

### Manual Install
```bash
pip install -r requirements.txt
pip install picpro
```

## 🚀 Usage

### Launch Application
```bash
python3 pyk150_gui.py
# or
./run.sh
```

### Basic Workflow
1. **Connect Hardware** - Plug in your K150 programmer
2. **Auto-Detect** - Click "Auto Connect" or use toolbar button
3. **Select PIC Type** - Choose your microcontroller model
4. **Load HEX File** - Browse or use recent files menu
5. **Program** - Click "Program" button and wait for completion
6. **Verify** - Always verify programming success

### Advanced Features
- **Language Switch** - Use toolbar dropdown or Tools menu
- **Preferences** - Configure auto-detection and other settings
- **Help System** - Access comprehensive user manual
- **Recent Files** - Quick access to previously used files

## 📁 Project Structure

```
PyK150/
├── pyk150_gui.py      # Main GUI application
├── config.py          # Configuration management
├── translations.py    # Multi-language support
├── device_detector.py # Auto device detection
├── help_system.py     # Built-in help system
├── install.py         # Installation script
├── run.sh            # Launch script
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## 🔧 Requirements

- **Python 3.6+** - Core runtime
- **tkinter** - GUI framework (usually included)
- **pyserial** - Serial communication
- **picpro** - PIC programming backend

## 🌍 Language Support

- **English** - Full interface translation
- **Türkçe** - Complete Turkish localization

Switch languages via:
- Toolbar dropdown
- Tools → Language menu
- Preferences dialog

## 🛠️ Configuration

Settings are automatically saved to `~/.pyk150/config.json`:

- Last used port and PIC type
- Window geometry and position
- Language preference
- Recent files list
- Auto-detection settings

## 🆘 Troubleshooting

### Common Issues

**"No serial ports found"**
- Check USB connection
- Install programmer drivers
- Try different USB port

**"picpro command not found"**
- Run: `pip install picpro`
- Check Python PATH

**"Programming failed"**
- Verify chip orientation
- Check chip type selection
- Try erasing chip first

**Permission denied (Linux)**
- Add user to dialout group: `sudo usermod -a -G dialout $USER`
- Log out and back in

### Getting Help
- Built-in help: Help → User Manual
- Check output log for error details
- Enable auto-detection for device issues

## 📄 License

MIT License - Free and open source

## 🙏 Credits

- Based on **picpro** by Salamek
- GUI developed for enhanced usability
- Inspired by the original PicPro projects
