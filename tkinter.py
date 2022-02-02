import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

root = tk.Tk()
root.geometry("800x300")
root.title('Tkinter place Geometry Manager')

# screenshot from session
def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()


button = tk.Button(root, text='Okay', command=lambda: popupmsg("wowzer"))
button.place(x=20, y=10)

text = ScrolledText(root, height='8', width='95')

text.place(x=10, y=150)

root.resizable(False, False)
root.mainloop()
