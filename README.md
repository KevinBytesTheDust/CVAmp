# Crude Twitch Viewer Bot (CTVBot)
[![](https://img.shields.io/github/downloads/jlplenio/crude-twitch-viewer-bot/total)](https://github.com/jlplenio/crude-twitch-viewer-bot/releases/latest)
[![](https://github.com/jlplenio/crude-twitch-viewer-bot/actions/workflows/pytest.yml/badge.svg)](https://github.com/jlplenio/crude-twitch-viewer-bot/actions/workflows/pytest.yml)
[![format & lint](https://github.com/jlplenio/crude-twitch-viewer-bot/actions/workflows/format_lint.yml/badge.svg)](https://github.com/jlplenio/crude-twitch-viewer-bot/actions/workflows/format_lint.yml)
[![](https://github.com/jlplenio/crude-twitch-viewer-bot/actions/workflows/build.yml/badge.svg)](https://github.com/jlplenio/crude-twitch-viewer-bot/actions/workflows/build.yml)

>Disclaimer: For educational purpose only. Any discussion of illegal use will be deleted immediately!
### Getting Started
Download the one-file executable for Windows, Linux and MacOS from the [latest CTVBot release](https://github.com/jlplenio/crude-twitch-viewer-bot/releases/latest).  
Read the comprehensive [wiki](https://github.com/jlplenio/crude-twitch-viewer-bot/wiki) for a [detailed tutorial](https://github.com/jlplenio/crude-twitch-viewer-bot/wiki/Detailed-Tutorial), [usage tips](https://github.com/jlplenio/crude-twitch-viewer-bot/wiki/Advanced-features-and-controls) and [troubleshooting steps](https://github.com/jlplenio/crude-twitch-viewer-bot/wiki/Troubleshooting).

[:coffee: You can sponsor me a coffee](https://ko-fi.com/jlplenio) if you enjoy this tool and want to support its continued development. 

### Mandatory Requirements
- You need to provide your own private HTTP proxies to the [proxy_list.txt](proxy/proxy_list.txt)  
  Buy trusted proxies [here](https://www.webshare.io/?referral_code=w6nfvip4qp3g) or follow the [Webshare.io Proxies Guide](https://github.com/jlplenio/crude-twitch-viewer-bot/wiki/Webshare.io-Proxies-Guide).
- Chrome needs to be already installed on your system.

### Platform Support Overview

| Platform              |       Twitch       |      Youtube       |   Kick    |
|-----------------------|:------------------:|:------------------:|:---------:|
| General Functionality | :heavy_check_mark: | :heavy_check_mark: | :warning: |
| Lowest Quality Select | :heavy_check_mark: | :heavy_check_mark: |    :x:    |
| Status Boxes Updates  | :heavy_check_mark: | :heavy_check_mark: |    :x:    |
| Login/Authentication  |    :hourglass:     |        :x:         |    :x:    |

:heavy_check_mark: Supported, :warning: Problems/Instability, :x: Unsupported, :hourglass: In Development 

### In Action

![](docs/gui.png)

#### Controls and Color codes of the square boxes

⬛ - Instance is spawned.    🟨 - Instance is buffering.    🟩 - Instance is actively watching.

🖱️ Left click: Refresh page.
🖱️ Right click: Destroy instance.
🖱️ Left click + CTRL: Take screenshot.

### Misc
- CPU load and bandwidth can get heavy. Channels with 160p work best.
- Tested on Windows 10 with headless ~100, headful ~30. Linux and macOS is experimental.

The Crude Twitch Viewer Bot (CTVBot) is a small GUI tool that spawns muted Google Chrome instances via [Playwright](https://github.com/microsoft/playwright-python), each with a different user-agent and HTTP proxy connection. Each instance navigates to the streaming channel and selects the lowest possible resolution.

Read the comprehensive [wiki](https://github.com/jlplenio/crude-twitch-viewer-bot/wiki) for a [detailed tutorial](https://github.com/jlplenio/crude-twitch-viewer-bot/wiki/Detailed-Tutorial), [usage tips](https://github.com/jlplenio/crude-twitch-viewer-bot/wiki/Advanced-features-and-controls) and [troubleshooting steps](https://github.com/jlplenio/crude-twitch-viewer-bot/wiki/Troubleshooting).





