import logging
import os
import random

logger = logging.getLogger(__name__)


class ProxyGetter:
    def __init__(self, proxy_file_name="proxy_list.txt"):
        self.proxy_list = []
        self.pathed_file_name = os.path.join(os.getcwd(), "proxy", proxy_file_name)
        self.build_proxy_list()

    def build_proxy_list(self):
        try:
            if self.pathed_file_name.endswith(".txt"):
                self.build_proxy_list_txt()
            else:
                print("File type not supported")
        except Exception as e:
            logger.exception(e)
            raise FileNotFoundError(f"Unable to find {self.pathed_file_name}")

    def build_proxy_list_txt(self):
        with open(self.pathed_file_name, "r") as fp:
            proxy_list = [line.strip() for line in fp if line.strip()]

        for proxy in proxy_list:
            proxy_parts = proxy.split(":")
            if len(proxy_parts) == 4:
                ip, port, username, password = proxy_parts
                if username.lower() != "username":
                    self.proxy_list.append(
                        {
                            "server": f"http://{ip}:{port}",
                            "username": username,
                            "password": password,
                        }
                    )
                else:
                    logger.warning(f"Skipping proxy with placeholder username: {proxy}")
            elif len(proxy_parts) == 2:
                ip, port = proxy_parts
                self.proxy_list.append(
                    {
                        "server": f"http://{ip}:{port}",
                        "username": "",
                        "password": "",
                    }
                )
            else:
                logger.warning(f"Invalid proxy format: {proxy}")

    def get_proxy_as_dict(self) -> dict:
        if not self.proxy_list:
            return {}

        proxy = self.proxy_list.pop(-1)
        self.proxy_list.insert(0, proxy)
        return proxy
