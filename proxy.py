import json
import random


class ProxyGetter:
    def __init__(self):
        self.proxy_list = []
        self.build_proxy_list()

    def build_proxy_list(self):

        socks5_pattern = "socks5://{}:{}@{}"

        with open("proxy_list.json") as json_file:
            proxy_dict = json.load(json_file)

        username = proxy_dict["user"]
        password = proxy_dict["pass"]
        ip_list = proxy_dict["ip_port"]

        if not all([username, password, ip_list]):
            print("Incomplete proxy_list.json")
            return

        for ip_port in ip_list:
            self.proxy_list.append(socks5_pattern.format(username, password, ip_port))

        random.shuffle(self.proxy_list)

    def get_proxy(self):
        if not self.proxy_list:
            return None

        proxy = self.proxy_list.pop(0)
        self.proxy_list.append(proxy)
        return proxy
