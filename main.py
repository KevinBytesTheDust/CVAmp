"""
Start in REPL and interact with manager with command examples below

Spawn a single instance or multiple with threading:
manager.spawn_instance()
manager.spawn_instances(5)

Delete a single instance or all with threading:
manager.delete_latest()
manager.delete_all_instances()
"""

from spawner import BrowserManager

import logger_config

logger_config.setup()

SPAWNER_THREAD_COUNT = 3
CLOSER_THREAD_COUNT = 10
PROXY_FILE_NAME = "proxy_list.txt"
HEADLESS = False
SPAWN_INTERVAL_SECONDS = 2

target_url = "https://www.twitch.tv/username"

manager = BrowserManager(spawn_thread_count=SPAWNER_THREAD_COUNT,
                         delete_thread_count=CLOSER_THREAD_COUNT,
                         headless=HEADLESS,
                         proxy_file_name=PROXY_FILE_NAME,
                         spawn_interval_seconds=SPAWN_INTERVAL_SECONDS,
                         target_url=target_url,
                         )

print("Available proxies", len(manager.proxies.proxy_list))
print("Available window locations", len(manager.screen.spawn_locations))
