import time


def test_open_one_instance(record_property):
    from manager import InstanceManager

    SPAWNER_THREAD_COUNT = 3
    CLOSER_THREAD_COUNT = 10
    PROXY_FILE_NAME = "proxy_list.txt"
    HEADLESS = True
    SPAWN_INTERVAL_SECONDS = 2

    target_url = "https://www.twitch.tv/shroud"

    manager = InstanceManager(
        spawn_thread_count=SPAWNER_THREAD_COUNT,
        delete_thread_count=CLOSER_THREAD_COUNT,
        headless=HEADLESS,
        proxy_file_name=PROXY_FILE_NAME,
        spawn_interval_seconds=SPAWN_INTERVAL_SECONDS,
        target_url=target_url,
    )

    manager.spawn_instance()

    instance_is_watching = False
    for _ in range(60):
        instances_overview = manager.get_instances_overview()
        if 1 in instances_overview:
            if instances_overview[1] == 'watching':
                instance_is_watching = True
                break
        time.sleep(1)

    manager.__del__()

    assert instance_is_watching
