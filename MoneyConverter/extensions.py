import requests
import json
from MoneyConverter.config import keys

class ConvertionException(Exception):
    pass

class MoneyConverter():
    @staticmethod
    def convert(quote: str, base: str, amount: str):

        if quote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}')

        try:
            quote_tiker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать вылюту {quote}')

        try:
            base_tiker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать вылюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать колличество {base}')

        req = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_tiker}&tsyms={base_tiker}')
        total_base =float(json.loads(req.content)[keys[base]]) * float(amount)
        return round(total_base, 2)