import tkinter as tk
import tkinter.ttk as ttk
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
                if delay >= 1:
                    for c in range(int(delay)):
                        sleep(1)
                        if not self.running:
                            break
                    if delay != int(delay):
                        remain_delay = delay - int(delay)
                        remain_delay = str(f'{remain_delay:.3f}')
                        sleep(float(remain_delay))
                else:
                    sleep(delay)
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
                if self.binding:
                    click_key = key
                    self.binding = False
                else:
                    if str(key) == str(click_key):
                        clicker_thread.running = not clicker_thread.running
            return key

        self.listener = keyboard.Listener(on_press=on_press)
        self.listener.start()
        self.listener.join()

click_key = 'Key.page_up'
milisec = 100
sec = 0
min = 0
hour = 0
delay = 0.1
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
        self.window = tk.Toplevel(root)
        self.window.focus_set()
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
        global yspacer
        yspacer = 0
        root.focus_set()
        self.window.destroy()
        windows.remove(self.title)
        if self.title == 'AutoClicker':
            clicker_thread.running = False
            clicker_thread.program_running = False
            if shortcut_thread.listener != None:
                shortcut_thread.listener.stop()
        if self.title == 'Shortcut Setting':
            if shortcut_thread.binding:
                shortcut_thread.binding = False
                text.after_cancel(update)

class NewMenu():
    def __init__(self, title:str, x:float, y:float):
        self.menubutton = ttk.Menubutton(menu_frame, text=title, style="Toolbutton")
        self.menubutton.place(relx=x, rely=y)
        self.menu = tk.Menu(self.menubutton, tearoff=False)
        self.menubutton.config(menu=self.menu)

    def new_command(self, title:str, function):
        self.menu.add_command(label=title, command=function)

def on_main_close():
    root.destroy()
    clicker_thread.running = False
    clicker_thread.program_running = False
    if shortcut_thread.listener != None:
        shortcut_thread.listener.stop()
    if shortcut_thread.binding:
        text.after_cancel(update)

def center_window():
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 270) // 2
    y = (screen_height - 240) // 2
    root.geometry(f'270x140+{x}+{y}')

def shortcut_setting():
    global win2
    global text
    global win2button
    root.focus_set()
    if windows.count('Shortcut Setting') == 0:
        win2 = NewWindow(250, 100, 'Shortcut Setting')
        win2button = ttk.Button(win2.window, text='Click / Stop', command=shortcut_changer)
        win2button.place(relx=0.25, rely=0.5, anchor='center', width=100, height=42)
        text = tk.Text(win2.window, font=8)
        text.tag_configure('tag_name', justify='center')
        text.insert(tk.END, str(click_key).replace("'", '').upper())
        text.tag_add('tag_name', '1.0', 'end')
        text.place(relx=0.75, rely=0.5, anchor='center', width=100, height=40)
        win2_close()

def shortcut_changer():
    win2.window.focus_set()
    clicker_thread.running = False
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

def callback(input):
    if input.isdigit():
        return True
                          
    elif input == '':
        return True
  
    else: 
        return False

yspacer = 0
def new_entry(root, start_value, labeltext, y, x):
    global yspacer
    yspacer += 0.05
    y += yspacer
    reg = root.register(callback) 
    entry = tk.Entry(root, width=4, justify='right', validate='key', validatecommand=(reg, '%P'))
    entry.insert(0, start_value)
    entry.place(relx=0.82, rely=y)
    label = tk.Label(root, text=labeltext)
    label.place(relx=x, rely=y-0.02)
    return entry

def interval():
    global interval_win
    if windows.count('Interval Config') == 0:
        interval_win = NewWindow(270, 120, 'Interval Config')
        milisecs = new_entry(interval_win.window, milisec, 'miliseconds', 0.1, 0.54)
        secs = new_entry(interval_win.window, sec, 'seconds', 0.25, 0.597)
        mins = new_entry(interval_win.window, min, 'minutes', 0.4, 0.597)
        hours = new_entry(interval_win.window, hour, 'hours', 0.55, 0.637)
        interval_confirm_button = ttk.Button(interval_win.window, text='Save Changes', command=lambda: interval_change(milisecs.get(), secs.get(), mins.get(), hours.get()))
        interval_confirm_button.place(relx=0.1, rely=0.15, width=100, height=40)
        restore_default_button = ttk.Button(interval_win.window, text='Default Settings')
        restore_default_button.place(relx=0.1, rely=0.55, width=100, height=40)
        interval_win_close()

def interval_change(milisecs, secs, mins, hours):
    global milisec, sec, min, hour, delay
    interval_win.window.focus_set()
    clicker_thread.running = False
    if not milisecs.isdigit():
        milisecs = 0
    milisecs = int(milisecs)
    if not secs.isdigit():
        secs = 0
    secs = int(secs)
    if not mins.isdigit():
        mins = 0
    mins = int(mins)
    if not hours.isdigit():
        hours = 0
    hours = int(hours)

    milisec = milisecs
    sec = secs
    min = mins
    hour = hours
    delay = milisecs / 1000
    delay += secs
    delay += mins * 60
    delay += hours * 3600

def open_help():
    root.focus_set()
    open('help.txt')

root = tk.Tk()
root.attributes('-topmost', True)
root.title("DNI Auto Clicker")
root.resizable(False, False)
center_window()

c = 0
menu_style = ttk.Style()
menu_style.configure('Toolbutton', background='white')
menu_frame = tk.Frame(root, background='white')
menu_frame.place(relx=0, rely=0, height=24, width=270)
file_menu = NewMenu('File', 0.02, 0)
config_menu = NewMenu('Config', 0.13, 0)
config_menu.new_command('Interval', interval)
help_menu = NewMenu('Help', 0.31, 0)
help_menu.new_command('Help', open_help)

button = ttk.Button(root, text=f'Press {str(click_key).replace("'", '').upper()} to click', command=shortcut_setting)
button.place(relx=0.5, rely=0.4, anchor='center', height=40, width=240)

button2 = ttk.Button(root, text='Help >>', command=open_help)
button2.place(relx=0.5, rely=0.75, anchor='center', height=40, width=240)

root.protocol('WM_DELETE_WINDOW', on_main_close)
def win2_close():
    win2.window.protocol('WM_DELETE_WINDOW', win2.on_close)
def interval_win_close():
    interval_win.window.protocol('WM_DELETE_WINDOW', interval_win.on_close)

root.mainloop()
