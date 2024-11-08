import pandas
    

def parse_xls_bulletin_to_dict(date: str) -> list[dict[str, str | float]]:
    """
    Парсит XLS-бюллетень торгов и извлекает необходимые данные в виде списка словарей.

    Загружает Excel файл, преобразует и фильтрует данные по нужным столбцам и значениям.
    Данные возвращаются только для записей, где количество договоров больше 0.

    Args:
        date (str): Дата торгов, используемая для формирования имени файла.

    Returns:
        List[Dict[str, str | float]]: Список словарей, каждый из которых представляет собой
                                      одну запись о торговом инструменте с нужными полями.
    """
    
    file_path = f"{date}.xls"
    
    df = pandas.read_excel(file_path, skiprows=6, usecols="B:F,O", skipfooter=2)
    
    df.columns = df.columns.str.replace("\n", " ", regex=True)
    
    to_numeric_columns = [
        "Количество Договоров, шт.",
        "Обьем Договоров, руб.",
        "Объем Договоров в единицах измерения",
    ]
    
    for column in to_numeric_columns:
        df[column] = pandas.to_numeric(df[column], errors="coerce")

    df_filtered = df[df["Количество Договоров, шт."] > 0]

    df_filtered = df_filtered.rename(
        columns={
            "Код Инструмента": "exchange_product_id",
            "Наименование Инструмента": "exchange_product_name",
            "Базис поставки": "delivery_basis_name",
            "Объем Договоров в единицах измерения": "volume",
            "Обьем Договоров, руб.": "total",
            "Количество Договоров, шт.": "count",
        }
    )[
        [
            "exchange_product_id",
            "exchange_product_name",
            "delivery_basis_name",
            "volume",
            "total",
            "count",
        ]
    ]
    
    return df_filtered.to_dict(orient="records")
