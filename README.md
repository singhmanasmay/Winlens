# Winlens

A lightweight Windows utility that brings Google Lens to your desktop with a single hotkey. Instantly capture any part of your screen and search it with Google Lens.

## Features

- 🔍 Instant screen capture and Google search
- ⌨️ Customizable global hotkey
- 🎯 System tray integration
- 🚀 Auto-start capability

## Installation

1. Download the latest release from the releases page
3. Run the downloaded file `Winlens.exe`

Or run from source:

1. Clone this repository
2. Install dependencies:
```
pip install -r requirements.txt
```
3. Run `Winlens.pyw`

## Requirements

- Windows 10 1507 and above
- Python 3.x (if running from source)
- Required Python packages (if running from source):
  - customtkinter (installed automatically with pip)
  - keyboard (installed automatically with pip)
  - pillow (installed automatically with pip)
  - pystray (installed automatically with pip)
  - pywebview (installed automatically with pip)
  - screeninfo (installed automatically with pip)
  - tendo (installed automatically with pip)
  - winaccent (installed automatically with pip)

## Usage

1. Launch Winlens - it will appear in your system tray
2. Press `Windows + C` (default hotkey) or click the tray icon to capture and search
3. The captured area will automatically open in Google Lens
4. To change the hotkey: 
  - right-click the tray icon and select Hotkey > Modify
  - input a custom hotkey in the feild or record one from your keyboard
  - restart the application for the new hotkey to take effect
5. To toggle autostart, right-click the tray icon and select Autostart

## Config file

Settings are stored in `%APPDATA%\Winlens\config.json`:

- `autostart`: Enable/disable start with Windows
- `shortcut`: Global hotkey combination
- `search_active`: Internal state tracking (do not touch)


## License

[MIT License](LICENSE)
