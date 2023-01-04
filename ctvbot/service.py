from __future__ import annotations

import datetime
import logging
import threading
import time
from typing import TYPE_CHECKING

from .utils import InstanceCommands

if TYPE_CHECKING:
    from .manager import InstanceManager
    from .instance import Instance

logger = logging.getLogger(__name__)


class RestartChecker:
    def __init__(self, manager: InstanceManager, restart_interval_s: int = 600):
        self.manager = manager
        self.restart_interval_s = restart_interval_s
        self.worker_thread = None
        self.abort = False
        self.sleep_time = restart_interval_s

    def start(self):
        if not self.worker_thread or not self.worker_thread.is_alive():
            logger.info("Restarter enabled.")
            self.worker_thread = threading.Thread(target=self.restart_loop, daemon=True)
            self.worker_thread.start()

    def stop(self):
        if self.worker_thread and self.worker_thread.is_alive():
            logger.info("Restarter disabled.")
            self.abort = True

    def get_oldest_instance(self) -> Instance:
        return min(self.manager.browser_instances.values(), key=lambda instance: instance.last_restart_dt)

    def issue_restart(self, instance):
        instance.command = InstanceCommands.RESTART
        instance.last_restart_dt = datetime.datetime.now()

    def restart_loop(self):
        while True:
            time.sleep(self.sleep_time)

            instances_count = self.manager.instances_alive_count
            self.sleep_time = self.restart_interval_s / instances_count

            if self.abort:
                self.abort = False
                return

            try:
                instance = self.get_oldest_instance()
            except ValueError as e:
                logger.exception(e)
                continue
            logger.info(f"Restarting oldest instance {instance.id}. Restart interval: {self.sleep_time}")
            self.issue_restart(instance)
