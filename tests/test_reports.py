from unittest.mock import mock_open, patch

import pandas as pd

from src.reports import spending_by_category


def test_spending_by_category(samp_transactions: pd.DataFrame) -> None:
    df_transactions = pd.DataFrame(samp_transactions)
    current_datetime = "20.04.2023 12:00:00"
    category = "Еда"

    mock_open_func = mock_open()

    with patch("builtins.open", mock_open_func):
        result = spending_by_category(df_transactions, category, current_datetime).to_dict(orient="records")

    expected_result = [
        {"Дата операции": "10.03.2023 12:00:00", "Категория": "Еда", "Сумма": 200},
        {"Дата операции": "20.04.2023 12:00:00", "Категория": "Еда", "Сумма": 300},
    ]
    assert result == expected_result

    mock_open_func.assert_called_once_with("../logs/log_file.json", "w", encoding="utf-8")
