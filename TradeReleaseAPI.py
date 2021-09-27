import pyupbit
from TradeAPI import TradeAPI
import requests

class TradeReleaseAPI( TradeAPI ):
    def __init__(self):
        with open('upbit.txt') as f:
            lines = f.readlines()
            access = lines[0].strip()
            secret = lines[1].strip()
        self.upbit = pyupbit.Upbit(access, secret)

    def get_tickers(self, fiat):
        res = pyupbit.get_tickers(fiat)
        return res
    
    def get_current_price(self, ticker_list):
        res = pyupbit.get_current_price(ticker_list)
        return res
    
    def get_ohlcv(self, ticker, count=200, interval='day', to='20210922'):
        res = pyupbit.get_ohlcv(ticker, count=count, interval=interval, to=to )
        return res

    def get_orderbook(self, tickers):
        res = pyupbit.get_orderbook(tickers)
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
        res = self.upbit.sell_market_order(ticker, balance)
        return res

    def buy_market_order(self,ticker, balance):
        res = self.upbit.buy_market_order(ticker, balance)
        return res


