import pyupbit
from TradeAPI import TradeAPI
from TimeControl import TimeControl
import pandas as pd
import requests

class TradeDebugAPI( TradeAPI ):

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
            cls.check_sell_dict()
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
        return cls.sell_dict

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

if __name__ == '__main__':
    dApi = TradeDebugAPI()
    print(dApi.ticker_list)
    print(dApi.df['min1']['KRW-BTC'].index)
        
        
