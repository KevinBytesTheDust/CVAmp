# Crude twitch viewer bot with selenium 

Disclaimer: For educational purpose only!

Small script that spawns Google Chrome instances, each with a different user-agent and SOCKS5 proxy connection. 
Each instance navigates to the twitch channel, selects the lowest possible resolution and
adheres itself to the available screen space.

### Important
- Maximum recommended chrome instance count is ~25.   
  CPU load is heavy. Bandwidth is ok with low resolution.
- Requires a list of SOCKS 5 proxies
- Headless option can reduce CPU load by ~30%.
- Only tested on Windows 10 and Chrome Version 93.0.4577.63

### In action

![](instances_spawning.gif)


