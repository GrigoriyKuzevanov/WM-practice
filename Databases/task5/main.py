from spimex_parser import SpimexBulletinParser
from bulletin_xls_parser import parse_xls_bulletin_to_dict
from db_saver import save_bulletin_to_db


def main() -> None:
    """
    Основная функция для выполнения процесса сбора, обработки и сохранения данных
    о результатах торгов СПбМТСБ.

    Выполняет следующие шаги:
    1. Инициализирует парсер для получения ссылки на последний бюллетень.
    2. Загружает файл бюллетеня в формате XLS.
    3. Парсит загруженный файл и извлекает данные в виде списка словарей.
    4. Сохраняет каждый элемент данных в базу данных.
    """
    
    parser = SpimexBulletinParser()

    date, last_bulletin_link = parser.get_last_bulletin_link()
    parser.upload_bulletin_xls(last_bulletin_link, date)
    
    bulletin_data = parse_xls_bulletin_to_dict(date)
    
    for item in bulletin_data:
        save_bulletin_to_db(item, date)


if __name__ == "__main__":
    main()
