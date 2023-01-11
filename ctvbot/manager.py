import datetime
import logging
import os
import random
import threading
import time

from . import logger_config, utils

logger_config.setup()
from .instance import Instance
from .proxy import ProxyGetter
from .screen import Screen
from .service import RestartChecker
from .utils import InstanceCommands

logger = logging.getLogger(__name__)


class InstanceManager:
    def __init__(
        self,
        spawn_thread_count,
        delete_thread_count,
        headless,
        auto_restart,
        proxy_file_name,
        spawn_interval_seconds=2,
        target_url=None,
    ):

        logger.info("Manager start")

        self._spawn_thread_count = spawn_thread_count
        self._delete_thread_count = delete_thread_count
        self._headless = headless
        self._auto_restart = auto_restart
        self.proxies = ProxyGetter(os.path.join(os.getcwd(), "proxy", proxy_file_name))
        self.spawn_interval_seconds = spawn_interval_seconds
        self.target_url = target_url

        self.manager_lock = threading.Lock()
        self.screen = Screen(window_width=500, window_height=300)
        self.user_agents_list = self.get_user_agents()
        self.browser_instances = {}

        self.instances_overview = dict()
        self.instances_alive_count = 0
        self.instances_watching_count = 0

        self.restart_checker = RestartChecker(manager=self, restart_interval_s=1200)

    def get_user_agents(self):
        try:
            with open(os.path.join(os.getcwd(), "proxy/user-agents.txt")) as user_agents:
                return user_agents.read().splitlines()
        except Exception as e:
            logger.exception(e)
            raise FileNotFoundError()

    def get_headless(self) -> bool:
        return self._headless

    def set_headless(self, new_value: bool):
        self._headless = new_value

    def get_auto_restart(self) -> bool:
        return self._auto_restart

    def set_auto_restart(self, new_value: bool):
        logger.info(f"Setting auto-restart to " + str(new_value))
        self._auto_restart = new_value
        self.reconfigure_auto_restart_status()

    def __del__(self):
        print("Deleting manager: cleaning up instances", datetime.datetime.now())
        self.delete_all_instances()
        print("Manager shutting down", datetime.datetime.now())

    def get_random_user_agent(self):
        return random.choice(self.user_agents_list)

    def update_instances_alive_count(self):
        alive_instances = filter(
            lambda instance: instance.status != utils.InstanceStatus.SHUTDOWN, self.browser_instances.values()
        )
        self.instances_alive_count = len(list(alive_instances))

    def reconfigure_auto_restart_status(self):
        if self.instances_alive_count and self._auto_restart:
            self.restart_checker.start()
        else:
            self.restart_checker.stop()

    def update_instances_watching_count(self):
        self.instances_watching_count = len(
            [1 for instance in self.browser_instances.values() if instance.status == utils.InstanceStatus.WATCHING]
        )

    def update_instances_overview(self):
        new_overview = {}
        for instance_id, instance in self.browser_instances.items():
            new_overview[instance_id] = instance.status
        self.instances_overview = new_overview

    def spawn_instances(self, n, target_url=None):
        for _ in range(n):
            self.spawn_instance(target_url)
            time.sleep(self.spawn_interval_seconds)

    def spawn_instance(self, target_url=None):

        if not self.browser_instances:
            browser_instance_id = 1
        else:
            browser_instance_id = max(self.browser_instances.keys()) + 1

        t = threading.Thread(
            target=self.spawn_instance_thread,
            args=(target_url, self.instance_status_report_callback, browser_instance_id),
            daemon=True,
        )
        t.start()

    def instance_status_report_callback(self, instance_id, instance_status):
        # self.instances_overview[instance_id] = instance_status
        # for now simply triggers the manager to refresh status for all instances
        # maybe track status in separate list, where instances report to
        # and shutdown instances issue remove on dict with instance id
        # his would allow the removal of "instance.status != "shutdown"" in update_instances_alive_count

        logger.info(f"{instance_status.value.upper()} instance {instance_id}")

        self.update_instances_overview()
        self.update_instances_alive_count()
        self.update_instances_watching_count()
        self.reconfigure_auto_restart_status()

    def spawn_instance_thread(self, target_url, status_reporter, browser_instance_id):

        if not any([target_url, self.target_url]):
            raise Exception("No target target url provided")

        if not target_url:
            target_url = self.target_url

        with self.manager_lock:
            user_agent = self.get_random_user_agent()
            proxy = self.proxies.get_proxy_as_dict()

            if self._headless:
                screen_location = self.screen.get_default_location()
            else:
                screen_location = self.screen.get_free_screen_location()

            if not screen_location:
                print("no screen space left")
                return

            server_ip = proxy.get("server", "no proxy")
            logger.info(f"Ordered instance {browser_instance_id}, {threading.currentThread().name}, proxy {server_ip}")

            browser_instance = Instance(
                user_agent,
                proxy,
                target_url,
                status_reporter,
                location_info=screen_location,
                headless=self._headless,
                auto_restart=self._auto_restart,
                instance_id=browser_instance_id,
            )

            self.browser_instances[browser_instance_id] = browser_instance

        browser_instance.start()

        if browser_instance_id in self.browser_instances:
            del browser_instance
            self.browser_instances.pop(browser_instance_id)

    def queue_command(self, instance_id: int, command: InstanceCommands) -> bool:
        if instance_id not in self.browser_instances:
            return False

        self.browser_instances[instance_id].command = command

    def delete_latest(self):
        if not self.browser_instances:
            print("No instances found")
            return

        latest_key = max(self.browser_instances.keys())
        self.delete_specific(latest_key)

    def delete_specific(self, instance_id):
        if instance_id not in self.browser_instances:
            print(f"Instance ID {instance_id} not found. Unable to shutdown.")
            return

        instance = self.browser_instances[instance_id]
        print(f"Issuing shutdown of instance #{instance_id}")
        instance.command = InstanceCommands.EXIT

    def delete_all_instances(self):
        for instance_id in self.browser_instances:
            self.delete_specific(instance_id)
