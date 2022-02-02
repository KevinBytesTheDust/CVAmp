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

target_url = "https://www.twitch.tv/username"
SPAWNER_THREAD_COUNT = 3
SPAWNER_THREAD_COUNT = 4
# todo: Have only one chromedriver instance and listen to requests with driver.request_interceptor
# asnchronously trigger this requests to many requests_bots with proxy and user-agent
# and mimic the chromedriver requests. Use only HEAD for GET requests to avoid always any network traffic
CLOSER_THREAD_COUNT = 10
DISABLE_CAPTURE = True
HEADLESS = False

manager = BrowserManager(target_url,
                         SPAWNER_THREAD_COUNT,
                         CLOSER_THREAD_COUNT,
                         DISABLE_CAPTURE,
                         HEADLESS)

print("Available proxies", len(manager.proxies.proxy_list))
print("Available window locations", len(manager.screen.spawn_locations))
