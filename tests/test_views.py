import datetime as dt
import pytest
from unittest.mock import patch
from pathlib import Path
import pandas as pd
from src.views import get_greeting, get_expenses_cards, top_transaction, transaction_currency

ROOT_PATH = Path(__file__).resolve().parent.parent


def test_get_greeting_morning():
    with pytest.raises(TypeError):
        with patch('datetime.datetime.now') as mock_now:
            mock_now.return_value = dt.datetime(2023, 4, 1, 8, 0, 0)
            assert get_greeting() == "Доброе утро"


def test_get_greeting_afternoon():
    with pytest.raises(TypeError):
        with patch('datetime.datetime.now') as mock_now:
            mock_now.return_value = dt.datetime(2023, 4, 1, 14, 0, 0)
            assert get_greeting() == "Добрый день"


def test_get_greeting_evening():
    with pytest.raises(TypeError):
        with patch('datetime.datetime.now') as mock_now:
            mock_now.return_value = dt.datetime(2023, 4, 1, 19, 0, 0)
            assert get_greeting() == "Добрый вечер"


def test_get_greeting_night():
    with pytest.raises(TypeError):
        with patch('datetime.datetime.now') as mock_now:
            mock_now.return_value = dt.datetime(2023, 4, 1, 23, 0, 0)
            assert get_greeting() == "Доброй ночи"


@pytest.fixture
def sample_transactions():
    return pd.DataFrame({
        "Номер карты": ["*1112", "*5091"],
        "Сумма платежа": [-100, -200]
    })


def test_get_expenses_cards(sample_transactions):
    result = get_expenses_cards(sample_transactions)

    assert result[0] == {"last_digits": "*1112", "total spent": 100, "cashback": 1.0}
    assert result[1] == {"last_digits": "*5091", "total spent": 200, "cashback": 2.0}
