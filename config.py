"""
Configuration Manager
Handles reading and writing to the config.json file that stores application settings.
"""
import json
import os
import shutil

backup = ''
path = ''

def create(backup,path):
    """
    Create a new config.json file from the backup if it doesn't exist.
    
    Args:
        backup (str): Path to the backup config.json file
        path (str): Path to the new config.json file
    """
    shutil.copy2(backup, path)
        

def read(key):
    """
    Read a value from the config.json file.
    """
    global read
    try:
        with open(path,'r') as config:
            return json.loads(config.read())[key]
    except:
        create(backup, path)
        return read(key)
    
def write(key, value):
    """
    Write a value to the config.json file.
    """
    global write
    try:
        with open(path,'r') as config:
            dict= json.loads(config.read())
            dict[key]= value
        with open(path,'w') as config:
            config.write(json.dumps(dict, indent=4))
    except:
        create(backup, path)
        write(key, value)
