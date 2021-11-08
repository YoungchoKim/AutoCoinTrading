import pyupbit
from quotationApi import QuotationApi
from TimeControl import TimeControl
import pandas as pd
import requests
import logging

class QuotationDebugApi( QuotationApi ):

    def __init__(self):
        with open('debug/ticker_list') as f:
            lines = f.readlines()
            self.ticker_list = lines[0].strip().split(',')
        self.df = {}
        self.df['day'] = {}
        self.df['min1'] = {}
        
        for ticker in self.ticker_list:
            self.df['day'][ticker] = pd.read_csv('debug/day-{}.csv'.format(ticker), index_col=[0])
        for ticker in self.ticker_list:
            self.df['min1'][ticker] = pd.read_csv('debug/min1-{}.csv'.format(ticker), index_col=[0])

        self.max_len = len(self.df['min1']['KRW-BTC'])
        print('max_len : ', self.max_len)
        self.min1 = self.df['min1']['KRW-BTC'].index[200]
        self.day = self.df['day']['KRW-BTC'].index[200]
        self.day_idx = 200

    def get_tickers(self, fiat):
        return self.ticker_list
    
    def get_current_price(self, ticker_list):
        res = {}
        debug_idx = TimeControl.get_debug_idx()
        for ticker in ticker_list:
            res[ticker] = self.df['min1'][ticker].iloc[debug_idx, 3]
        return res
    
    def get_ohlcv(self, ticker, count=200, interval='day', to='20210922'):
        debug_idx = TimeControl.get_debug_idx()
        if interval == 'day':
            res = self.df['day'][ticker][self.day_idx-200:self.day_idx]
            if self.day != to:
                self.day = to
                self.day_idx += 1
        elif interval == 'minute1':
            res = self.df['min1'][ticker][debug_idx-200:debug_idx]

        return res
    
    def get_orderbook(self, tickers):
        res = pyupbit.get_orderbook(tickers)
        return res


if __name__ == '__main__':
    print(dApi.ticker_list)
    print(dApi.df['min1']['KRW-BTC'].index)
        
        
