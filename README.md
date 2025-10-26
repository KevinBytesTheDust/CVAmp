# Crude Viewer Amplifier (CVAmp)

[![](https://img.shields.io/github/downloads/kevinbytesthedust/cvamp/total)](https://github.com/KevinBytesTheDust/cvamp/releases/latest)
[![](https://github.com/KevinBytesTheDust/cvamp/actions/workflows/pytest.yml/badge.svg)](https://github.com/KevinBytesTheDust/cvamp/actions/workflows/pytest.yml)
[![](https://github.com/KevinBytesTheDust/cvamp/actions/workflows/format_lint.yml/badge.svg)](https://github.com/KevinBytesTheDust/cvamp/actions/workflows/format_lint.yml)
[![](https://github.com/KevinBytesTheDust/cvamp/actions/workflows/build.yml/badge.svg)](https://github.com/KevinBytesTheDust/cvamp/actions/workflows/build.yml)

![grafik](https://github.com/user-attachments/assets/66110d35-1683-4f95-a48f-a737c5dcedd0)

> Disclaimer: For educational purpose only. Any discussion of illegal use will be deleted immediately!  
> Full disclaimer below.

### Getting Started

1. Download the one-file executable for Windows, Linux and MacOS from the [latest CVAmp release](https://github.com/KevinBytesTheDust/cvamp/releases/latest).
2. Provide your proxies or follow our comprehensive [Proxies Guide](https://github.com/KevinBytesTheDust/cvamp/wiki/Webshare.io-Proxies-Guide).  
   Get 10 free proxies for testing and 10% off your first proxy purchase at [Webshare.io](https://blueloperlabs.ch/proxy/wf).  

Read the comprehensive [wiki](https://github.com/KevinBytesTheDust/cvamp/wiki) for [usage tips](https://github.com/KevinBytesTheDust/cvamp/wiki/Advanced-features-and-controls) and [troubleshooting steps](https://github.com/KevinBytesTheDust/cvamp/wiki/Troubleshooting).  
Ask questions in the [discussions](https://github.com/KevinBytesTheDust/cvamp/discussions) or [report issues](https://github.com/KevinBytesTheDust/cvamp/issues).

### Mandatory Requirements

- Provide your own private HTTP proxies to the [proxy_list.txt](proxy/proxy_list.txt) or follow our [Proxies Guide](https://github.com/KevinBytesTheDust/cvamp/wiki/Webshare.io-Proxies-Guide).  
Get 10 free proxies for testing and 10% off your first proxy purchase at [Webshare.io](https://blueloperlabs.ch/proxy/wf).  

- Chrome needs to be already installed on your system.

### Platform Support Overview (2025.10.18)

| Platform              |      Twitch      |       Kick       |        Youtube       |
| --------------------- | :--------------: | :--------------: | :------------------: |
| General Functionality |        :heavy\_check\_mark:        |        :heavy\_check\_mark:        | :heavy\_check\_mark: |
| Lowest Quality Select | :heavy\_check\_mark: |        :heavy\_check\_mark:        | :heavy\_check\_mark: | 
| Status Boxes Updates  | :heavy\_check\_mark: |        :heavy\_check\_mark:        | :heavy\_check\_mark: |
| Login/Authentication  |        :heavy\_check\_mark:        |        :heavy\_check\_mark:        |          :x:         |  
| Automatic Chat        |        :heavy\_check\_mark:        |        :heavy\_check\_mark:        |          :x:         |    
| Automatic Follow      |        :heavy\_check\_mark:        |       :x:        |          :x:         |   
| Low CPU Usage Mode    |        :heavy\_check\_mark:        |       :x:        |          :x:         | 

:heavy_check_mark: Supported, :warning: Problems, :x: Unsupported, ⏳ In Development

### In Action

![image](https://github.com/user-attachments/assets/94611ec5-c6c7-4473-9bb4-3f41dad3b563)

#### Controls and Color codes of the square boxes

⬛ - Instance is spawned. 🟨 - Instance is buffering. 🟩 - Instance is actively watching.

🖱️ Left click: Refresh page.
🖱️ Right click: Destroy instance.
🖱️ Left click + CTRL: Take screenshot.

### Misc

- CPU load and bandwidth can get heavy. Channels with 160p work best.
- Tested on Windows 10 with headless ~100, headful ~30. Linux and macOS is experimental.

The Crude Viewer Amplifier (CVAmp) is a small GUI tool that spawns muted Google Chrome instances via [Playwright](https://github.com/microsoft/playwright-python), each with a different HTTP proxy connection. Each instance navigates to the streaming channel and selects the lowest possible resolution.

Read the comprehensive [wiki](https://github.com/KevinBytesTheDust/cvamp/wiki) for a [detailed tutorial](https://github.com/KevinBytesTheDust/cvamp/wiki/Detailed-Tutorial), [usage tips](https://github.com/KevinBytesTheDust/cvamp/wiki/Advanced-features-and-controls) and [troubleshooting steps](https://github.com/KevinBytesTheDust/cvamp/wiki/Troubleshooting).

### Full disclaimer

This project was established to contribute to open-source collaboration and showcase the educational value of reverse engineering. Although its primary purpose is for learning and understanding, users must be aware that altering viewer metrics on platforms such as Twitch violates their Terms of Service and could lead to legal repercussions. We urge users to engage with this tool responsibly. Misuse is solely at your discretion and risk. Discussions promoting illegal activities will be promptly removed.
