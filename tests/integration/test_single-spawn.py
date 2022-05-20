import time

def test_open_one_instance(record_property):
    from spawner import BrowserManager

    SPAWNER_THREAD_COUNT = 3
    CLOSER_THREAD_COUNT = 10
    PROXY_FILE_NAME = "proxy_list.txt"
    HEADLESS = True
    SPAWN_INTERVAL_SECONDS = 2

    target_url = "https://www.twitch.tv/electricallongboard"

    manager = BrowserManager(spawn_thread_count=SPAWNER_THREAD_COUNT,
                             delete_thread_count=CLOSER_THREAD_COUNT,
                             headless=HEADLESS,
                             proxy_file_name=PROXY_FILE_NAME,
                             spawn_interval_seconds=SPAWN_INTERVAL_SECONDS,
                             target_url=target_url,
                             )

    manager.spawn_instance()

    for _ in range(60):
        if manager.get_fully_initialized_count() > 0:
            break
        time.sleep(1)

    instances_count = manager.get_fully_initialized_count()

    record_property("instances_count", instances_count)

    manager.__del__()

    assert instances_count == 1

