"""
Hotkey Configuration GUI
Provides a user interface for configuring the application's keyboard shortcut.
Uses customtkinter for modern UI elements and matches Windows accent colors.
"""
import customtkinter as ctk
import keyboard
import winaccent
import threading
import config
import os

# Calculate a darker shade of Windows accent color for button hover state
dark_accent=list(winaccent.hex_to_rgb(winaccent.accent_normal))
dark_accent[0], dark_accent[1], dark_accent[2]= int(dark_accent[0]*0.6), int(dark_accent[1]*0.6), int(dark_accent[2]*0.6)
dark_accent= '#%02x%02x%02x' % tuple(dark_accent)
    
def key_trigger(x):
    """Validates and saves the entered hotkey"""
    if hotkey_valid(entry.get())== True:
        entry.configure(border_color= '#7CFC00')
        statuslabel.configure(text='saved',text_color='#7CFC00')
        config.config(key='shortcut',value=entry.get(),mode='w',path=os.path.join(os.getenv('APPDATA'),'Winlens\\config.json'))
    else:
        entry.configure(border_color= '#FF0000')
        statuslabel.configure(text='invalid hotkey',text_color='#FF0000')

def hotkey_valid(hotkey):
    """Tests if a hotkey combination is valid and available"""
    try:
        keyboard.add_hotkey(hotkey,lambda:0)
        keyboard.unhook_all()
        return True
    except:
        return False

def recording():
    """Records the next keyboard combination pressed"""
    recorded_hotkey= keyboard.read_hotkey()
    entry.insert(0, recorded_hotkey)
    key_trigger('x')
    recordbutton.configure(text='Record')
    keyboard.unhook_all()

def record():
    """Initiates hotkey recording process"""
    entry.delete(0, ctk.END)
    recordbutton.configure(text='Recording')
    entry.configure(border_color= '#0096FF')
    statuslabel.configure(text='waiting for input',text_color='#0096FF')
    recording_parent_thread= threading.Thread(target=recording)
    recording_parent_thread.isDaemon= True
    recording_parent_thread.start()

# Initialize main window
root= ctk.CTk()

# Configure window properties
width = 400
height = 65
root.geometry(f'{width}x{height}+{int((root.winfo_screenwidth()/2)-(width/2))}+{int((root.winfo_screenheight()/2)-(height/2))}')
root.configure(fg_color='black')
root.title('Winlens')
root.iconbitmap(os.path.join(os.path.dirname(__file__),'icon.ico'))
ctk.set_appearance_mode("dark")

# Create and configure UI elements
entryframe= ctk.CTkFrame(root, width=400, height=65, fg_color='black')
entryframe.place(x=0, y=0)

# Hotkey input field
entry= ctk.CTkEntry(entryframe, width=400, height=40, text_color=winaccent.accent_normal, 
                   placeholder_text_color=winaccent.accent_normal, 
                   placeholder_text=config.config(key='shortcut',mode='r',path=os.path.join(os.getenv('APPDATA'),'Winlens\\config.json')), 
                   fg_color='black', border_color=winaccent.accent_normal, 
                   font=('Segoe UI', 20), corner_radius=10)
entry.place(x=0,y=0)
entry.bind('<KeyRelease>',key_trigger)

# Record button
recordbutton = ctk.CTkButton(entryframe, text='Record', width=80, height=28, 
                            text_color='black', fg_color=winaccent.accent_normal, 
                            corner_radius=6, hover_color=dark_accent, 
                            font=('Segoe UI',14), command=record)
recordbutton.place(x=314, y=6)

# Status label
statuslabel=ctk.CTkLabel(entryframe, height=10,width=400, anchor='e',
                        padx=10,pady=0, font=('Segoe UI',16),text='')
statuslabel.place(x=0,y=40)

# Start the GUI event loop
root.mainloop()