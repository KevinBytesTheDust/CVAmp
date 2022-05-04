# Crude twitch viewer bot
[![](https://img.shields.io/github/downloads/jlplenio/crude-twitch-viewer-bot/v0.1.0/total)](https://github.com/jlplenio/crude-twitch-viewer-bot/releases/latest)

Disclaimer: For educational purpose only!

Small tool that spawns muted Google Chrome instances via [Playwright](https://github.com/microsoft/playwright-python), each with a different user-agent and HTTP proxy connection. 
Each instance navigates to the twitch channel, activates theater mode and adheres itself to the available screen space. 
Settings in localStorage ensure the lowest possible resolution.

Download the one-file executable for Windows from the [latest CTVB release](https://github.com/jlplenio/crude-twitch-viewer-bot/releases/latest).

### Important
- You need to provide HTTP proxies to [proxy_list.txt](proxy/proxy_list.txt)  
  Buy some at [webshare.io (referred)](https://www.webshare.io/?referral_code=w6nfvip4qp3g), download txt and put in [proxy_list.txt](proxy/proxy_list.txt). 
- Tested with instance count: Headless ~100, headful ~30.
- Tested on Windows 10.
- CPU load and bandwidth can get heavy. Channels with 160p work best.



### In action

GUI  
![](docs/gui.png)
 
Headful spawning
(If you go headless, the browser windows will be invisible)  
![](docs/instances_spawning.gif)

### Usage

#### Executable for windows

Download the one-file executable for Windows from the [latest CTVB release](https://github.com/jlplenio/crude-twitch-viewer-bot/releases/latest).

#### Script version

```
GUI: main_gui.py
```
```
REPL: main.py

Start in REPL and interact with manager through command examples below

Spawn a single instance or multiple with threading:
manager.spawn_instance()
manager.spawn_instances(5)

Delete a single instance or all with threading:
manager.delete_latest()
manager.delete_all_instances()
```


