#!/usr/bin/env python3
"""
Device detection and auto-connection for PyK150
"""

import serial
import serial.tools.list_ports
import threading
import time
import re

class DeviceDetector:
    def __init__(self):
        self.known_devices = {
            # Common VID:PID combinations for K150/K128/K149/K182 programmers
            "1A86:7523": "CH340 Serial (Common for K150)",
            "0403:6001": "FTDI Serial (Some K150 variants)",
            "10C4:EA60": "Silicon Labs CP210x (Some programmers)",
            "067B:2303": "Prolific PL2303 (Older programmers)"
        }
        
        self.detection_callbacks = []
        self.is_detecting = False
        
    def add_detection_callback(self, callback):
        """Add callback for device detection events"""
        self.detection_callbacks.append(callback)
        
    def notify_callbacks(self, event, data):
        """Notify all callbacks of detection events"""
        for callback in self.detection_callbacks:
            try:
                callback(event, data)
            except Exception:
                pass  # Ignore callback errors
                
    def get_all_ports(self):
        """Get all available serial ports"""
        return list(serial.tools.list_ports.comports())
        
    def detect_programmer_ports(self):
        """Detect potential programmer ports"""
        ports = self.get_all_ports()
        programmer_ports = []
        
        for port in ports:
            # Check by VID:PID
            vid_pid = f"{port.vid:04X}:{port.pid:04X}" if port.vid and port.pid else None
            if vid_pid and vid_pid in self.known_devices:
                programmer_ports.append({
                    'port': port.device,
                    'description': port.description,
                    'hwid': port.hwid,
                    'vid_pid': vid_pid,
                    'device_type': self.known_devices[vid_pid],
                    'confidence': 'high'
                })
                continue
                
            # Check by description patterns
            desc = port.description.lower()
            if any(keyword in desc for keyword in ['ch340', 'ch341', 'usb-serial', 'ftdi']):
                programmer_ports.append({
                    'port': port.device,
                    'description': port.description,
                    'hwid': port.hwid,
                    'vid_pid': vid_pid,
                    'device_type': 'Possible programmer device',
                    'confidence': 'medium'
                })
                
        return programmer_ports
        
    def test_programmer_connection(self, port, timeout=3):
        """Test if a port has a working programmer"""
        try:
            # Try to open the port
            with serial.Serial(port, 9600, timeout=1) as ser:
                # Send a simple test command (this would need to be adapted for actual protocol)
                # For now, just check if we can open the port
                return True
        except (serial.SerialException, OSError):
            return False
            
    def auto_detect_programmer(self, callback=None):
        """Automatically detect and test programmer"""
        def detect():
            self.is_detecting = True
            self.notify_callbacks('detection_started', None)
            
            try:
                # Get potential programmer ports
                programmer_ports = self.detect_programmer_ports()
                
                if not programmer_ports:
                    self.notify_callbacks('no_devices_found', None)
                    if callback:
                        callback(None, "No potential programmer devices found")
                    return
                
                # Test each port
                working_ports = []
                for port_info in programmer_ports:
                    self.notify_callbacks('testing_port', port_info)
                    
                    if self.test_programmer_connection(port_info['port']):
                        working_ports.append(port_info)
                        
                if working_ports:
                    # Sort by confidence (high confidence first)
                    working_ports.sort(key=lambda x: 0 if x['confidence'] == 'high' else 1)
                    best_port = working_ports[0]
                    
                    self.notify_callbacks('device_found', best_port)
                    if callback:
                        callback(best_port, None)
                else:
                    self.notify_callbacks('no_working_devices', programmer_ports)
                    if callback:
                        callback(None, "Found potential devices but none are responding")
                        
            except Exception as e:
                self.notify_callbacks('detection_error', str(e))
                if callback:
                    callback(None, f"Detection error: {str(e)}")
            finally:
                self.is_detecting = False
                self.notify_callbacks('detection_finished', None)
                
        # Run detection in separate thread
        thread = threading.Thread(target=detect)
        thread.daemon = True
        thread.start()
        
    def monitor_ports(self, callback):
        """Monitor for port changes"""
        self.port_change_callback = callback
        self.monitoring_active = True
        
        def monitor():
            last_ports = set()
            while self.monitoring_active:
                try:
                    current_ports = set(port.device for port in serial.tools.list_ports.comports())
                    
                    if current_ports != last_ports:
                        added = current_ports - last_ports
                        removed = last_ports - current_ports
                        
                        if added or removed:
                            if callback and self.monitoring_active:
                                callback(list(current_ports), list(added), list(removed))
                        
                        last_ports = current_ports
                    
                    time.sleep(2)  # Check every 2 seconds
                except Exception as e:
                    if self.monitoring_active:
                        print(f"Port monitoring error: {e}")
                    time.sleep(5)  # Wait longer on error
                    
        self.monitor_thread = threading.Thread(target=monitor)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
    def stop_monitoring(self):
        """Stop port monitoring"""
        self.monitoring_active = False
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread = None
