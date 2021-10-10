import threading
import time 
from TimeControl import TimeControl


class PriceInfo(threading.Thread) :
    _instance = None

    def __init__(self, quotationApi, queue):
        super(PriceInfo, self).__init__()
        self.quotationApi = quotationApi
        self.queue = queue
        self.ticker_list = self.quotationApi.get_tickers('KRW')
        self.cur_price_dict = self.quotationApi.get_current_price(self.ticker_list)
        self.sleep_time = TimeControl.get_sleep_time()
        
        self.date = TimeControl.get_min()
        
        self.ohlcv = {}
        self.init_ohlcv()
        self.queue.put(self.ohlcv)
    
    @classmethod
    def get_instance(cls, TradeApi, queue):
        if not cls._instance:
            cls._instance = PriceInfo(TradeApi, queue)
        return cls._instance

    def get_tickers(self):
        return self.ticker_list

    def set_tickers(self, ticker_list):
        self.ticker_list = ticker_list

    def init_ohlcv(self):
        self.ohlcv['day'] = {}
        for ticker in self.ticker_list:
            self.ohlcv['day'][ticker] = self.quotationApi.get_ohlcv(ticker, 200, 'day', self.date)
            time.sleep(self.sleep_time['ohlcv'])

        self.ohlcv['min1'] = {}
        for ticker in self.ticker_list:
            self.ohlcv['min1'][ticker] = self.quotationApi.get_ohlcv(ticker, 200, 'minute1', self.date)
            time.sleep(self.sleep_time['ohlcv'])
    
    def get_current_price(self):
        return self.cur_price_dict

    def run(self):
        while(True):
            time.sleep(self.sleep_time['while'])
            minute = TimeControl.get_min()
            if minute[-8:] == '10:00:00':
                for ticker in self.ticker_list:
                    res = self.quotationApi.get_ohlcv(ticker, 200, 'day', minute)
                    self.ohlcv['day'][ticker] = res
                    time.sleep(self.sleep_time['ohlcv'])
                self.queue.put(self.ohlcv)
                    

            if self.date != minute:
                self.date = minute
                for ticker in self.ticker_list:
                    res = self.quotationApi.get_ohlcv(ticker, 200, 'minute1', self.date)
                    #TODO: if get ohlcv is failed... do not put in queue
                    self.ohlcv['min1'][ticker] = res
                    time.sleep(self.sleep_time['ohlcv'])
                self.queue.put(self.ohlcv)


