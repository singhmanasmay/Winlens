"""
Windows Registry Autostart Manager
Handles adding/removing the application from Windows startup via registry.
"""
import winreg

# Connect to current user's registry
_registry= winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)

def get_runonce():
    """Opens the Windows Run registry key with full access"""
    return winreg.OpenKey(_registry,r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0,winreg.KEY_ALL_ACCESS)

def add(name, application):
    """Add application to Windows autostart
    Args:
        name (str): Registry key name
        application (str): Full path to executable
    """
    key= get_runonce()
    try:
        winreg.SetValueEx(key, name, 0, winreg.REG_SZ, application)
    except WindowsError as e:
        print(e)
    winreg.CloseKey(key)

def exists(name):
    """Check if application exists in autostart
    Args:
        name (str): Registry key name to check
    Returns:
        bool: True if exists, False otherwise
    """
    key= get_runonce()
    exists= True
    try:
        winreg.QueryValueEx(key, name)
    except WindowsError:
        exists= False
    winreg.CloseKey(key)
    return exists

def remove(name):
    """Remove application from autostart if it exists
    Args:
        name (str): Registry key name to remove
    """
    if exists(name):
        key= get_runonce()
        winreg.DeleteValue(key, name)
        winreg.CloseKey(key)


#add('winlens',r'C:\Users\Manasmay\Desktop\winlens\basic\test0.py')
#print(exists('winlens'))
#remove('winlens')
