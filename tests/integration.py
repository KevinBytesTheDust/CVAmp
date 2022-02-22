import time

from spawner import BrowserManager


def test_open_one_instance(record_property):
    target_url = "https://www.twitch.tv/electricallongboard"
    SPAWNER_THREAD_COUNT = 3
    CLOSER_THREAD_COUNT = 10
    PROXY_FILE_NAME = "proxy_list.txt"
    DISABLE_CAPTURE = False
    HEADLESS = False

    manager = BrowserManager(spawn_thread_count=SPAWNER_THREAD_COUNT,
                             delete_thread_count=CLOSER_THREAD_COUNT,
                             disable_capture=DISABLE_CAPTURE,
                             headless=HEADLESS,
                             proxy_file_name=PROXY_FILE_NAME,
                             target_url=target_url)

    manager.spawn_instance()

    time.sleep(5)

    request_count = len(
        [1 for r in manager.browser_instances[0].driver.requests if r.url.endswith(".ts")])

    manager.delete_latest()

    record_property("request_count", request_count)

    assert request_count > 2
