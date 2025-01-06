import tkinter as tk

root = tk.Tk()

def new_window():
    tp_lvl = tk.Toplevel(root)
    tp_lvl.title('teste')

tk.Button(root, text='new window', command=new_window).pack()

root.mainloop()

