import time

from spawner import BrowserManager

def test_open_one_instance(record_property):
    target_url = "https://www.twitch.tv/electricallongboard"
    SPAWNER_THREAD_COUNT = 3
    CLOSER_THREAD_COUNT = 10
    REQUEST_CAPTURE = True
    HEADLESS = False

    manager = BrowserManager(target_url,
                             SPAWNER_THREAD_COUNT,
                             CLOSER_THREAD_COUNT,
                             REQUEST_CAPTURE,
                             HEADLESS)

    manager.spawn_instance()

    time.sleep(20)

    request_count = len(
        [1 for r in manager.browser_instances[0].driver.requests if r.url.endswith(".ts")])

    manager.delete_latest()

    record_property("request_count", request_count)

    assert request_count > 10
