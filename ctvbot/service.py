from __future__ import annotations
import logging
import threading
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .manager import InstanceManager

logger = logging.getLogger(__name__)


class StatusChecker:
    def __init__(self, manager: InstanceManager, update_interval_s=2):
        self.update_interval = update_interval_s
        self.manager = manager
        self.worker_thread = threading.Thread(target=self.loop, daemon=True)
        self.check_status = True

        self.worker_thread.start()

    def loop(self):
        while self.check_status:
            self.manager.update_instances_overview()
            self.manager.update_instances_alive_count()
            self.manager.update_instances_watching_count()
            time.sleep(self.update_interval)


class RestartChecker:
    pass
