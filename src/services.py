import json
import logging
import re

import pandas as pd

logger = logging.getLogger("logs")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("..\\logs\\services.log", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def transfers_to_individuals(transactions: pd.DataFrame) -> str:
    """Функция возвращает JSON с транзакциями переводов физлицам."""
    logger.info("Функция начала свою работу.")
    transactions_dict = transactions.to_dict("records")
    filtered_transactions = list(filter(lambda x: x["Категория"] == "Переводы", transactions_dict))
    transfers = list(filter(lambda x: re.findall(r"\w+\s\w\.", x["Описание"]), filtered_transactions))
    json_data = json.dumps(transfers, ensure_ascii=False, indent=4)
    logger.info("Функция успешно завершила свою работу.")
    return json_data
