from enum import Enum, auto
from ctvbot import sites

supported_sites = {
    "twitch.tv/": sites.Twitch,
    "youtube.com/": sites.Youtube,
    "kick.com/": sites.Kick,
}


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
