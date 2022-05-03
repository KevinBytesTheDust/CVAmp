from gui import GUI
from spawner import BrowserManager

SPAWNER_THREAD_COUNT = 3
CLOSER_THREAD_COUNT = 10
PROXY_FILE_NAME = "proxy_list.txt"
HEADLESS = False
SPAWN_INTERVAL_SECONDS = 2


manager = BrowserManager(spawn_thread_count=SPAWNER_THREAD_COUNT,
                         delete_thread_count=CLOSER_THREAD_COUNT,
                         headless=HEADLESS,
                         proxy_file_name=PROXY_FILE_NAME,
                         spawn_interval_seconds=SPAWN_INTERVAL_SECONDS,
                         )

print("Available proxies", len(manager.proxies.proxy_list))
print("Available window locations", len(manager.screen.spawn_locations))

GUI(manager).run()