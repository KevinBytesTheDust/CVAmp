# Crude twitch viewer bot with selenium 

Disclaimer: For educational purpose only!

Small script that spawns muted Google Chrome instances, each with a different user-agent and SOCKS5 proxy connection. 
Each instance navigates to the twitch channel, activates theater mode and adheres itself to the available screen space. 
Settings in localStorage ensure the lowest possible resolution.

### Important
- Maximum recommended chrome instance count is ~25.
- CPU load and bandwidth can get heavy. Channels with 160p work best.
- Requires a list of SOCKS 5 proxies
- Headless option can reduce CPU load by ~30%.
- Only tested on Windows 10 and Chrome Version 97

### In action

![](instances_spawning.gif)

### Usage

```
Start in REPL and interact with manager through command examples below

Spawn a single instance or multiple with threading:
manager.spawn_instance()
manager.spawn_instances(5)

Delete a single instance or all with threading:
manager.delete_latest()
manager.delete_all_instances()
```


