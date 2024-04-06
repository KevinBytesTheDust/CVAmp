from enum import Enum, auto
from ctvbot import sites


class InstanceCommands(Enum):
    SCREENSHOT = auto()
    REFRESH = auto()
    EXIT = auto()
    RESTART = auto()
    NONE = auto()


class InstanceStatus(Enum):
    STARTING = "starting"
    BUFFERING = "buffering"
    WATCHING = "watching"
    RESTARTING = "restarting"
    INITIALIZED = "initialized"
    SHUTDOWN = "shutdown"
    INACTIVE = "inactive"


class CloudflareBlockException(Exception):
    pass
