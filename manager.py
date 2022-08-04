import os
import random
import threading
import time

from concurrent.futures.thread import ThreadPoolExecutor

from proxy.proxy import ProxyGetter
from screen import Screen

import logging

from spawner import Instance

logger = logging.getLogger(__name__)


class InstanceManager:
    def __init__(
        self,
        spawn_thread_count,
        delete_thread_count,
        headless,
        proxy_file_name,
        spawn_interval_seconds=2,
        target_url=None,
    ):

        logger.info("Manager start")

        self.spawn_interval_seconds = spawn_interval_seconds
        self._headless = headless
        self._spawn_thread_count = spawn_thread_count
        self._delete_thread_count = delete_thread_count

        self.target_url = target_url

        self.screen = Screen(window_width=500, window_height=300)
        self.proxies = ProxyGetter(os.path.join(os.getcwd(), "proxy", proxy_file_name))

        self.user_agents_list = self.get_user_agents()

        self.browser_instances_dict = {}

    def get_user_agents(self):
        try:
            with open(os.path.join(os.getcwd(), "proxy", "user-agents.txt")) as user_agents:
                return user_agents.read().splitlines()
        except Exception as e:
            logger.exception(e)
            raise FileNotFoundError()

    def set_headless(self, new_value: bool):
        self._headless = new_value

    def __del__(self):
        print("Deleting manager: cleaning up instances")
        self.delete_all_instances()

    def get_random_user_agent(self):
        return random.choice(self.user_agents_list)

    def get_active_count(self):
        return len(self.browser_instances_dict.keys())

    def get_instances_overview(self):
        return_dict = {}
        for key, instance_dict in self.browser_instances_dict.items():
            return_dict[key] = 'alive'

            if instance_dict['instance'].fully_initialized:
                return_dict[key] = 'init'

            if instance_dict['instance'].is_watching:
                return_dict[key] = 'watching'

        return return_dict

    def get_fully_initialized_count(self):
        return len(
            [True for instance in self.browser_instances_dict.values() if instance['instance'].fully_initialized]
        )

    def spawn_instances(self, n, target_url=None):
        for _ in range(n):
            self.spawn_instance(target_url)
            time.sleep(self.spawn_interval_seconds)

    def spawn_instance(self, target_url=None):
        t = threading.Thread(target=self.spawn_instance_thread, args=(target_url,))
        t.start()

    def spawn_instance_thread(self, target_url=None):

        if not any([target_url, self.target_url]):
            raise Exception("No target target url provided")

        with threading.Lock():
            user_agent = self.get_random_user_agent()
            proxy = self.proxies.get_proxy_as_dict()

            if self._headless:
                screen_location = self.screen.get_default_location()
            else:
                screen_location = self.screen.get_free_screen_location()

            if not screen_location:
                print("no screen space left")
                return

            instance_dict = dict()

            if not self.browser_instances_dict:
                browser_instance_id = 1
            else:
                browser_instance_id = max(self.browser_instances_dict.keys()) + 1

            logger.info(f"{threading.currentThread()} starting instance no {browser_instance_id}")

            self.browser_instances_dict[browser_instance_id] = instance_dict

        if not target_url:
            target_url = self.target_url

        browser_instance = Instance(user_agent, proxy, target_url, screen_location, self._headless, browser_instance_id)

        instance_dict['thread'] = threading.currentThread()
        instance_dict['instance'] = browser_instance

        browser_instance.start()

        if browser_instance_id in self.browser_instances_dict:
            del browser_instance
            self.browser_instances_dict.pop(browser_instance_id)

    def queue_screenshot(self, instance_id: int) -> bool:
        if instance_id not in self.browser_instances_dict:
            return False

        self.browser_instances_dict[instance_id]['instance'].command = 'screenshot'
        print("Saved screenshot of instance id", instance_id)

    def queue_refresh(self, instance_id: int) -> bool:
        if instance_id not in self.browser_instances_dict:
            return False

        print("Refreshing the instance id", instance_id)
        self.browser_instances_dict[instance_id]['instance'].command = 'refresh'

    def delete_specific(self, instance_id: int) -> bool:
        if instance_id not in self.browser_instances_dict:
            return False

        print("Destroying the instance id", instance_id)
        self.browser_instances_dict[instance_id]['instance'].command = 'exit'

    def delete_latest(self):
        if not self.browser_instances_dict:
            print("No instances found")
            return

        with threading.Lock():
            latest_key = max(self.browser_instances_dict.keys())
            instance_dict = self.browser_instances_dict.pop(latest_key)
            logger.info(f"Issuing shutdown of instance #{latest_key}")
            time.sleep(0.3)

            instance_dict['instance'].command = "exit"

    def delete_all_instances(self):
        with ThreadPoolExecutor(max_workers=self._delete_thread_count) as executor:
            for i in range(len(self.browser_instances_dict)):
                executor.submit(self.delete_latest)
