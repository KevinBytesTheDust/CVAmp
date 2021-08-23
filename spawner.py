import random
import threading
import time
from concurrent.futures.thread import ThreadPoolExecutor

from seleniumwire import webdriver

from proxy import ProxyGetter
from screen import Screen


class BrowserManager:
    def __init__(self, target_url, spawn_thread_count, delete_thread_count):
        self._spawn_thread_count = spawn_thread_count
        self._delete_thread_count = delete_thread_count

        self.target_url = target_url

        self.screen = Screen(window_width=500, window_height=300)
        self.proxies = ProxyGetter()

        self.user_agents_list = []
        with open("user-agents.txt") as user_agents:
            self.user_agents_list = user_agents.read().splitlines()

        self.browser_instances = []

    def __del__(self):
        print("Deleting manager: cleaning up instances")
        self.delete_all_instances()

    def get_random_user_agent(self):
        return random.choice(self.user_agents_list)

    def spawn_instances(self, n):
        with ThreadPoolExecutor(max_workers=self._spawn_thread_count) as executor:
            for i in range(n):
                executor.submit(self.spawn_instance)

    def spawn_instance(self):

        with threading.Lock():
            user_agent = self.get_random_user_agent()
            proxy = self.proxies.get_proxy()
            screen_location = self.screen.get_free_screen_location()

        if not screen_location:
            print("no screen space left")
            return

        browser_instance = BrowserSpawn(user_agent, proxy, self.target_url, screen_location)

        self.browser_instances.append(browser_instance)

        browser_instance.modify_driver()  # Todo: Kill instance if error

    def delete_latest(self):
        if not self.browser_instances:
            print("No instances found")
            return

        with threading.Lock():
            instance = self.browser_instances.pop()
            print("Deleting instance no", instance.location_info["index"])
            time.sleep(0.2)

        instance.__del__()

    def delete_all_instances(self):
        with ThreadPoolExecutor(max_workers=self._delete_thread_count) as executor:
            for i in range(len(self.browser_instances)):
                executor.submit(self.delete_latest)

    def go_to(self, url, instance_no):
        # Todo
        pass

    def go_to_all(self, url):
        # Todo
        pass


class BrowserSpawn:
    def __init__(self, user_agent, proxy_string, target_url, location_info):
        self.user_agent = user_agent
        self.proxy_string = proxy_string
        self.target_url = target_url

        self.location_info = location_info

        self.driver = self.spawn_driver()
        self.css_retries = 3

    def __del__(self):
        self.location_info["free"] = True

        if self.driver:
            self.driver.quit()

    def spawn_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--mute-audio")
        options.add_argument("user-agent={}".format(self.user_agent))

        seleniumwire_options = {}

        if self.proxy_string:
            seleniumwire_options = {"proxy": {"http": self.proxy_string, "https": self.proxy_string,}}

        driver = webdriver.Chrome("chromedriver.exe", options=options, seleniumwire_options=seleniumwire_options)

        driver.set_window_size(640, 480)

        driver.get(self.target_url)

        return driver

    def modify_driver(self):

        css_targets = [
            'button[data-a-target="consent-banner-accept"]',
            'button[data-test-selector="upsell-bottom-banner__dismiss-button"]',
            'button[data-a-target="player-overlay-mature-accept"]',
            'button[data-a-target="player-theatre-mode-button"]',
            'button[data-a-target="player-settings-button"]',
            'button[data-a-target="player-settings-menu-item-quality"]',
        ]

        for css_target in css_targets:
            for i in range(self.css_retries):
                try:
                    self.driver.find_element_by_css_selector(css_target).click()
                except:
                    print("Unable to find", css_target, "try", i)
                    continue
                break

        for i in range(self.css_retries):
            try:
                self.driver.find_elements_by_css_selector(
                    'div[data-a-target="player-settings-submenu-quality-option"]'
                )[-1].click()
            except:
                print(
                    "Unable to find", 'div[data-a-target="player-settings-submenu-quality-option"]', "try", i,
                )
                continue
            break

        self.driver.set_window_size(self.location_info["width"], self.location_info["height"])
        self.driver.set_window_position(x=self.location_info["x"], y=self.location_info["y"], windowHandle="current")
