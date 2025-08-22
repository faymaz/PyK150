#!/usr/bin/env python3
"""
Translation system for PyK150
"""

# Translation dictionary
TRANSLATIONS = {
    "en": {
        # Main window
        "title": "PyK150 - PIC Programmer GUI",
        "programming": "Programming",
        "dump_read": "Dump/Read",
        "chip_info": "Chip Info",
        "ready": "Ready",
        
        # Connection settings
        "connection_settings": "Connection Settings",
        "serial_port": "Serial Port:",
        "refresh": "Refresh",
        "pic_type": "PIC Type:",
        
        # File selection
        "file_selection": "File Selection",
        "hex_file": "HEX File:",
        "browse": "Browse",
        "output_file": "Output File:",
        
        # Options
        "options": "Options",
        "enable_icsp": "Enable ICSP",
        "binary_format": "Binary format",
        "fuse_settings": "Fuse Settings:",
        "fuse_format": "# Format: FUSE_NAME:FUSE_VALUE (one per line)\n# Example: CONFIG1:0x3F4A",
        
        # Operations
        "operations": "Operations",
        "program": "Program",
        "verify": "Verify",
        "erase": "Erase",
        "dump_memory": "Dump Memory",
        
        # Memory types
        "memory_type": "Memory Type",
        "rom": "ROM",
        "eeprom": "EEPROM",
        "config": "CONFIG",
        
        # Info
        "chip_information": "Chip Information",
        "get_chip_info": "Get Chip Info",
        "get_hex_info": "Get HEX Info",
        "connection_info": "Connection Info",
        "uses_connection": "Uses connection settings from Programming tab",
        
        # Output
        "output_log": "Output Log",
        
        # Messages
        "error": "Error",
        "success": "Success",
        "warning": "Warning",
        "select_port": "Please select a serial port",
        "select_pic": "Please select a PIC type",
        "select_hex": "Please select a HEX file",
        "hex_file_too_large": "HEX file is too large for selected chip",
        "specify_output": "Please specify an output file",
        "operation_completed": "Operation completed successfully!",
        "operation_failed": "Operation failed!",
        "operation_timeout": "Operation timed out",
        "picpro_not_found": "picpro command not found.\nPlease install picpro first:\npip install picpro",
        
        # Menu
        "file": "File",
        "edit": "Edit",
        "tools": "Tools",
        "help": "Help",
        "open": "Open",
        "save": "Save",
        "exit": "Exit",
        "preferences": "Preferences",
        "about": "About",
        "user_manual": "User Manual",
        
        # Device detection
        "detecting_devices": "Detecting devices...",
        "device_found": "Device found",
        "no_device_found": "No compatible device found",
        "auto_connect": "Auto Connect",
        
        # Recent files
        "recent_files": "Recent Files",
        "clear_recent": "Clear Recent Files",
        
        # Picpro settings
        "picpro_path": "Picpro Path:",
        "browse_picpro": "Browse for picpro",
        "auto_find_picpro": "Auto-find picpro executable",
        "test_picpro": "Test",
        "picpro_valid": "Picpro executable is valid",
        "picpro_invalid": "Invalid picpro executable",
        "picpro_not_set": "Picpro path not set",
        "programming": "Programming",
        "dump_read": "Dump/Read",
        "chip_info": "Chip Info",
        "ready": "Ready",
        
        # Connection settings
        "connection_settings": "Connection Settings",
        "serial_port": "Serial Port:",
        "refresh": "Refresh",
        "pic_type": "PIC Type:",
        
        # File selection
        "file_selection": "File Selection",
        "hex_file": "HEX File:",
        "browse": "Browse",
        "output_file": "Output File:",
        
        # Options
        "options": "Options",
        "enable_icsp": "Enable ICSP",
        "binary_format": "Binary format",
        "fuse_settings": "Fuse Settings:",
        "fuse_format": "# Format: FUSE_NAME:FUSE_VALUE (one per line)\n# Example: CONFIG1:0x3F4A",
        
        # Operations
        "operations": "Operations",
        "program": "Program",
        "verify": "Verify",
        "erase": "Erase",
        "dump_memory": "Dump Memory",
        
        # Memory types
        "memory_type": "Memory Type",
        "rom": "ROM",
        "eeprom": "EEPROM",
        "config": "CONFIG",
        
        # Info
        "chip_information": "Chip Information",
        "get_chip_info": "Get Chip Info",
        "get_hex_info": "Get HEX Info",
        "connection_info": "Connection Info",
        "uses_connection": "Uses connection settings from Programming tab",
        
        # Output
        "output_log": "Output Log",
        
        # Messages
        "error": "Error",
        "success": "Success",
        "warning": "Warning",
        "select_port": "Please select a serial port",
        "select_pic": "Please select a PIC type",
        "select_hex": "Please select a HEX file",
        "hex_file_too_large": "HEX file is too large for selected chip",
        "specify_output": "Please specify an output file",
        "operation_completed": "Operation completed successfully!",
        "operation_failed": "Operation failed!",
        "operation_timeout": "Operation timed out",
        "picpro_not_found": "picpro command not found.\nPlease install picpro first:\npip install picpro",
        
        # Menu
        "file": "File",
        "edit": "Edit",
        "tools": "Tools",
        "help": "Help",
        "open": "Open",
        "save": "Save",
        "exit": "Exit",
        "preferences": "Preferences",
        "about": "About",
        "user_manual": "User Manual",
        
        # Device detection
        "detecting_devices": "Detecting devices...",
        "device_found": "Device found",
        "no_device_found": "No compatible device found",
        "auto_connect": "Auto Connect",
        
        # Recent files
        "recent_files": "Recent Files",
        "clear_recent": "Clear Recent Files",
        
        # Picpro settings
        "picpro_path": "Picpro Path:",
        "browse_picpro": "Browse for picpro",
        "auto_find_picpro": "Auto-find picpro executable",
        "test_picpro": "Test",
        "picpro_valid": "Picpro executable is valid",
        "picpro_invalid": "Invalid picpro executable",
        "picpro_not_set": "Picpro path not set",
        
        # Menu items
        "file": "File",
        "open": "Open",
        "exit": "Exit",
        "tools": "Tools",
        "preferences": "Preferences",
        "help": "Help",
        "about": "About",
        "user_manual": "User Manual",
        
        # Tabs
        "programming_tab": "Programming",
        "dump_tab": "Dump/Read",
        "info_tab": "Chip Info",
        
        # Info tab
        "connection_info": "Connection Info",
        "chip_information": "Chip Information",
        
        # Recent files
        "recent_files": "Recent Files",
        "clear_recent": "Clear Recent",
        "no_recent_files": "No recent files",
        
        # Device detection
        "device_connected": "Device connected",
        "device_disconnected": "Device disconnected",
        "auto_detection": "Auto Detection",
        "detecting_device": "Detecting device...",
        "device_found": "Device found",
        "no_device_found": "No device found",
        
        # Preferences dialog
        "language": "Language",
        "auto_detect_programmer": "Auto-detect programmer",
        "save_window_position": "Save window position",
        "show_tooltips": "Show tooltips",
        "apply": "Apply",
        "cancel": "Cancel",
        "ok": "OK",
        
        # Picpro configuration
        "picpro_config": "Picpro Configuration",
        "picpro_path": "Picpro Path",
        "auto_find_picpro": "Auto-find picpro",
        "browse_picpro": "Browse picpro",
        "test_picpro": "Test picpro",
        "picpro_status": "Picpro Status",
        "picpro_valid": "Picpro valid",
        "picpro_invalid": "Picpro invalid",
        "picpro_not_found": "Picpro not found",
        "picpro_test_success": "Picpro test successful",
        "picpro_test_failed": "Picpro test failed",
        
        # Version warnings
        "version_warning_title": "Picpro Version Warning",
        "version_too_old": "Picpro version too old",
        "minimum_version_required": "Minimum version 0.3.0 required",
        
        # Chip placement guide
        "chip_placement_guide": "Chip Placement Guide",
        "select_chip_for_guide": "Select a chip to see placement guide",
        "place_chip_pin1": "Place {chip} with Pin 1 at top-left corner",
        "chip_guide_not_available": "Chip guide for {chip} not available",
        "zif_socket": "K150 ZIF Socket",
        "pin_1": "Pin 1",
        "placement_instructions": "Placement Instructions:",
        "open_zif_lever": "1. Open ZIF socket lever",
        "insert_chip_notch": "2. Insert chip with notch at top",
        "pin1_top_left": "3. Pin 1 goes to top-left",
        "close_lever": "4. Close lever to secure chip"
    },
    "de": {
        # Main window
        "title": "PyK150 - PIC Programmierer",
        "connection_settings": "Verbindungseinstellungen",
        "serial_port": "Serielle Schnittstelle",
        "pic_type": "PIC Typ",
        "refresh": "Aktualisieren",
        "auto_connect": "Automatisch verbinden",
        
        # File operations
        "file_selection": "Dateiauswahl",
        "hex_file": "HEX Datei",
        "browse": "Durchsuchen",
        "output_file": "Ausgabedatei",
        
        # Operations
        "operations": "Operationen",
        "program": "Programmieren",
        "verify": "Verifizieren",
        "erase": "Löschen",
        "dump_memory": "Speicher auslesen",
        "get_chip_info": "Chip-Info abrufen",
        
        # Options
        "options": "Optionen",
        "icsp_enabled": "ICSP aktiviert",
        "binary_format": "Binärformat",
        "enable_icsp": "ICSP aktivieren",
        "fuse_settings": "Fuse-Einstellungen",
        "fuse_format": "# Format: FUSE_NAME:FUSE_WERT (eine pro Zeile)\n# Beispiel: CONFIG1:0x3F4A",
        
        # Memory types
        "memory_type": "Speichertyp",
        "rom": "ROM",
        "eeprom": "EEPROM",
        "config": "CONFIG",
        
        # Status and messages
        "status": "Status",
        "ready": "Bereit",
        "programming": "Programmiere...",
        "verifying": "Verifiziere...",
        "erasing": "Lösche...",
        "dumping": "Lese aus...",
        "success": "Erfolgreich",
        "error": "Fehler",
        "failed": "Fehlgeschlagen",
        
        # Dialogs
        "select_hex": "Bitte wählen Sie eine HEX-Datei",
        "select_pic": "Bitte wählen Sie einen PIC-Typ",
        "select_port": "Bitte wählen Sie eine serielle Schnittstelle",
        "select_output": "Bitte wählen Sie eine Ausgabedatei",
        "file_not_found": "Datei nicht gefunden",
        "operation_completed": "Operation abgeschlossen",
        "operation_failed": "Operation fehlgeschlagen",
        
        # Menu items
        "file": "Datei",
        "open": "Öffnen",
        "exit": "Beenden",
        "tools": "Werkzeuge",
        "preferences": "Einstellungen",
        "help": "Hilfe",
        "about": "Über",
        "user_manual": "Benutzerhandbuch",
        
        # Tabs
        "programming_tab": "Programmierung",
        "dump_tab": "Auslesen/Backup",
        "info_tab": "Chip-Info",
        
        # Info tab
        "connection_info": "Verbindungsinfo",
        "chip_information": "Chip-Informationen",
        
        # Recent files
        "recent_files": "Zuletzt verwendete Dateien",
        "clear_recent": "Verlauf löschen",
        "no_recent_files": "Keine zuletzt verwendeten Dateien",
        
        # Device detection
        "device_connected": "Gerät verbunden",
        "device_disconnected": "Gerät getrennt",
        "auto_detection": "Automatische Erkennung",
        "detecting_device": "Erkenne Gerät...",
        "device_found": "Gerät gefunden",
        "no_device_found": "Kein Gerät gefunden",
        
        # Preferences dialog
        "language": "Sprache",
        "auto_detect_programmer": "Programmierer automatisch erkennen",
        "save_window_position": "Fensterposition speichern",
        "show_tooltips": "Tooltips anzeigen",
        "apply": "Anwenden",
        "cancel": "Abbrechen",
        "ok": "OK",
        
        # Picpro configuration
        "picpro_config": "Picpro Konfiguration",
        "picpro_path": "Picpro Pfad",
        "auto_find_picpro": "Picpro automatisch finden",
        "browse_picpro": "Picpro durchsuchen",
        "test_picpro": "Picpro testen",
        "picpro_status": "Picpro Status",
        "picpro_valid": "Picpro gültig",
        "picpro_invalid": "Picpro ungültig",
        "picpro_not_found": "Picpro nicht gefunden",
        "picpro_test_success": "Picpro Test erfolgreich",
        "picpro_test_failed": "Picpro Test fehlgeschlagen",
        
        # Version warnings
        "version_warning_title": "Picpro Versions-Warnung",
        "version_too_old": "Picpro Version zu alt",
        "minimum_version_required": "Mindestversion 0.3.0 erforderlich",
        
        # Main window
        "title": "PyK150 - PIC Programmierer",
        "connection_settings": "Verbindungseinstellungen",
        "serial_port": "Serielle Schnittstelle",
        "pic_type": "PIC Typ",
        "refresh": "Aktualisieren",
        "auto_connect": "Automatisch verbinden",
        
        # File operations
        "file_selection": "Dateiauswahl",
        "hex_file": "HEX Datei",
        "browse": "Durchsuchen",
        "output_file": "Ausgabedatei",
        
        # Operations
        "operations": "Operationen",
        "program": "Programmieren",
        "verify": "Verifizieren",
        "erase": "Löschen",
        "dump_memory": "Speicher auslesen",
        "get_chip_info": "Chip-Info abrufen",
        
        # Options
        "options": "Optionen",
        "icsp_enabled": "ICSP aktiviert",
        "binary_format": "Binärformat",
        "enable_icsp": "ICSP aktivieren",
        "fuse_settings": "Fuse-Einstellungen",
        "fuse_format": "# Format: FUSE_NAME:FUSE_WERT (eine pro Zeile)\n# Beispiel: CONFIG1:0x3F4A",
        
        # Memory types
        "memory_type": "Speichertyp",
        "rom": "ROM",
        "eeprom": "EEPROM",
        "config": "CONFIG",
        
        # Status and messages
        "status": "Status",
        "ready": "Bereit",
        "programming": "Programmiere...",
        "verifying": "Verifiziere...",
        "erasing": "Lösche...",
        "dumping": "Lese aus...",
        "success": "Erfolgreich",
        "error": "Fehler",
        "failed": "Fehlgeschlagen",
        
        # Dialogs
        "select_hex": "Bitte wählen Sie eine HEX-Datei",
        "select_pic": "Bitte wählen Sie einen PIC-Typ",
        "select_port": "Bitte wählen Sie eine serielle Schnittstelle",
        "select_output": "Bitte wählen Sie eine Ausgabedatei",
        "file_not_found": "Datei nicht gefunden",
        "operation_completed": "Operation abgeschlossen",
        "operation_failed": "Operation fehlgeschlagen",
        
        # Menu items
        "file": "Datei",
        "open": "Öffnen",
        "exit": "Beenden",
        "tools": "Werkzeuge",
        "preferences": "Einstellungen",
        "help": "Hilfe",
        "about": "Über",
        "user_manual": "Benutzerhandbuch",
        
        # Tabs
        "programming_tab": "Programmierung",
        "dump_tab": "Auslesen/Backup",
        "info_tab": "Chip-Info",
        
        # Info tab
        "connection_info": "Verbindungsinfo",
        "chip_information": "Chip-Informationen",
        
        # Recent files
        "recent_files": "Zuletzt verwendete Dateien",
        "clear_recent": "Verlauf löschen",
        "no_recent_files": "Keine zuletzt verwendeten Dateien",
        
        # Device detection
        "device_connected": "Gerät verbunden",
        "device_disconnected": "Gerät getrennt",
        "auto_detection": "Automatische Erkennung",
        "detecting_device": "Erkenne Gerät...",
        "device_found": "Gerät gefunden",
        "no_device_found": "Kein Gerät gefunden",
        
        # Preferences dialog
        "language": "Sprache",
        "auto_detect_programmer": "Programmierer automatisch erkennen",
        "save_window_position": "Fensterposition speichern",
        "show_tooltips": "Tooltips anzeigen",
        "apply": "Anwenden",
        "cancel": "Abbrechen",
        "ok": "OK",
        
        # Picpro configuration
        "picpro_config": "Picpro Konfiguration",
        "picpro_path": "Picpro Pfad",
        "auto_find_picpro": "Picpro automatisch finden",
        "browse_picpro": "Picpro durchsuchen",
        "test_picpro": "Picpro testen",
        "picpro_status": "Picpro Status",
        "picpro_valid": "Picpro gültig",
        "picpro_invalid": "Picpro ungültig",
        "picpro_not_found": "Picpro nicht gefunden",
        "picpro_test_success": "Picpro Test erfolgreich",
        "picpro_test_failed": "Picpro Test fehlgeschlagen",
        
        # Version warnings
        "version_warning_title": "Picpro Versions-Warnung",
        "version_too_old": "Picpro Version zu alt",
        "minimum_version_required": "Mindestversion 0.3.0 erforderlich",
        "operation_failed": "Operation failed"
    },
    "tr": {
        # Ana pencere
        "title": "PyK150 - PIC Programlayıcı GUI",
        "programming": "Programlama",
        "dump_read": "Okuma/Yedekleme",
        "chip_info": "Çip Bilgisi",
        "ready": "Hazır",
        
        # Bağlantı ayarları
        "connection_settings": "Bağlantı Ayarları",
        "serial_port": "Seri Port:",
        "refresh": "Yenile",
        "pic_type": "PIC Türü:",
        
        # Dosya seçimi
        "file_selection": "Dosya Seçimi",
        "hex_file": "HEX Dosyası:",
        "browse": "Gözat",
        "output_file": "Çıktı Dosyası:",
        
        # Seçenekler
        "options": "Seçenekler",
        "operations": "İşlemler",
        "program": "Programla",
        "verify": "Doğrula",
        "erase": "Sil",
        "dump_memory": "Belleği Oku",
        "get_chip_info": "Chip Bilgisi Al",
        
        # Options
        "options": "Seçenekler",
        "icsp_enabled": "ICSP Etkin",
        "binary_format": "Binary Format",
        "enable_icsp": "ICSP Etkinleştir",
        "fuse_settings": "Fuse Ayarları",
        "fuse_format": "# Format: FUSE_ADI:FUSE_DEGERI (her satırda bir)\n# Örnek: CONFIG1:0x3F4A",
        
        # Memory types
        "memory_type": "Bellek Türü",
        "rom": "ROM",
        "eeprom": "EEPROM",
        "config": "CONFIG",
        
        # Status and messages
        "status": "Durum",
        "ready": "Hazır",
        "programming": "Programlanıyor...",
        "verifying": "Doğrulanıyor...",
        "erasing": "Siliniyor...",
        "dumping": "Okunuyor...",
        "success": "Başarılı",
        "error": "Hata",
        "failed": "Başarısız",
        
        # Dialogs
        "select_hex": "Lütfen bir HEX dosyası seçin",
        "select_pic": "Lütfen bir PIC türü seçin",
        "select_port": "Lütfen bir seri port seçin",
        "select_output": "Lütfen çıktı dosyası seçin",
        "file_not_found": "Dosya bulunamadı",
        "operation_completed": "İşlem tamamlandı",
        "operation_failed": "İşlem başarısız",
        
        # Menu items
        "file": "Dosya",
        "open": "Aç",
        "exit": "Çıkış",
        "tools": "Araçlar",
        "preferences": "Tercihler",
        "help": "Yardım",
        "about": "Hakkında",
        "user_manual": "Kullanım Kılavuzu",
        
        # Tabs
        "programming_tab": "Programlama",
        "dump_tab": "Okuma/Yedekleme",
        "info_tab": "Chip Bilgisi",
        
        # Info tab
        "connection_info": "Bağlantı Bilgisi",
        "chip_information": "Chip Bilgileri",
        
        # Recent files
        "recent_files": "Son Dosyalar",
        "clear_recent": "Son Dosyaları Temizle",
        "no_recent_files": "Son dosya yok",
        
        # Device detection
        "device_connected": "Cihaz bağlandı",
        "device_disconnected": "Cihaz bağlantısı kesildi",
        "auto_detection": "Otomatik Algılama",
        "detecting_device": "Cihaz algılanıyor...",
        "device_found": "Cihaz bulundu",
        "no_device_found": "Cihaz bulunamadı",
        
        # Preferences dialog
        "language": "Dil",
        "auto_detect_programmer": "Programcıyı Otomatik Algıla",
        "save_window_position": "Pencere Konumunu Kaydet",
        "show_tooltips": "İpuçlarını Göster",
        "apply": "Uygula",
        "cancel": "İptal",
        "ok": "Tamam",
        
        # Picpro configuration
        "picpro_config": "Picpro Yapılandırması",
        "picpro_path": "Picpro Yolu",

        # Ana pencere
        "title": "PyK150 - PIC Programlayıcı Arayüzü",
        "programming": "Programlama",
        "dump_read": "Okuma/Yedekleme",
        "chip_info": "Çip Bilgisi",
        "ready": "Hazır",
        
        # Bağlantı ayarları
        "connection_settings": "Bağlantı Ayarları",
        "serial_port": "Seri Port:",
        "refresh": "Yenile",
        "pic_type": "PIC Türü:",
        
        # Dosya seçimi
        "file_selection": "Dosya Seçimi",
        "hex_file": "HEX Dosyası:",
        "browse": "Gözat",
        "output_file": "Çıktı Dosyası:",
        
        # Seçenekler
        "options": "Seçenekler",
        "operations": "İşlemler",
        "program": "Programla",
        "verify": "Doğrula",
        "erase": "Sil",
        "dump_memory": "Belleği Oku",
        "get_chip_info": "Chip Bilgisi Al",
        
        # Options
        "options": "Seçenekler",
        "icsp_enabled": "ICSP Etkin",
        "binary_format": "Binary Format",
        "enable_icsp": "ICSP Etkinleştir",
        "fuse_settings": "Fuse Ayarları",
        "fuse_format": "# Format: FUSE_ADI:FUSE_DEGERI (her satırda bir)\n# Örnek: CONFIG1:0x3F4A",
        
        # Memory types
        "memory_type": "Bellek Türü",
        "rom": "ROM",
        "eeprom": "EEPROM",
        "config": "CONFIG",
        
        # Status and messages
        "status": "Durum",
        "ready": "Hazır",
        "programming": "Programlanıyor...",
        "verifying": "Doğrulanıyor...",
        "erasing": "Siliniyor...",
        "dumping": "Okunuyor...",
        "success": "Başarılı",
        "error": "Hata",
        "failed": "Başarısız",
        
        # Dialogs
        "select_hex": "Lütfen bir HEX dosyası seçin",
        "select_pic": "Lütfen bir PIC türü seçin",
        "select_port": "Lütfen bir seri port seçin",
        "select_output": "Lütfen çıktı dosyası seçin",
        "file_not_found": "Dosya bulunamadı",
        "operation_completed": "İşlem tamamlandı",
        "operation_failed": "İşlem başarısız",
        
        # Menu items
        "file": "Dosya",
        "open": "Aç",
        "exit": "Çıkış",
        "tools": "Araçlar",
        "preferences": "Tercihler",
        "help": "Yardım",
        "about": "Hakkında",
        "user_manual": "Kullanım Kılavuzu",
        
        # Tabs
        "programming_tab": "Programlama",
        "dump_tab": "Okuma/Yedekleme",
        "info_tab": "Chip Bilgisi",
        
        # Info tab
        "connection_info": "Bağlantı Bilgisi",
        "chip_information": "Chip Bilgileri",
        
        # Recent files
        "recent_files": "Son Dosyalar",
        "clear_recent": "Son Dosyaları Temizle",
        "no_recent_files": "Son dosya yok",
        
        # Device detection
        "device_connected": "Cihaz bağlandı",
        "device_disconnected": "Cihaz bağlantısı kesildi",
        "auto_detection": "Otomatik Algılama",
        "detecting_device": "Cihaz algılanıyor...",
        "device_found": "Cihaz bulundu",
        "no_device_found": "Cihaz bulunamadı",
        
        # Preferences dialog
        "language": "Dil",
        "auto_detect_programmer": "Programcıyı Otomatik Algıla",
        "save_window_position": "Pencere Konumunu Kaydet",
        "show_tooltips": "İpuçlarını Göster",
        "apply": "Uygula",
        "cancel": "İptal",
        "ok": "Tamam",
        
        # Picpro configuration
        "picpro_config": "Picpro Yapılandırması",
        "picpro_path": "Picpro Yolu",
        "auto_find_picpro": "Picpro'yu Otomatik Bul",
        "browse_picpro": "Picpro'ya Gözat",
        "test_picpro": "Test Et",
        "picpro_status": "Picpro Durumu",
        "picpro_valid": "Picpro geçerli",
        "picpro_invalid": "Geçersiz picpro",
        "picpro_not_found": "Picpro bulunamadı",
        "picpro_test_success": "Picpro testi başarılı",
        "picpro_test_failed": "Picpro testi başarısız",
        "version_warning_title": "Picpro Sürüm Uyarısı",
        "version_too_old": "Picpro sürümü çok eski",
        "minimum_version_required": "En az sürüm 0.3.0 gerekli"
    }
}

class Translations:
    def __init__(self):
        self.translations = TRANSLATIONS
        self.current_language = "en"
    
    def set_language(self, language):
        """Set current language"""
        if language in self.translations:
            self.current_language = language
    
    def get(self, key, default=None):
        """Get translated text"""
        return self.translations.get(self.current_language, {}).get(key, default or key)
    
    def __call__(self, key, default=None):
        """Allow direct calling: tr("key")"""
        return self.get(key, default)