import requests
from bs4 import BeautifulSoup


class SpimexBulletinParser:
    """
    Класс для парсинга бюллетеней торгов с сайта СПбМТСБ.
    
    Attributes:
        BASE_URL (str): Базовый url сайта биржи
        TRADE_RESULTS_URL (str): Url страницы с результатами торгов
    """
    
    def __init__(self) -> None:
        """
        Инициализирует базовый URL и URL страницы с результатами торгов.
        """
        
        self.BASE_URL = "https://spimex.com"
        self.TRADE_RESULTS_URL = f"{self.BASE_URL}/markets/oil_products/trades/results"

    def get_last_bulletin_link(self) -> tuple[str, str] | None:
        """
        Получает дату торгов и ссылку для скачиваиния последнего бюллетеня.
        
        Returns:
            tuple[str, str] | None: Кортеж из даты торгов и ссылки для скачивания бюллетеня,
                                    либо None, если данные не удалось получить
        """
        
        response = requests.get(self.TRADE_RESULTS_URL)

        if response.status_code == 200:
            bs = BeautifulSoup(response.text, "html.parser")

            div = bs.find("div", class_="accordeon-inner__item")

            link_a = div.find("a", class_="accordeon-inner__item-title")
            date_span = div.find("span")

            if link_a and date_span:
                upload_url = self.BASE_URL + link_a.get("href")

                return date_span.text, upload_url

    def upload_bulletin_xls(self, link_to_upload: str, date: str) -> None:
        """
        Загружает файл бюллетеня торгов в формате xls по переданной ссылке
        и сохраняет его с именем на основе переданной даты.
        
        Args:
            link_to_upload (str): Ссылка для скачивания бюллетеня
            date (str): Дата торгов в строковом формате
        """
        
        response = requests.get(link_to_upload)

        if response.status_code == 200:
            with open(f"{date}.xls", "wb") as f:
                f.write(response.content)
