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
        self.queue_counter = 0
        self.root = tk.Tk()
        self.headless = tk.BooleanVar(value=True)
        self.change_headmode()

    def spawn_one_func(self):
        print("Spawning one instance. Please wait for alive & working instances increase.")
        target_url = self.root.children['!entry'].get()
        threading.Thread(target=self.manager.spawn_instance, args=(target_url,)).start()

    def spawn_three_func(self):
        print("Spawning three instances. Please wait for alive & working instances increase.")
        target_url = self.root.children['!entry'].get()
        threading.Thread(target=self.manager.spawn_instances, args=(3, target_url)).start()

    def delete_one_func(self):
        print("Destroying one instance. Please wait for alive & working instances decrease.")
        threading.Thread(target=self.manager.delete_latest).start()

    def delete_all_func(self):
        print("Destroying all instances. Please wait for alive & working instances decrease.")
        threading.Thread(target=self.manager.delete_all_instances).start()

    def change_headmode(self):
        self.manager.set_headless(self.headless.get())

    def run(self):

        root = self.root
        root.geometry("600x305+500+500")
        root.title('Crude twitch viewer bot - jlplenio')

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

        #checkbox
        headless_checkbox = ttk.Checkbutton(root, text='headless', command=self.change_headmode, variable=self.headless, onvalue=True, offvalue=False)
        headless_checkbox.place(x=55, y=90)

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
        instances_text = tk.Label(root, text="Instances", borderwidth=2)
        instances_text.place(x=470, y=10)

        alive_instances_text = tk.Label(root, text="alive", borderwidth=2)
        alive_instances_text.place(x=470, y=40)
        watching_instances_text = tk.Label(root, text="working", borderwidth=2)
        watching_instances_text.place(x=470, y=60)

        alive_instances = tk.Label(root, text=0, borderwidth=2, relief="solid", width=5)
        alive_instances.place(x=530, y=40)
        watching_instances = tk.Label(root, text=0, borderwidth=2, relief="solid", width=5)
        watching_instances.place(x=530, y=60)

        cpu_usage_text = tk.Label(root, text="CPU Usage", borderwidth=2)
        cpu_usage_text.place(x=460, y=85)
        ram_usage_text = tk.Label(root, text="RAM Usage", borderwidth=2)
        ram_usage_text.place(x=465, y=105)

        # text box
        text_area = ScrolledText(root, height='10', width='92', font=('regular', 8))
        text_area.place(x=20, y=140)

        # bottom
        lbl = tk.Label(root, text=r"https://github.com/jlplenio/crude-twitch-viewer-bot", fg="blue", cursor="hand2")
        lbl.bind("<Button-1>", lambda event: webbrowser.open(lbl.cget("text")))
        lbl.place(x=150, y=288)

        # refresh counters
        def refresher():
            proxy_available.configure(text=len(self.manager.proxies.proxy_list))
            alive_instances.configure(text=self.manager.get_active_count())
            watching_instances.configure(text=self.manager.get_fully_initialized_count())
            cpu_usage_text.configure(text="   {:.2f}% CPU Usage".format(psutil.cpu_percent()))
            ram_usage_text.configure(text=" {:.2f}% RAM Usage".format(psutil.virtual_memory().percent))
            root.after(2000, refresher)  # every x milliseconds...

        refresher()

        # # redirect stdout
        # def redirector(str_input):
        #     text_area.insert(tk.INSERT, str_input)
        #     text_area.see(tk.END)

        #sys.stdout.write = redirector

        root.resizable(False, False)
        root.mainloop()
