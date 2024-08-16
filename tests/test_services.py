import json
import unittest

import pandas as pd

from src.services import transfers_to_individuals


class TestTransfersToIndividuals(unittest.TestCase):

    def test_transfers_to_individuals(self) -> None:
        data = {
            "Категория": ["Переводы", "Переводы", "Расходы"],
            "Описание": ["Перевод Ивану И.", "Перевод Петрову П.", "Оплата услуг"],
        }
        transactions = pd.DataFrame(data)

        expected_output = json.dumps(
            [
                {"Категория": "Переводы", "Описание": "Перевод Ивану И."},
                {"Категория": "Переводы", "Описание": "Перевод Петрову П."},
            ],
            ensure_ascii=False,
            indent=4,
        )

        result = transfers_to_individuals(transactions)
        self.assertEqual(result, expected_output)
