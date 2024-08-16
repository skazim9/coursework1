# -*- coding: utf-8 -*-

import datetime
import json
import logging
from pathlib import Path
import pandas as pd
import os
import requests
from dotenv import load_dotenv

load_dotenv("..\\.env")

ROOT_PATH = Path(__file__).resolve().parent.parent

logger = logging.getLogger("logs")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("..\\logs\\utils.log", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_data(data: str) -> datetime.datetime:
    """Функция преобразования даты"""
    logger.info(f"Получена строка даты: {data}")
    try:
        data_obj = datetime.datetime.strptime(data, "%d.%m.%Y %H:%M:%S")
        logger.info(f"Преобразована в объект datetime: {data_obj}")
        return data_obj
    except ValueError as e:
        logger.error(f"Ошибка преобразования даты: {e}")
        raise e


def read_excel_file(file_path) -> pd.DataFrame:
    """Функция принимает путь до excel файла и преобразует в DataFrame"""
    logger.info(f"Вызвана функция получения транзакций из файла {file_path}")
    try:
        df_transactions = pd.read_excel(file_path)
        logger.info(f"Файл {file_path} найден, данные о транзакциях получены")
        return df_transactions
    except FileNotFoundError:
        logger.info(f"Файл {file_path} не найден")
        raise


def get_dict_transaction(file_path) -> list[dict]:
    """Функция преобразовывающая датафрейм в словарь pyhton"""
    logger.info(f"Вызвана функция get_dict_transaction с файлом {file_path}")
    try:
        df = pd.read_excel(file_path)
        logger.info(f"Файл {file_path}  прочитан")
        dict_transaction = df.to_dict(orient="records")
        logger.info("Датафрейм  преобразован в список словарей")
        return dict_transaction
    except FileNotFoundError:
        logger.error(f"Файл {file_path} не найден")
        raise
    except Exception as e:
        logger.error(f"Произошла ошибка: {str(e)}")
        raise


def get_user_setting(path):
    """Функция перевода настроек пользователя(курс и акции) из json объекта"""
    logger.info(f"Вызвана функция с файлом {path}")
    with open(path, "r", encoding="utf-8") as f:
        user_setting = json.load(f)
        logger.info("Получены настройки пользователя")
    return user_setting["user_currencies"], user_setting["user_stocks"]


def get_currency_rates(currencies):
    """функция, возвращает курсы"""
    logger.info("Вызвана функция для получения курсов")
    API_KEY = os.environ.get("API_KEY_CURRENCY")
    symbols = "%2C".join(currencies)
    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={symbols}&base=RUB"
    payload = {}

    headers = {"apikey": API_KEY}
    response = requests.request("GET", url, headers=headers, data=payload)
    resp_data = response.json()
    status_code = response.status_code
    if status_code != 200:
        print(f"Запрос не был успешным. Возможная причина: {response.reason}")

    else:
        data_list = [
            {key: round(1 / value, 2)}
            for key, value in resp_data.get("rates").items()
            if key in currencies
        ]
        return data_list


def get_stock_price(stocks):
    """Функция, возвращающая курсы акций"""
    logger.info("Вызвана функция возвращающая курсы акций")
    API_KEY_STOCK = os.environ.get('API_KEY_STOCK')
    stock_price = []
    for stock in stocks:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={API_KEY_STOCK}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Запрос не был успешным. Возможная причина: {response.reason}")

        else:
            resp_data = response.json()
            stock_price.append({stock: float(resp_data.get("Global Quote").get("05. price"))})
    logger.info("Функция завершила свою работу")
    return stock_price
