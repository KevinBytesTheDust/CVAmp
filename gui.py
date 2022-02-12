import sys
import threading
import tkinter as tk
import webbrowser
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

import psutil

from spawner import BrowserManager


class GUI:

    def __init__(self, manager: BrowserManager):
        self.manager = manager
        self.root = None

    def spawn_one_func(self):
        print("Spawning one instance. Please wait for active instances increase.")
        target_url = self.root.children['!entry'].get()
        threading.Thread(target=self.manager.spawn_instance, args=(target_url,)).start()

    def spawn_three_func(self):
        print("Spawning three instances. Please wait for active instances increase.")
        target_url = self.root.children['!entry'].get()
        threading.Thread(target=self.manager.spawn_instances, args=(3, target_url)).start()

    def delete_one_func(self):
        print("Destroying one instance. Please wait for active instances decrease.")
        threading.Thread(target=self.manager.delete_latest).start()

    def delete_all_func(self):
        print("Destroying all instances. Please wait for active instances decrease.")
        threading.Thread(target=self.manager.delete_all_instances).start()

    def run(self):
        root = tk.Tk()
        self.root = root
        root.geometry("600x305")
        root.title('Crude twitch viewer bot with selenium - jlplenio')

        # separators
        separator_left = ttk.Separator(orient='vertical')
        separator_left.place(x=170, relx=0, rely=0, relwidth=0.2, relheight=1)
        separator_right = ttk.Separator(orient='vertical')
        separator_right.place(x=-170, relx=1, rely=0, relwidth=0.2, relheight=1)

        # left
        proxy_available_text = tk.Label(root, text="Proxies Available", borderwidth=2)
        proxy_available_text.place(x=40, y=10)
        proxy_available = tk.Label(root, text="0", borderwidth=2, relief="solid", width=5)
        proxy_available.place(x=70, y=40)
        # proxy_reload = tk.Button(root, width=15, anchor="n", text='Reload Proxylist', command=lambda: Sleeper.sleepx(5))
        # proxy_reload.place(x=30, y=80)

        # mid
        channel_url = tk.Entry(root, width=40)
        channel_url.place(x=180, y=10)
        channel_url.insert(0, "https://www.twitch.tv/channel_name")

        spawn_one = tk.Button(root, width=15, anchor="w", text='Spawn 1 instance', command=lambda: self.spawn_one_func())
        spawn_one.place(x=180, y=50)
        spawn_three = tk.Button(root, width=15, anchor="w", text='Spawn 3 instances', command=lambda: self.spawn_three_func())
        spawn_three.place(x=180, y=100)
        destroy_one = tk.Button(root, width=15, anchor="w", text='Destroy 1 instance', command=lambda: self.delete_one_func())
        destroy_one.place(x=305, y=50)
        destroy_all = tk.Button(root, width=15, anchor="w", text='Destroy all instances', command=lambda: self.delete_all_func())
        destroy_all.place(x=305, y=100)

        # right
        live_instances_text = tk.Label(root, text="Active Instances", borderwidth=2)
        live_instances_text.place(x=470, y=10)

        cpu_usage_text = tk.Label(root, text="CPU Usage", borderwidth=2)
        cpu_usage_text.place(x=460, y=82)
        ram_usage_text = tk.Label(root, text="RAM Usage", borderwidth=2)
        ram_usage_text.place(x=460, y=100)

        live_instances = tk.Label(root, text=0, borderwidth=2, relief="solid", width=5)
        live_instances.place(x=500, y=40)

        # text box
        text_area = ScrolledText(root, height='10', width='92', font=('regular', 8))
        text_area.place(x=20, y=140)

        # bottom
        lbl = tk.Label(root, text=r"https://github.com/jlplenio/twitch-viewer-bot-selenium", fg="blue", cursor="hand2")
        lbl.bind("<Button-1>", lambda event: webbrowser.open(lbl.cget("text")))
        lbl.place(x=150, y=288)

        # refresh counters
        def refresher():
            proxy_available.configure(text=len(self.manager.proxies.proxy_list))
            live_instances.configure(text=len(self.manager.browser_instances))
            cpu_usage_text.configure(text="   {:.2f}% CPU Usage".format(psutil.cpu_percent()))
            ram_usage_text.configure(text=" {:.2f}% RAM Usage".format(psutil.virtual_memory().percent))
            root.after(500, refresher)  # every 0.5 second...

        refresher()

        # redirect stdout
        def redirector(str_input):
            text_area.insert(tk.INSERT, str_input)
            text_area.see(tk.END)

        sys.stdout.write = redirector

        root.resizable(False, False)
        root.mainloop()