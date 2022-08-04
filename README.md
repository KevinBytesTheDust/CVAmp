# Crude twitch viewer bot
[![](https://img.shields.io/github/downloads/jlplenio/crude-twitch-viewer-bot/total)](https://github.com/jlplenio/crude-twitch-viewer-bot/releases/latest)
[![](https://github.com/jlplenio/crude-twitch-viewer-bot/actions/workflows/pytest.yml/badge.svg)](https://github.com/jlplenio/crude-twitch-viewer-bot/actions/workflows/pytest.yml)
[![](https://github.com/jlplenio/crude-twitch-viewer-bot/actions/workflows/build.yml/badge.svg)](https://github.com/jlplenio/crude-twitch-viewer-bot/actions/workflows/build.yml)

Disclaimer: For educational purpose only!

Small tool that spawns muted Google Chrome instances via [Playwright](https://github.com/microsoft/playwright-python), each with a different user-agent and HTTP proxy connection. 
Each instance navigates to the twitch channel, activates theater mode and adheres itself to the available screen space. 
Settings in localStorage ensure the lowest possible resolution.

Download the one-file executable for Windows from the [latest CTVB release](https://github.com/jlplenio/crude-twitch-viewer-bot/releases/latest).

### Important
- You need to provide HTTP proxies to [proxy_list.txt](proxy/proxy_list.txt)  
  Buy some at [webshare.io (referred)](https://www.webshare.io/?referral_code=w6nfvip4qp3g), download txt and put in [proxy_list.txt](proxy/proxy_list.txt).
- Chrome needs to be already installed on your system.
- Tested with instance count: Headless ~100, headful ~30.
- Tested on Windows 10.
- CPU load and bandwidth can get heavy. Channels with 160p work best.

### In action

![](docs/gui.png)

#### Color codes of the square boxes

⬛ - Instance is spawned.  
🟨 - Instance is buffering.  
🟩 - Instance is actively watching.
 
#### Headful spawning
![](docs/instances_spawning.gif)  
(If you go headless, the browser windows will be invisible)  


### Usage Windows
#### Steps
Download the one-file executable for Windows from the [latest CTVB release](https://github.com/jlplenio/crude-twitch-viewer-bot/releases/latest).

1. Extract zip file to a folder.
2. Add own proxies or buy some at [webshare.io (referred)](https://www.webshare.io/?referral_code=w6nfvip4qp3g) to proxy/proxy_list.txt.
3. Start executable and wait for GUI.
4. Spawn instances patiently.

#### Interactions with the square boxes
🖱️ Left click: Refresh page.  
🖱️ Right click: Destroy instance.  
🖱️ Left click + CTRL: Take screenshot (saved in root folder).   




