import pyupbit
from exchangeApi import ExchangeApi
import requests

class ExchangeRelApi( ExchangeApi ):
    def __init__(self):
        with open('upbit.txt') as f:
            lines = f.readlines()
            access = lines[0].strip()
            secret = lines[1].strip()
        self.upbit = pyupbit.Upbit(access, secret)

    def get_order(self, ticker, state = 'wait'):
        res = self.upbit.get_order(ticker, state)
        return res

    def get_balance(self, ticker):
        res = self.upbit.get_balance(ticker)
        return res
    
    def get_balances(self):
        res = self.upbit.get_balances()
        return res

    def sell_limit_order(self,ticker, cost, count):
        res = self.upbit.sell_limit_order(ticker, cost, count)
        return res

    def buy_limit_order(self,ticker, cost, count):
        res = self.upbit.buy_limit_order(ticker, cost, count)
        return res

    def sell_market_order(self,ticker, count):
        res = self.upbit.sell_market_order(ticker, count)
        return res

    def buy_market_order(self,ticker, balance):
        res = self.upbit.buy_market_order(ticker, balance)
        return res

    def cancel_order(self, uuid):
        res = self.upbit.cancel_order(uuid)
        return res

