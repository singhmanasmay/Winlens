"""
Main Application Entry Point
Creates system tray icon and manages core functionality including:
- Hotkey listening
- Autostart management
- Configuration handling
- Single instance enforcement
"""
import keyboard
import threading
import pystray
from PIL import Image
import os
from tendo import singleton
import sys

import autorun
import config

config.backup = os.path.join(os.path.dirname(__file__),'config.json')
config.path = os.path.join(os.getenv('APPDATA'),'Winlens\\config.json')

def quit():
    """Force quit the application"""
    os.popen(f'taskkill /f /pid {os.getpid()}')

def start_search():
    """Start search function in a separate thread"""
    search_thread= threading.Thread(target=search)
    search_thread.start()

def search():
    """Launch search window if not already active"""
    if config.read(key='search_active')== False:
        # Launch search.exe using PowerShell to avoid console window
        os.popen(f'%SystemRoot%\\system32\\WindowsPowerShell\\v1.0\\powershell.exe Invoke-Item "{os.path.join(os.path.dirname(__file__),"search.pyw")}"')

def autostart():
    """Toggle autostart status in registry and config"""
    if autorun.exists('winlens')== True:
        autorun.remove('winlens')
        config.write(key='autostart',value=False)
    else:
        autorun.add('winlens',os.path.abspath(sys.argv[0]))
        config.write(key='autostart',value=True)

# Sync autostart status between registry and config
if autorun.exists('winlens')!= config.read(key='autostart'):
    autostart()

def gui():
    """Launch settings GUI"""
    os.popen(f'%SystemRoot%\\system32\\WindowsPowerShell\\v1.0\\powershell.exe Invoke-Item "{os.path.join(os.path.dirname(__file__),"gui.pyw")}"')

def github():
    """Open the GitHub repository in the default web browser"""
    os.popen('start https://github.com/singhmanasmay/Winlens')

# Ensure only one instance is running
try:
    me = singleton.SingleInstance()
except:
    quit()

# Reset search active flag on startup
config.write(key='search_active',value=False)

# Load tray icon image
image = Image.open(os.path.join(os.path.dirname(__file__),'icon.png'))

# Register global hotkey from config
keyboard.add_hotkey(config.read(key='shortcut'),start_search)

# Create and run system tray icon with menu
icon= pystray.Icon('winlens',icon=image,menu=pystray.Menu(
    pystray.MenuItem('',start_search,default=True,visible=False),  # Hidden default action
    pystray.MenuItem('Hotkey',pystray.Menu(
        pystray.MenuItem(config.read(key='shortcut'),quit,enabled=False),
        pystray.MenuItem('Modify',gui)
    )),
    pystray.MenuItem('Autostart',autostart,checked=lambda item: autorun.exists('winlens')),
    pystray.MenuItem('Github',github),
    pystray.MenuItem('Quit',quit)
    )).run()