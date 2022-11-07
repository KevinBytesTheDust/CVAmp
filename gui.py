import logging
import os
import sys
import threading
import tkinter as tk
import webbrowser
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

import psutil
import toml

from manager import InstanceManager
from utils import InstanceCommands

logger = logging.getLogger(__name__)


class InstanceBox(tk.Frame):
    def __init__(self, manager, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.instance_id = None
        self.manager = manager

        self.bind(
            "<Button-1>", lambda event: self.manager.queue_command(self.instance_id, InstanceCommands.REFRESH)
        )  # left clickk
        self.bind(
            "<Button-3>", lambda event: self.manager.queue_command(self.instance_id, InstanceCommands.EXIT)
        )  # right click
        self.bind(
            "<Control-1>", lambda event: self.manager.queue_command(self.instance_id, InstanceCommands.SCREENSHOT)
        )  # control left click

    def modify(self, status, instance_id):
        self.instance_id = instance_id
        color_codes = {
            "inactive": "SystemButtonFace",
            "alive": "grey",
            "init": "yellow",
            "watching": "#44d209",
        }

        color = color_codes[status]
        self.configure(background=color)


class GUI:
    def __init__(self, manager: InstanceManager):
        self.manager = manager
        self.queue_counter = 0
        self.root = tk.Tk()
        self.instances_boxes = []

        self.headless = tk.BooleanVar(value=manager.get_headless())
        self.auto_restart = tk.BooleanVar(value=manager.get_auto_restart())

    def spawn_one_func(self):
        print("Spawning one instance. Please wait for alive & watching instances increase.")
        target_url = self.root.nametowidget("channel_url_entry").get()
        threading.Thread(target=self.manager.spawn_instance, args=(target_url,)).start()

    def spawn_three_func(self):
        print("Spawning three instances. Please wait for alive & watching instances increase.")
        target_url = self.root.nametowidget("channel_url_entry").get()
        threading.Thread(target=self.manager.spawn_instances, args=(3, target_url)).start()

    def delete_one_func(self):
        print("Destroying one instance. Please wait for alive & watching instances decrease.")
        threading.Thread(target=self.manager.delete_latest).start()

    def delete_all_func(self):
        print("Destroying all instances. Please wait for alive & watching instances decrease.")
        threading.Thread(target=self.manager.delete_all_instances).start()

    def run(self):

        root = self.root
        root.geometry("600x305+500+500")

        # Pyinstaller fix to find file, when using --onefile and --add-data
        path_to_cwd = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))
        path_to_icon = os.path.abspath(os.path.join(path_to_cwd, "ctvb_logo.ico"))
        root.iconbitmap(path_to_icon)

        path_to_toml = os.path.abspath(os.path.join(path_to_cwd, "pyproject.toml"))
        version = toml.load(path_to_toml)["tool"]["poetry"]["version"]

        root.title(f"Crude twitch viewer bot | v{version} | jlplenio")

        # separators
        separator_left = ttk.Separator(orient="vertical")
        separator_left.place(x=170, relx=0, rely=0, relwidth=0.2, relheight=0.5)
        separator_right = ttk.Separator(orient="vertical")
        separator_right.place(x=-170, relx=1, rely=0, relwidth=0.2, relheight=0.5)

        # left
        proxy_available_text = tk.Label(root, text="Proxies Available", borderwidth=2)
        proxy_available_text.place(x=40, y=10)
        proxy_available = tk.Label(root, text="0", borderwidth=2, relief="solid", width=5)
        proxy_available.place(x=70, y=40)

        lbl_buy = tk.Label(root, text="(buy more)", fg="blue", cursor="hand2")
        lbl_buy.bind(
            "<Button-1>",
            lambda event: webbrowser.open("https://www.webshare.io/?referral_code=w6nfvip4qp3g"),
        )
        lbl_buy.place(x=58, y=62)

        headless_checkbox = ttk.Checkbutton(
            root,
            text="headless",
            variable=self.headless,
            command=lambda: self.manager.set_headless(self.headless.get()),
            onvalue=True,
            offvalue=False,
        )
        headless_checkbox.place(x=200, y=94)

        auto_restart_checkbox = ttk.Checkbutton(
            root,
            variable=self.auto_restart,
            text="auto restart",
            command=lambda: self.manager.set_auto_restart(self.auto_restart.get()),
            onvalue=True,
            offvalue=False,
        )
        auto_restart_checkbox.place(x=320, y=94)

        # right
        instances_text = tk.Label(root, text="Instances", borderwidth=2)
        instances_text.place(x=455, y=10)

        alive_instances_text = tk.Label(root, text="alive", borderwidth=2)
        alive_instances_text.place(x=455, y=40)
        watching_instances_text = tk.Label(root, text="watching", borderwidth=2)
        watching_instances_text.place(x=455, y=60)

        alive_instances = tk.Label(root, text=0, borderwidth=2, relief="solid", width=5)
        alive_instances.place(x=530, y=40)
        watching_instances = tk.Label(root, text=0, borderwidth=2, relief="solid", width=5)
        watching_instances.place(x=530, y=60)

        cpu_usage_text = tk.Label(root, text="CPU", borderwidth=2)
        cpu_usage_text.place(x=440, y=88)
        ram_usage_text = tk.Label(root, text="RAM", borderwidth=2)
        ram_usage_text.place(x=510, y=88)

        # mid log
        channel_url = tk.Entry(root, width=40, name="channel_url_entry")
        channel_url.place(x=180, y=10)
        channel_url.insert(0, "https://www.twitch.tv/channel_name")

        spawn_one = tk.Button(
            root,
            width=15,
            anchor="w",
            text="Spawn 1 instance",
            command=lambda: self.spawn_one_func(),
        )
        spawn_one.place(x=180, y=35)
        spawn_three = tk.Button(
            root,
            width=15,
            anchor="w",
            text="Spawn 3 instances",
            command=lambda: self.spawn_three_func(),
        )
        spawn_three.place(x=180, y=65)
        destroy_one = tk.Button(
            root,
            width=15,
            anchor="w",
            text="Destroy 1 instance",
            command=lambda: self.delete_one_func(),
        )
        destroy_one.place(x=305, y=35)
        destroy_all = tk.Button(
            root,
            width=15,
            anchor="w",
            text="Destroy all instances",
            command=lambda: self.delete_all_func(),
        )
        destroy_all.place(x=305, y=65)

        # mid text box
        text_area = ScrolledText(root, height="7", width="92", font=("regular", 8))
        text_area.place(
            x=20,
            y=120,
        )

        id_counter = 1
        for row in range(5):
            for col in range(50):
                box = InstanceBox(
                    self.manager,
                    self.root,
                    background="SystemButtonFace",
                    bd=0.5,
                    relief="raised",
                    width=10,
                    height=10,
                )
                box.place(x=24 + col * 11, y=230 + row * 12)
                self.instances_boxes.append(box)
                id_counter += 1

        # bottom
        lbl = tk.Label(
            root,
            text=r"https://github.com/jlplenio/crude-twitch-viewer-bot",
            fg="blue",
            cursor="hand2",
        )
        lbl.bind("<Button-1>", lambda event: webbrowser.open(lbl.cget("text")))
        lbl.place(x=150, y=288)

        # refresh counters
        def refresher():

            instances_overview = self.manager.get_instances_overview()

            proxy_available.configure(text=len(self.manager.proxies.proxy_list))

            for (id, status), box in zip(instances_overview.items(), self.instances_boxes):
                box.modify(status, id)

            for index in range(len(instances_overview), len(self.instances_boxes)):
                self.instances_boxes[index].modify("inactive", None)

            alive_instances.configure(text=self.manager.get_active_count())
            watching_count = len([1 for id, status in instances_overview.items() if status == "watching"])
            watching_instances.configure(text=str(watching_count))
            cpu_usage_text.configure(text=" {:.2f}% CPU".format(psutil.cpu_percent()))
            ram_usage_text.configure(text=" {:.2f}% RAM".format(psutil.virtual_memory().percent))
            root.after(1000, refresher)  # every x milliseconds...

        refresher()

        # redirect stdout
        def redirector(str_input):

            if self.root:
                text_area.configure(state='normal')
                text_area.insert(tk.INSERT, str_input)
                text_area.see(tk.END)
                text_area.configure(state='disabled')
            else:
                sys.stdout = sys.__stdout__

        sys.stdout.write = redirector

        root.resizable(False, False)
        root.mainloop()
