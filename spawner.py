import random
import tkinter
from seleniumwire import webdriver

from proxy import ProxyGetter


class BrowserManager:
    def __init__(self, target_url):
        self.target_url = target_url

        self.window_height = 300
        self.window_width = 500

        self.screen_width = self.get_screen_resolution("width")
        self.screen_height = self.get_screen_resolution("height")

        self.user_agents_list = []
        with open("user-agents.txt") as user_agents:
            self.user_agents_list = user_agents.read().splitlines()

        self.spawn_locations = self.generate_spawn_locations()
        self.browser_instances = []

        self.proxies = ProxyGetter()

    def get_random_user_agent(self):
        return random.choice(self.user_agents_list)

    def get_screen_resolution(self, kind):
        root = tkinter.Tk()
        root.withdraw()

        if kind == "width":
            return root.winfo_screenwidth()
        if kind == "height":
            return root.winfo_screenheight()

        return None

    def generate_spawn_locations(self):
        spawn_locations = []

        cols = int(self.screen_width / self.window_width)
        rows = int(self.screen_height / self.window_height)

        for row in range(rows):
            for col in range(cols):
                spawn_locations.append((col * self.window_width, row * self.window_height))

        return spawn_locations

    def spawn_instance(self):
        browser_instance = BrowserSpawn(
            len(self.browser_instances),
            self.window_height,
            self.window_width,
            self.get_random_user_agent(),
            self.proxies.get_proxy(),
            self.target_url,
            self.spawn_locations[len(self.browser_instances)],
        )

        browser_instance.modify_driver()  # Todo: Kill instance if error

        self.browser_instances.append(browser_instance)

    def delete_latest(self):
        if not self.browser_instances:
            print("No instances found")
            return

        self.browser_instances.pop()

    def delete_all_instances(self):
        for i in range(len(self.browser_instances)):
            self.delete_latest()


class BrowserSpawn:
    def __init__(
        self, instance_no, window_height, window_width, user_agent, proxy_string, target_url, spawn_position,
    ):
        self.instance_no = instance_no
        self.window_height = window_height
        self.window_width = window_width
        self.user_agent = user_agent
        self.proxy_string = proxy_string
        self.target_url = target_url
        self.spawn_position = spawn_position

        self.driver = self.spawn_driver()
        self.css_retries = 3

    def __del__(self):
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

        self.driver.set_window_size(self.window_width, self.window_height)
        self.driver.set_window_position(x=self.spawn_position[0], y=self.spawn_position[1], windowHandle="current")
