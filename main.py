"""
Start in REPL and interact with manager with command examples below

Spawn instance:
manager.spawn_instance()

Delete instance:
manager.delete_latest()
"""

from spawner import BrowserManager

target_url = "https://www.twitch.tv/username"

manager = BrowserManager(target_url=target_url)

print("Available proxies", len(manager.proxies.proxy_list))
print("Available window locations", len(manager.spawn_locations))
