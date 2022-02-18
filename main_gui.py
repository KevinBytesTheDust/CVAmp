from gui import GUI
from spawner import BrowserManager

SPAWNER_THREAD_COUNT = 3
CLOSER_THREAD_COUNT = 10
PROXY_FILE_NAME = "proxy_list.txt"
DISABLE_CAPTURE = True
HEADLESS = True

# todo add chrome version
manager = BrowserManager(SPAWNER_THREAD_COUNT,
                         CLOSER_THREAD_COUNT,
                         DISABLE_CAPTURE,
                         HEADLESS,
                         PROXY_FILE_NAME)

print("Available proxies", len(manager.proxies.proxy_list))
print("Available window locations", len(manager.screen.spawn_locations))

g = GUI(manager)
g.run()
