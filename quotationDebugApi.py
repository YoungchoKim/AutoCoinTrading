import pyupbit
from quotationApi import QuotationApi
from TimeControl import TimeControl
import pandas as pd
import requests
import logging

class QuotationDebugApi( QuotationApi ):

    @classmethod
    def init(cls):
        with open('debug/ticker_list') as f:
            lines = f.readlines()
            cls.ticker_list = lines[0].strip().split(',')
        cls.df = {}
        cls.df['day'] = {}
        cls.df['min1'] = {}
        
        for ticker in cls.ticker_list:
            cls.df['day'][ticker] = pd.read_csv('debug/day-{}.csv'.format(ticker), index_col=[0])
        for ticker in cls.ticker_list:
            cls.df['min1'][ticker] = pd.read_csv('debug/min1-{}.csv'.format(ticker), index_col=[0])

        cls.max_len = len(cls.df['min1']['KRW-BTC'])
        print('max_len : ', cls.max_len)
        cls.min1 = cls.df['min1']['KRW-BTC'].index[200]
        cls.day = cls.df['day']['KRW-BTC'].index[200]
        cls.min_idx = 200
        cls.day_idx = 200
        TimeControl.set_min(cls.min1)
        TimeControl.set_day(cls.day)
        TimeControl.set_min_list(cls.df['min1']['KRW-BTC'].index[201:])

    @classmethod
    def get_tickers(cls, fiat):
        return cls.ticker_list
    
    @classmethod
    def get_current_price(cls, ticker_list):
        res = {}
        for ticker in ticker_list:
            res[ticker] = cls.df['min1'][ticker].iloc[cls.min_idx, 3]
        return res
    
    @classmethod
    def get_ohlcv(cls, ticker, count=200, interval='day', to='20210922'):
        if interval == 'day':
            res = cls.df['day'][ticker][cls.day_idx-200:cls.day_idx]
            if cls.day != to:
                cls.day = to
                cls.day_idx += 1
        elif interval == 'minute1':
            res = cls.df['min1'][ticker][cls.min_idx-200:cls.min_idx]
            if cls.min1 != to:
                cls.min1 = to
                cls.min_idx += 1

            if cls.min_idx >= cls.max_len-1:
                print('balance: {}'.format(cls.balance))
                for tick,value in cls.have_dict.items():
                    cost, cnt = value
                    print(tick, ' cost: {}, count: {}'.format(cost, cnt))
                    cls.balance += cnt * cls.df['min1'][tick].iloc[-1, 3]
                print('total: {}'.format(cls.balance))
                quit()


        return res
    
    @classmethod
    def get_orderbook(cls, tickers):
        res = pyupbit.get_orderbook(tickers)
        return res


if __name__ == '__main__':
    print(dApi.ticker_list)
    print(dApi.df['min1']['KRW-BTC'].index)
        
        
