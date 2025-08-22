# PyK150 v1.0.0-beta - PIC Programmer GUI

A modern cross-platform GUI for programming PIC microcontrollers using K150 compatible programmers.

## Features

- **Visual Chip Placement Guide**: Interactive guide showing proper chip orientation
- **HEX File Size Validation**: Prevents programming oversized files
- **Multi-language Support**: English, Turkish, German
- **Auto Device Detection**: Automatic K150 programmer detection
- **Complete PIC Database**: 198+ supported PIC microcontrollers
- **ICSP Programming**: In-Circuit Serial Programming support
- **Real-time Logging**: Detailed operation feedback

## Supported Programmers

- **K150** - Fully tested and supported
- **K128/K149/K182** - Compatible models
- Requires picpro 0.3.0+ backend

## Installation

```bash
pip install -r requirements.txt
python3 install.py
```

## Usage

```bash
./run.sh
```

1. Connect K150 programmer
2. Select PIC type
3. Load HEX file
4. Click Program

## Requirements

- Python 3.6+
- picpro 0.3.0+
- pyserial

## License

MIT License
