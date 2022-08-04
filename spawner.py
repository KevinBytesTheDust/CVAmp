import datetime
import json
import random
import threading
from playwright.sync_api import sync_playwright
import logging

logger = logging.getLogger(__name__)


class Instance:
    def __init__(self, user_agent, proxy_dict, target_url, location_info=None, headless=False, id=-1):

        self.playwright = None
        self.context = None
        self.browser = None
        self.last_active_resume_time = 0
        self.last_active_timestamp = None
        self.is_watching = False

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

        self.command = None
        self.page = None

    def check_if_watching(self):
        datetime_now = datetime.datetime.now()

        if not self.last_active_timestamp:
            self.last_active_timestamp = datetime_now - datetime.timedelta(seconds=10)

        if self.last_active_timestamp > datetime_now - datetime.timedelta(seconds=10):
            return True

        current_resume_time = self.page.evaluate("window.localStorage.getItem('livestreamResumeTimes');")

        if current_resume_time:
            resume_time = json.loads(current_resume_time)
            resume_time = list(resume_time.values())[0]

            if resume_time > self.last_active_resume_time:
                self.last_active_timestamp = datetime.datetime.now()
                self.last_active_resume_time = resume_time
                return True
        return False

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
            if any([self.page, self.context, self.browser]):
                self.page.close()
                self.context.close()
                self.browser.close()
                self.playwright.stop()
            self.location_info['free'] = True

    def loop_and_check(self):
        while True:
            self.page.wait_for_timeout(5000)
            self.is_watching = self.check_if_watching()

            if self.command == "exit":
                return
            if self.command == "screenshot":
                self.save_screenshot()
            if self.command == "refresh":
                self.reload_page()
            self.command = None

    def save_screenshot(self):
        filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + f"_instance{self.id}.png"
        self.page.screenshot(path=filename)

    def reload_page(self):
        self.page.reload(timeout=30000)
        self.page.wait_for_selector(".persistent-player", timeout=30000)
        self.page.wait_for_timeout(1000)
        self.page.keyboard.press("Alt+t")

    def spawn_page(self):

        proxy_dict = self.proxy_dict
        server_ip = proxy_dict.get('server', 'no proxy')

        if not proxy_dict:
            proxy_dict = None

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            proxy=proxy_dict,
            headless=self._headless,
            channel='chrome',
            args=["--window-position={},{}".format(self.location_info["x"], self.location_info["y"])],
        )
        self.context = self.browser.new_context(
            user_agent=self.user_agent,
            viewport={"width": 800, "height": 600},
            proxy=proxy_dict,
        )

        self.page = self.context.new_page()
        self.page.add_init_script("""navigator.webdriver = false;""")

        self.page.goto("https://www.twitch.tv/login", timeout=100000)

        twitch_settings = {
            'mature': 'true',
            'video-muted': '{"default": "false"}',
            'volume': '0.5',
            'video-quality': '{"default": "160p30"}',
            'lowLatencyModeEnabled': 'false',
        }

        try:
            self.page.click("button[data-a-target=consent-banner-accept]", timeout=15000)
        except:
            logger.warning("Cookie consent banner not found/clicked.")

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

        logger.info(
            f"{threading.currentThread()} with instance no {self.id} fully initialized, using proxy {server_ip}"
        )
