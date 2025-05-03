"""
Configuration Manager
Handles reading and writing to the config.json file that stores application settings.
"""
import json
import os

def config(**kwargs):
    """
    Read or write configuration values from/to config.json
    
    Args:
        path (str): Path to config.json file
        mode (str): 'r' for read, 'w' for write
        key (str): Configuration key to access
        value (any): Value to write (only for write mode)
        
    Returns:
        any: Configuration value when reading
    """
    file= os.path.join(os.path.dirname(__file__),kwargs['path'])

    if kwargs['mode']=='r':
        with open(file,'r') as config:
            return json.loads(config.read())[kwargs['key']]   
    elif kwargs['mode']=='w':
        with open(file,'r') as config:
            dict= json.loads(config.read())
            dict[kwargs['key']]= kwargs['value']
        with open(file,'w') as config:
            config.write(json.dumps(dict, indent=4))