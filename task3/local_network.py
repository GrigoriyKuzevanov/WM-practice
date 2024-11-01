import random


class Server:
    _ip_count: int = 0
    _assigned_ips: set = set()

    @classmethod
    def _get_ip(cls) -> int:
        cls._ip_count += 1
        available_ips = set(range(1, cls._ip_count + 1)) - cls._assigned_ips
        ip = random.choice(list(available_ips))
        cls._assigned_ips.add(ip)
        return ip

    @classmethod
    def _del_ip(cls, ip):
        cls._ip_count -= 1
        cls._assigned_ips.discard(ip)

    def __init__(self):
        self._ip: int = self._get_ip()
        self._buffer: list[Data] = []
        self._linked_router: Router = None

    def __del__(self):
        self._del_ip(self._ip)

    def link_to_router(self, router: "Router"):
        self._linked_router = router

    def send_data(self, data: "Data"):
        if self._linked_router:
            self._linked_router.receive_data(self.get_ip, data)

    def receive_data(self, data: "Data"):
        self._buffer.append(data)

    def get_data(self):
        result = self._buffer.copy()
        self._buffer.clear()
        return result

    @property
    def get_ip(self):
        return self._ip


class Router:
    def __init__(self):
        self.__buffer: list = []
        self.__linked_ips: dict[int, "Server"] = dict()

    def receive_data(self, server_ip: int, data: "Data"):
        if server_ip in self.__linked_ips:
            self.__buffer.append(data)

    def link(self, server: Server):
        self.__linked_ips[server.get_ip] = server
        server.link_to_router(self)

    def unlink(self, server: Server):
        self.__linked_ips.pop(server.get_ip)

    def send_data(self):
        for data in self.__buffer:
            if data.ip in self.__linked_ips:
                server_to = self.__linked_ips[data.ip]
                server_to.receive_data(data)


class Data:
    def __init__(self, data: str, ip: int):
        self.data = data
        self.ip = ip

    def __repr__(self):
        return f"Data: <{self.data}>"
