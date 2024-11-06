import random


class Server:
    """
    Класс для представления сервера, котрый может принимать, хранить и пересылать данные.
    Сервер также имеет возможность определять уникальный адрес для связанных объектов
    класса Router.

    class Attrs:
        _ip_count (int): Счетчик IP-адресов, используется для выдачи уникальных адресов
        связанным объектам класса Router
        _assigned_ips (set): Множество уже выданных IP-адресов

    attrs:
        _ip (int): Уникальный IP-адрес сервера
        _buffer (list[Data]): Буфер для хранения полученных данных
        _linked_router (Router | None): Связанный с сервером роутер
    """

    _ip_count: int = 0
    _assigned_ips: set = set()

    @classmethod
    def _get_ip(cls) -> int:
        """
        Возвращает новый уникальный IP-адрес для сервера.
        """

        cls._ip_count += 1
        available_ips = set(range(1, cls._ip_count + 1)) - cls._assigned_ips
        ip = random.choice(list(available_ips))
        cls._assigned_ips.add(ip)
        return ip

    @classmethod
    def _del_ip(cls, ip: int) -> None:
        """
        Удаляет IP-адрес из множества уже назначенных адресов.

        Args:
            ip (int): IP-адрес для удаления
        """

        cls._ip_count -= 1
        cls._assigned_ips.discard(ip)

    def __init__(self) -> None:
        """
        Инициализирует сервер с униальным IP-адресом и пустым буфером данных.
        """

        self._ip: int = self._get_ip()
        self._buffer: list[Data] = []
        self._linked_router: Router = None

    def __del__(self) -> None:
        """
        Удаляет IP-адрес сервера при деструктуризации объекта сервера.
        """

        self._del_ip(self._ip)

    def link_to_router(self, router: "Router") -> None:
        """
        Устанавливает связь с роутером.

        Args:
            router (Router): Роутер для установления связи с сервером
        """

        self._linked_router = router

    def send_data(self, data: "Data") -> None:
        """
        Отправляет данные на роутер, только если роутер связан с сервером.

        Args:
            data (Data): Данные для отправки
        """

        if self._linked_router:
            self._linked_router.receive_data(self.get_ip, data)

    def receive_data(self, data: "Data") -> None:
        """
        Принимает данные и добавляет их в буфер сервера.

        Args:
            data (Data): Данные, принимаемые сервером
        """

        self._buffer.append(data)

    def get_data(self) -> list["Data"]:
        """
        Возвращает список данных из буфера, затем очищает буфер.
        """

        result = self._buffer.copy()
        self._buffer.clear()
        return result

    @property
    def get_ip(self) -> int:
        """
        Возвращает IP-адрес сервера.
        """

        return self._ip


class Router:
    """
    Класс, представляющий роутер для управления передачей данных
    на другие роутеры через сервер.

    Attrs:
        __buffer (list): Буфер для хранения данных
        __linked_ips (dict[int, Server]): Словарь с IP-адресами и связанными серверами
    """

    def __init__(self) -> None:
        """
        Инициализирует не подключенный к серверам роутер с пустым буфером.
        """

        self.__buffer: list = []
        self.__linked_ips: dict[int, "Server"] = dict()

    def receive_data(self, server_ip: int, data: "Data") -> None:
        """
        Принимает данные от сервера, если сервер связан с роутером, и добавляет их в буфер.

        Args:
            server_ip (int): IP-адрес сервера
            data (Data): Данные для добавления в буфер
        """

        if server_ip in self.__linked_ips:
            self.__buffer.append(data)

    def link(self, server: Server) -> None:
        """
        Связывает сервер с роутером.

        Args:
            server (Server): сервер для привязки
        """

        self.__linked_ips[server.get_ip] = server
        server.link_to_router(self)

    def unlink(self, server: Server) -> None:
        """
        Разрывает связь с сервером.

        Args:
            server (Server): сервер, с которым необходимо разорвать связь
        """

        self.__linked_ips.pop(server.get_ip)

    def send_data(self):
        """
        Отправляет данные из буфера в соответсвующие сервера, используя их IP-адреса.
        """

        for data in self.__buffer:
            if data.ip in self.__linked_ips:
                server_to = self.__linked_ips[data.ip]
                server_to.receive_data(data)


class Data:
    """
    Класс для представления данных.

    Attrs:
        data (str): Строка с данными
        ip (int): IP-адрес получателя
    """

    def __init__(self, data: str, ip: int) -> None:
        """
        Инициализирует объект данных.

        Args:
            data (str): Строка с данными
            ip (int): IP-адрес получателя
        """

        self.data = data
        self.ip = ip

    def __repr__(self) -> str:
        """
        Возвращает строкове представление объекта данных.
        """

        return f"Data: <{self.data}>"
