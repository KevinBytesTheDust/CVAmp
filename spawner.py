import os
import random
import threading
import time

from concurrent.futures.thread import ThreadPoolExecutor

from playwright.sync_api import sync_playwright
from proxy.proxy import ProxyGetter
from screen import Screen

import logging

logger = logging.getLogger(__name__)


class BrowserManager:
    def __init__(self,
                 spawn_thread_count,
                 delete_thread_count,
                 headless,
                 proxy_file_name,
                 spawn_interval_seconds=2,
                 target_url=None
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

    def set_headless(self, new_value: bool):
        self._headless = new_value

    def __del__(self):
        print("Deleting manager: cleaning up instances")
        self.delete_all_instances()

    def get_random_user_agent(self):
        return random.choice(self.user_agents_list)

    def get_active_count(self):
        return len(self.browser_instances_dict.keys())

    def get_fully_initialized_count(self):
        return len([True for instance in self.browser_instances_dict.values() if instance['instance'].fully_initialized])

    def spawn_instances(self, n, target_url=None):
        for _ in range(n):
            self.spawn_instance(target_url)
            time.sleep(self.spawn_interval_seconds)

    def spawn_instance(self, target_url=None):
        t = threading.Thread(target=self.spawn_instance_thread, args=(target_url,))
        t.start()

    def spawn_instance_thread(self, target_url=None):

        # spawn_allowed = False
        #
        # for spawn_try in range(30):
        #     if self.get_active_count()-2 <= self.get_fully_initialized_count():
        #         spawn_allowed = True
        #         break
        #     time.sleep(1)
        #
        # if not spawn_allowed:
        #     print("Too many uninitialized instances, stopping instance spawn")
        #     return

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

        browser_instance = BrowserSpawn(user_agent, proxy, target_url, screen_location, self._headless, browser_instance_id)

        instance_dict['thread'] = threading.currentThread()
        instance_dict['instance'] = browser_instance

        browser_instance.start()

        if browser_instance_id in self.browser_instances_dict:
            self.browser_instances_dict.pop(browser_instance_id)

    def delete_latest(self):
        if not self.browser_instances_dict:
            print("No instances found")
            return

        with threading.Lock():
            latest_key = max(self.browser_instances_dict.keys())
            instance_dict = self.browser_instances_dict.pop(latest_key)
            logger.info(f"Issuing shutdown of instance #{latest_key}")
            time.sleep(0.3)

            instance_dict['instance'].commands_queue.append(lambda: "exit")

    def delete_all_instances(self):
        with ThreadPoolExecutor(max_workers=self._delete_thread_count) as executor:
            for i in range(len(self.browser_instances_dict)):
                executor.submit(self.delete_latest)


class BrowserSpawn:
    def __init__(self, user_agent, proxy_dict, target_url, location_info=None, headless=False, id=-1):

        self.id = id
        self.user_agent = user_agent
        self.proxy_dict = proxy_dict
        self.target_url = target_url
        self._headless = headless

        self.fully_initialized = False

        self.location_info = location_info
        if not self.location_info:
            self.location_info = {
                "index": -1,
                "x": 0,
                "y": 0,
                "width": 500,
                "height": 300,
                "free": True,
                }

        self.commands_queue = []
        self.page = None

    def start(self):
        try:
            self.spawn_page()
            self.loop_and_check()
        except Exception as e:
            logger.exception(e)
            print(f"Instance {self.id} died")
        else:
            logger.info(f"{threading.currentThread()} with instance no {self.id} ended gracefully")
            print(f"Instance {self.id} shutting down")
        finally:
            if self.page:
                self.page.context.browser.close()
            self.location_info['free'] = True

    def loop_and_check(self):
        counter = 0
        while True:
            counter += random.randint(-1,3)
            self.page.wait_for_timeout(1000)
            for command in self.commands_queue:
                result = command()

                if result == "exit":
                    return

            # refresh page after ~600seconds
            if counter >= 600:
                self.reload_page()
                counter = 0

    def reload_page(self):
        self.page.reload(timeout=60000)
        self.page.wait_for_selector(".persistent-player", timeout=30000)
        self.page.wait_for_timeout(1000)
        self.page.keyboard.press("Alt+t")

    def spawn_page(self):

        proxy_dict = self.proxy_dict
        server_ip = proxy_dict.get('server', 'no proxy')

        if not proxy_dict:
            proxy_dict = None

        p = sync_playwright().start()

        browser = p.chromium.launch(
            proxy=proxy_dict,
            headless=self._headless,
            channel='chrome',
            args=["--window-position={},{}".format(self.location_info["x"], self.location_info["y"])]
            )
        context = browser.new_context(
            user_agent=self.user_agent,
            viewport={"width": 800, "height": 600},
            proxy=proxy_dict,
            )

        self.page = context.new_page()
        self.page.add_init_script("""navigator.webdriver = false;""")

        self.page.goto("https://www.twitch.tv/login")

        twitch_settings = {
            'mature': 'true',
            'video-muted': '{"default": "false"}',
            'volume': '0.5',
            'video-quality': '{"default": "160p30"}',
            'lowLatencyModeEnabled': 'false',
            }

        self.page.click("button[data-a-target=consent-banner-accept]", timeout=15000)

        for key, value in twitch_settings.items():
            tosend = """window.localStorage.setItem('{key}','{value}');""".format(key=key, value=value)
            self.page.evaluate(tosend)

        self.page.set_viewport_size({"width": self.location_info["width"], "height": self.location_info["height"]})

        self.page.goto(self.target_url, timeout=60000)
        self.page.wait_for_timeout(1000)
        self.page.wait_for_selector(".persistent-player", timeout=15000)
        self.page.keyboard.press("Alt+t")
        self.page.wait_for_timeout(1000)
        self.fully_initialized = True

        logger.info(f"{threading.currentThread()} with instance no {self.id} fully initialized, using proxy {server_ip}")
