import datetime
import json
import logging

from ctvbot import utils
from ctvbot.instance import Instance

logger = logging.getLogger(__name__)


class Unknown(Instance):
    name = "UNKNOWN"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def todo_every_loop(self):
        self.page.keyboard.press("Tab")

    def update_status(self):
        pass

    def todo_after_spawn(self):
        self.goto_with_retry(self.target_url)
        self.page.wait_for_timeout(1000)


class Youtube(Instance):
    name = "YOUTUBE"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def todo_every_loop(self):
        self.page.keyboard.press("Tab")

    def update_status(self):
        pass

    def todo_after_spawn(self):
        self.goto_with_retry(self.target_url)
        self.page.wait_for_timeout(1000)
        self.page.query_selector_all("button.yt-spec-button-shape-next--call-to-action")[-1].click()
        self.status = utils.InstanceStatus.INITIALIZED


class Kick(Instance):
    name = "KICK"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def todo_every_loop(self):
        self.page.keyboard.press("Tab")

    def update_status(self):
        pass

    def todo_after_spawn(self):
        self.goto_with_retry(self.target_url)
        self.page.wait_for_timeout(1000)

        if 'cloudflare' in self.page.content().lower():
            raise utils.CloudflareBlockException("Blocked by Cloudflare.")


class Twitch(Instance):
    name = "TWITCH"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def todo_after_load(self):
        self.page.wait_for_selector(".persistent-player", timeout=30000)
        self.page.wait_for_timeout(1000)
        self.page.keyboard.press("Alt+t")

    def update_status(self):
        datetime_now = datetime.datetime.now()

        # set default timestamp, to give the steam time to progress
        if not self.last_active_timestamp:
            self.last_active_timestamp = datetime_now - datetime.timedelta(seconds=10)

        if self.last_active_timestamp > datetime_now - datetime.timedelta(seconds=10):
            self.status = utils.InstanceStatus.WATCHING
            return

        current_resume_time = self.page.evaluate("window.localStorage.getItem('livestreamResumeTimes');")

        if current_resume_time:
            resume_time = json.loads(current_resume_time)
            resume_time = list(resume_time.values())[0]

            if resume_time > self.last_active_resume_time:
                self.last_active_timestamp = datetime.datetime.now()
                self.last_active_resume_time = resume_time
                self.status = utils.InstanceStatus.WATCHING
                return
        self.status = utils.InstanceStatus.BUFFERING

    def todo_after_spawn(self):
        self.goto_with_retry("https://www.twitch.tv/login")

        twitch_settings = {
            "mature": "true",
            "video-muted": '{"default": "false"}',
            "volume": "0.5",
            "video-quality": '{"default": "160p30"}',
            "lowLatencyModeEnabled": "false",
        }

        try:
            self.page.click("button[data-a-target=consent-banner-accept]", timeout=15000)
        except:
            logger.warning("Cookie consent banner not found/clicked.")

        for key, value in twitch_settings.items():
            tosend = """window.localStorage.setItem('{key}','{value}');""".format(key=key, value=value)
            self.page.evaluate(tosend)

        self.page.set_viewport_size(
            {
                "width": self.location_info["width"],
                "height": self.location_info["height"],
            }
        )

        self.goto_with_retry(self.target_url)
        self.page.wait_for_timeout(1000)
        self.page.wait_for_selector(".persistent-player", timeout=15000)
        self.page.keyboard.press("Alt+t")
        self.page.wait_for_timeout(1000)

        self.status = utils.InstanceStatus.INITIALIZED
