# Crude twitch viewer bot with selenium 

Disclaimer: For educational purpose only!

Small script that spawns Google Chrome instances, each with a different user-agent and SOCKS5 proxy connection. 
Each instance navigates to the twitch channel, selects the lowest possible resolution and
adheres itself to the available screen space.

### Important
- Only tested on Windows 10 and Chrome Version 92.0.4515.131 
- Requires a list of SOCKS 5 proxies
- Tested with 20 instances, very CPU heavy. Bandwidth is ok with low resolution.
- works with -headless option, too.

### In action

![](instances_spawning.gif)


