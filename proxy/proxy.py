import json
import random


class ProxyGetter:
    def __init__(self, pathed_file_name="proxy_list.json"):
        self.proxy_list = []
        self.pathed_file_name = pathed_file_name
        self.socks5_pattern = "socks5://{}:{}@{}"

        self.build_proxy_list()


    def build_proxy_list(self):

        if self.pathed_file_name.endswith(".json"):
            self.build_proxy_list_json()
        elif self.pathed_file_name.endswith(".txt"):
            self.build_proxy_list_txt()
        else:
            print("File type not supported")

    def build_proxy_list_txt(self):
        with open(self.pathed_file_name, "r") as fp:
            proxy_list = fp.read().splitlines()

        for proxy in proxy_list:
            proxy_parts = proxy.split(":")
            if len(proxy_parts) == 4:
                username = proxy_parts[2]
                password = proxy_parts[3]
                ip_port = ":".join(proxy_parts[0:2])
                self.proxy_list.append(self.socks5_pattern.format(username, password, ip_port))


        random.shuffle(self.proxy_list)


    def build_proxy_list_json(self):

        with open(self.pathed_file_name) as json_file:
            proxy_dict = json.load(json_file)

        username = proxy_dict["user"]
        password = proxy_dict["pass"]
        ip_list = proxy_dict["ip_port"]

        if not all([username, password, ip_list]):
            print("Incomplete", self.pathed_file_name)
            return

        for ip_port in ip_list:
            self.proxy_list.append(self.socks5_pattern.format(username, password, ip_port))

        random.shuffle(self.proxy_list)

    def get_proxy(self):
        if not self.proxy_list:
            return None

        proxy = self.proxy_list.pop(0)
        self.proxy_list.append(proxy)
        return proxy
