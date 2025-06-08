"""
Screen Capture and Search Window
Handles screen capture, Google Lens integration, and web view display.

Flow:
1. Takes a screenshot using Windows+PrintScreen
2. Creates a maximized webview window with Google Lens
3. Automatically pastes the screenshot when loaded
4. Manages search state to prevent multiple instances
"""
import webview
import keyboard
from screeninfo import get_monitors
import time
import os

import config

config.backup = os.path.join(os.path.dirname(__file__), 'config.json')
config.path = os.path.join(os.getenv('APPDATA'), 'Winlens\\config.json')

# Get primary monitor resolution for proper window sizing
for monitor in get_monitors():
    if monitor.is_primary== True:
        resx, resy = monitor.width, monitor.height

def paste():
    """Paste captured screenshot into Google Lens
    Called when webview window is fully loaded"""
    global resx,resy
    window.show()
    keyboard.send('ctrl+v')  # Paste screenshot from clipboard

# Set search active flag to prevent multiple instances
config.write(key='search_active',value=True)

# Capture screenshot using Windows + PrintScreen
keyboard.send('win+print screen')
time.sleep(0.1)  # Brief delay to ensure screenshot is captured

# Create maximized webview window with Google Lens
window=webview.create_window('Winlens', 'https://www.google.com/?olud',maximized=True) 
window.events.loaded += paste  # Register paste event when window loads
webview.start() 

# Reset search active flag when window closes
config.write(key='search_active',value=False)