import datetime

from db import SessionFactory
from models import SpimexTradingResult


def save_bulletin_to_db(data: dict[str, str | float], date: str) -> None:
    """
    Сохраняет данные бюллетеня торгов в базу данных.
    
    Args:
        data (Dict[str, str | float]): Словарь с данными бюллетеня, включающий идентификатор, название продукта,
                                     место поставки, объем, сумму и количество договоров.
        date (str): Дата торгов в формате "дд.мм.гггг".
    """
    
    with SessionFactory() as session:
        data_to_sql = {
            "exchange_product_id": data.get("exchange_product_id"),
            "exchange_product_name": data.get("exchange_product_name"),
            "oil_id": data.get("exchange_product_id")[:4],
            "delivery_basis_id": data.get("exchange_product_id")[4:7],
            "delivery_basis_name": data.get("delivery_basis_name"),
            "delivery_type_id": data.get("exchange_product_id")[-1],
            "volume": int(data.get("volume")),
            "total": int(data.get("total")),
            "count": int(data.get("count")),
            "date": datetime.datetime.strptime(date, "%d.%m.%Y"),
        }
        record = SpimexTradingResult(**data_to_sql)
        session.add(record)
        session.commit()
