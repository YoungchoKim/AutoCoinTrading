import pyupbit
from quotationApi import QuotationApi
import requests

class QuotationRelApi( QuotationApi ):
    def __init__(self):
        pass

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

