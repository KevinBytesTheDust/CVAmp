import random
from typing import Optional

import logging
logger = logging.getLogger(__name__)

class ProxyGetter:
    def __init__(self, pathed_file_name="proxy/proxy_list.txt"):
        self.proxy_list = []
        self.pathed_file_name = pathed_file_name
        self.socks5_pattern = "socks5://{}:{}@{}"

        self.build_proxy_list()

    def build_proxy_list(self):

        try:
            if self.pathed_file_name.endswith(".json"):
                raise NotImplementedError("JSON file not implemented yet")
            elif self.pathed_file_name.endswith(".txt"):
                self.build_proxy_list_txt()
            else:
                print("File type not supported")
        except Exception as e:
            logger.exception(e)

    def build_proxy_list_txt(self):
        with open(self.pathed_file_name, "r") as fp:
            proxy_list = fp.read().splitlines()

        for proxy in proxy_list:
            proxy_parts = proxy.split(":")
            if len(proxy_parts) == 4:
                username = proxy_parts[2]
                password = proxy_parts[3]
                ip_port = ":".join(proxy_parts[0:2])

                if username != "username":
                    self.proxy_list.append({
                        'server': "http://"+ip_port,
                        'username': username,
                        'password': password
                        })

        random.shuffle(self.proxy_list)

    def build_proxy_string(self, username, password, ip_port):
        if username == "username":
            return None
        return self.socks5_pattern.format(username, password, ip_port)

    def get_proxy_as_dict(self) -> dict:
        if not self.proxy_list:
            return {}

        proxy = self.proxy_list.pop(0)
        self.proxy_list.append(proxy)
        return proxy
