import tkinter as tk
from pynput.mouse import Controller, Button
from pynput import keyboard
from threading import Thread
from time import sleep
from webbrowser import open

class Clicker(Thread):
    def __init__(self):
        super(Clicker, self).__init__()
        self.running = False
        self.program_running = True

    def exit_program(self):
        self.running = False
        self.program_running = False

    def run(self):
        while self.program_running:
            while self.running:
                mouse = Controller()
                mouse.click(Button.left)
                sleep(0.1)
            sleep(0.1)

class Shortcut(Thread):
    def __init__(self):
        super(Shortcut, self).__init__()
        self.binding = False
        self.listener = None

    def run(self):
        def on_press(key):
            if clicker_thread.program_running:
                global click_key
                if str(key) == str(click_key):
                    clicker_thread.running = not clicker_thread.running
                
                if str(key) == 'Key.page_down':
                    clicker_thread.exit_program()
                
                if self.binding:
                    click_key = key
                    self.binding = False
            return key

        self.listener = keyboard.Listener(on_press=on_press)
        self.listener.start()
        self.listener.join()

click_key = 'Key.page_up'
clicker_thread = Clicker()
clicker_thread.start()
shortcut_thread = Shortcut()
shortcut_thread.start()
windows = []

class NewWindow():
    def __init__(self, width, height, title):
        self.width = width
        self.height = height+100
        self.title = title
        self.window = tk.Tk()
        self.center_window()
        self.window.geometry(f'{self.width}x{self.height-100}+{self.x}+{self.y}')
        self.window.attributes('-topmost', True)
        self.window.title(title)
        windows.append(title)
        self.window.resizable(False, False)
        
    def center_window(self):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        self.x = (screen_width - self.width) // 2
        self.y = (screen_height - self.height) // 2
    
    def on_close(self):
        self.window.destroy()
        windows.remove(self.title)
        if self.title == 'AutoClicker':
            clicker_thread.running = False
            clicker_thread.program_running = False
            if shortcut_thread.listener != None:
                shortcut_thread.listener.stop()
        if shortcut_thread.binding:
            text.after_cancel(update)

def shortcut_setting():
    global win2
    global text
    global win2button
    if windows.count('Shortcut Setting') == 0:
        win2 = NewWindow(250, 100, 'Shortcut Setting')
        win2button = tk.Button(win2.window, text='Click / Stop', command=shortcut_changer, height=2)
        win2button.place(relx=0.25, rely=0.5, anchor='center', width=100)
        text = tk.Text(win2.window, height=2, font=8)
        text.tag_configure('tag_name', justify='center')
        text.insert(tk.END, str(click_key).replace("'", '').upper())
        text.tag_add('tag_name', '1.0', 'end')
        text.place(relx=0.75, rely=0.5, anchor='center', width=100)
        win2_close()

def shortcut_changer():
    win2.window.focus_set()
    shortcut_thread.binding = True
    update_text()
    win2button.config(state='disabled')

def update_text():
    global update
    button.config(text=f'Press {str(click_key).replace("'", '').upper()} to click')
    text.delete('1.0', tk.END)
    text.tag_configure('tag_name', justify='center')
    text.insert(tk.END, str(click_key).replace("'", '').upper())
    text.tag_add('tag_name', '1.0', 'end')
    update = text.after(500, update_text)
    if shortcut_thread.binding == False:
        text.after_cancel(update)
        win2button.config(state='normal')

def open_help():
    open('help.txt')

win = NewWindow(270, 130, 'AutoClicker')
button = tk.Button(win.window, text=f'Press {str(click_key).replace("'", '').upper()} to click', command=shortcut_setting)
button.place(relx=0.5, rely=0.35, anchor='center', height=40, width=240)
button2 = tk.Button(win.window, text='Help >>', command=open_help)
button2.place(relx=0.5, rely=0.75, anchor='center', height=40, width=240)
icon = tk.PhotoImage(file='icon.png')
win.window.iconphoto(True, icon)

def win2_close():
    win2.window.protocol('WM_DELETE_WINDOW', win2.on_close)

win.window.protocol('WM_DELETE_WINDOW', win.on_close)

win.window.mainloop()
