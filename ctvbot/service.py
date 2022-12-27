from __future__ import annotations
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .manager import InstanceManager

logger = logging.getLogger(__name__)


class StatusChecker:
    def __init__(self, manager: InstanceManager, update_interval_s=60):
        self.update_interval = update_interval_s
        self.worker_thread = None
        self.manager = manager

        # start thread
    def loop(self):
        self.manager.update_instances_alive_count()
        self.manager.update_instances_watching_count()
        # see if gui updates
        # send to relic?



