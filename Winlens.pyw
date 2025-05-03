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
import shutil

import autorun
import config

# Create application data directory if it doesn't exist
if os.path.exists(os.path.join(os.getenv('APPDATA'),'Winlens'))== False:
    os.makedirs(os.path.join(os.getenv('APPDATA'),'Winlens'))

# Copy default config if it doesn't exist
if os.path.exists(os.path.join(os.getenv('APPDATA'),'Winlens\\config.json'))== False:
    shutil.copyfile(os.path.join(os.path.dirname(__file__),'config.json'), os.path.join(os.getenv('APPDATA'),'Winlens\\config.json'))

def quit():
    """Force quit the application"""
    os.popen(f'taskkill /f /pid {os.getpid()}')

def start_search():
    """Start search function in a separate thread"""
    search_thread= threading.Thread(target=search)
    search_thread.start()

def search():
    """Launch search window if not already active"""
    if config.config(key='search_active',mode='r',path=os.path.join(os.getenv('APPDATA'),'Winlens\\config.json'))== False:
        # Launch search.exe using PowerShell to avoid console window
        os.popen(f'%SystemRoot%\\system32\\WindowsPowerShell\\v1.0\\powershell.exe Invoke-Item "{os.path.join(os.path.dirname(__file__),"search.exe")}"')

def autostart():
    """Toggle autostart status in registry and config"""
    if autorun.exists('winlens')== True:
        autorun.remove('winlens')
        config.config(key='autostart',value=False,mode='w',path=os.path.join(os.getenv('APPDATA'),'Winlens\\config.json'))
    else:
        autorun.add('winlens',os.path.abspath(sys.argv[0]))
        config.config(key='autostart',value=True,mode='w',path=os.path.join(os.getenv('APPDATA'),'Winlens\\config.json'))

# Sync autostart status between registry and config
if autorun.exists('winlens')!= config.config(key='autostart',mode='r',path=os.path.join(os.getenv('APPDATA'),'Winlens\\config.json')):
    autostart()

def gui():
    """Launch settings GUI"""
    os.popen(f'%SystemRoot%\\system32\\WindowsPowerShell\\v1.0\\powershell.exe Invoke-Item "{os.path.join(os.path.dirname(__file__),"gui.exe")}"')

# Ensure only one instance is running
try:
    me = singleton.SingleInstance()
except:
    quit()

# Reset search active flag on startup
config.config(key='search_active',value=False,mode='w',path=os.path.join(os.getenv('APPDATA'),'Winlens\\config.json'))

# Load tray icon image
image = Image.open(os.path.join(os.path.dirname(__file__),'icon.png'))

# Register global hotkey from config
keyboard.add_hotkey(config.config(key='shortcut',mode='r',path=os.path.join(os.getenv('APPDATA'),'Winlens\\config.json')),start_search)

# Create and run system tray icon with menu
icon= pystray.Icon('winlens',icon=image,menu=pystray.Menu(
    pystray.MenuItem('',start_search,default=True,visible=False),  # Hidden default action
    pystray.MenuItem('Hotkey',pystray.Menu(
        pystray.MenuItem(config.config(key='shortcut',mode='r',path=os.path.join(os.getenv('APPDATA'),'Winlens\\config.json')),quit,enabled=False),
        pystray.MenuItem('Modify',gui)
    )),
    pystray.MenuItem('Autostart',autostart,checked=lambda item: autorun.exists('winlens')),
    pystray.MenuItem('Quit',quit)
    )).run()