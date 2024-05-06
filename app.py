

# Formato de resposta
# https://economia.awesomeapi.com.br/:format/:moeda
''''
Exemplos
    http://economia.awesomeapi.com.br/json/last/USD-BRL
    http://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL,BTC-BRL

    http://economia.awesomeapi.com.br/xml/USD-BRL/1
    http://economia.awesomeapi.com.br/USD-BRL/1?format=xml
'''
from abc import ABC
import requests
from datetime import date, datetime
import json


class Moeda():
    url_base = 'http://economia.awesomeapi.com.br/json'

    def __init__(self, coin) -> None:
        self.coin = coin

    def get_endpoint(self) -> str:
        return f'{self.url_base}/{self.coin}'

    def get_data(self):
        return requests.get(self.get_endpoint()).json()

    def save_data(self):
        with open(f'{self.__class__.__name__}_{datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.json', 'w') as file:
            json.dump(self.get_data(), file, indent=4)


class Last(Moeda):
    # Retorna moedas selecionadas (atualizado a cada 30 segundos)
    # Moedas selecionadas separado por vírgula (,) Ex.: USD-BRL,EUR-BRL,BTC-BRL
    # https://economia.awesomeapi.com.br/json/last/:moedas
    def __init__(self, coin: list) -> None:
        super().__init__(coin)

    def get_endpoint(self) -> str:
        return f'{self.url_base}/last/{self.coin}'


class LastDays(Moeda):
    # Retorna o fechamento dos últimos dias
    # https://economia.awesomeapi.com.br/json/daily/:moeda/:numero_dias

    def __init__(self, coin, number_of_days) -> None:
        super().__init__(coin)
        self.number_of_days = number_of_days

    def get_endpoint(self) -> str:
        return f'{self.url_base}/daily/{self.coin}/{self.number_of_days}'

    def get_data(self):
        return super().get_data()


class Quantity(Moeda):
    # Retorna cotações sequenciais de uma única moeda
    # https://economia.awesomeapi.com.br/:moeda/:quantidade
    url_base = 'http://economia.awesomeapi.com.br'

    def __init__(self, coin, len) -> None:
        super().__init__(coin)
        self.len = len

    def get_endpoint(self) -> str:
        return f"{self.url_base}/{self.coin}/{self.len}"


class Period(Moeda):
    # Retorna o fechamento de um período específico
    # https://economia.awesomeapi.com.br/json/daily/:moeda?start_date=20180901&end_date=20180930
    def __init__(self, coin, start_date: datetime, end_date: datetime) -> None:
        super().__init__(coin)
        self.sd = start_date
        self.ed = end_date

    def get_endpoint(self) -> str:
        return f"{self.url_base}/daily/{self.coin}?start_date={self.sd}&end_date={self.ed}"


class Sequence(Period):
    # Retorna cotações sequenciais de um período específico
    # https://economia.awesomeapi.com.br/:moeda/:quantidade?start_date=20200301&end_date=20200330

    def __init__(self, coin, quantity, start_date: datetime, end_date: datetime) -> None:
        super().__init__(coin, start_date, end_date)
        self.quantity = quantity

    def get_endpoint(self) -> str:
        return f"{self.url_base}/{self.coin}/{self.quantity}?start_date={self.sd}&end_date={self.ed}"


t = Sequence('USD-BRL', 10, '20240410', '20240502')
print(t.get_data())
t.save_data()
