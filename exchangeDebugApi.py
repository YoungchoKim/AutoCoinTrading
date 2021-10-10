import pyupbit
from exchangeApi import ExchangeApi
from TimeControl import TimeControl
import pandas as pd
import requests
import logging

class ExchangeDebugApi( ExchangeApi ):

    @classmethod
    def init(cls):
        cls.balance = 100000
        # (ticker, cost, count)
        cls.have_dict = {}
        cls.buy_dict = {}
        cls.sell_dict = {}

    @classmethod
    def check_sell_dict(cls):
        if len(cls.sell_dict) == 0:
            return
        success_ticker = []
        for ticker, value in cls.sell_dict.items():
            cost, count = value
            high = cls.df['min1'][ticker].iloc[cls.min_idx, 1]
            low = cls.df['min1'][ticker].iloc[cls.min_idx, 2]
            if cost <= high:
                cls.balance += cost * count
                success_ticker.append(ticker)
        for ticker in success_ticker:
            cls.sell_dict.pop(ticker)
            cls.have_dict.pop(ticker)
    @classmethod
    def check_buy_dict(cls):
        if len(cls.buy_dict) == 0:
            return
        success_ticker = []
        for ticker, value in cls.buy_dict.items():
            cost, count = value
            high = cls.df['min1'][ticker].iloc[cls.min_idx, 1]
            low = cls.df['min1'][ticker].iloc[cls.min_idx, 2]
            if cost >= low :
                cls.balance -= cost * count
                success_ticker.append(ticker)
                cls.have_dict[ticker] = (cost, count)
        for ticker in success_ticker:
            cls.buy_dict.pop(ticker)
    
    def get_order(cls, ticker, state='wait'):
        pass
    
    @classmethod
    def get_balance(cls, ticker):
        res = cls.upbit.get_balance(ticker)
        return res
    
    @classmethod
    def get_balances(cls):
        res = []
        item = {'currency':'KRW','balance':cls.balance,'avg_buy_price':0}
        res.append(item)
        for k, v in cls.have_dict.items():
            cost, cnt = v
            item = {'currency':k[4:], 'balance':cnt, 'avg_buy_price':cost}
            res.append(item)
        return res

    @classmethod
    def sell_limit_order(cls,ticker, cost, count):
        cls.sell_dict[ticker]  = (cost, count)
        return {'uuid':ticker}

    @classmethod
    def buy_limit_order(cls,ticker, cost, count):
        cls.buy_dict[ticker] = (cost, count)
        return cls.buy_dict

    @classmethod
    def sell_market_order(cls,ticker, count):
        cost = cls.df['min1'][ticker].iloc[cls.min_idx, 3]
        have_dict.pop(ticker)
        cls.balance += cost * count
        return cls.balance

    @classmethod
    def buy_market_order(cls,ticker, balance):
        cost = cls.df['min1'][ticker].iloc[cls.min_idx, 3]
        count = balance / cost
        cls.have_dict[ticker] = (cost, count)
        cls.balance -= cost * count
        return cls.have_dict

    @classmethod
    def cancel_order(cls, uuid):
        del cls.sell_dict[uuid]
        return uuid

if __name__ == '__main__':
    print(dApi.ticker_list)
    print(dApi.df['min1']['KRW-BTC'].index)
        
        
