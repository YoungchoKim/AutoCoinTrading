import time
import logging
import pandas as pd
import numpy as np
from multiprocessing import shared_memory, Semaphore
class TimeControl:
    mode = 'debug'

    @classmethod
    def init(cls, shm_name, sem):
        if cls.mode == 'debug':
            cls.price_info_init()
            cls.shm_name = shm_name
            cls.sem = sem
    
    @classmethod
    def price_info_init(cls):
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
        print('TimeControl price_info_init success')

    @classmethod
    def set_mode(cls, mode):
        cls.mode = mode
    
    @classmethod
    def get_day(cls):
        if cls.mode == 'release':
            now = time.localtime()
            day = '%04d%02d%02d' % (now.tm_year, now.tm_mon, now.tm_mday)
            return day

        elif cls.mode == 'debug':
            idx = cls.get_debug_idx()
            return cls.df['day']['KRW-BTC'].index[idx]
    
    @classmethod
    def get_min(cls):
        if cls.mode == 'release':
            now = time.localtime()
            minute = '%04d%02d%02d %02d:%02d:00' % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)
            return minute
        elif cls.mode == 'debug':
            idx = cls.get_debug_idx()
            return cls.df['min1']['KRW-BTC'].index[idx]

    @classmethod
    def get_sleep_time(cls):
        sleep_time = {}
        if cls.mode == 'release':
            sleep_time['while'] = 1
            sleep_time['ohlcv'] = 0.05
            sleep_time['account'] = 0.2
        elif cls.mode == 'debug':
            sleep_time['while'] = 0
            sleep_time['ohlcv'] = 0
            sleep_time['account'] = 0

        return sleep_time

    @classmethod
    def get_debug_idx(cls):
        cls.sem.acquire()
        new_shm = shared_memory.SharedMemory(name=cls.shm_name)
        tmp_arr = np.ndarray((1,1), dtype='u8', buffer=new_shm.buf)
        ret = int(tmp_arr[0])
        cls.sem.release()
        return ret
    
    @classmethod
    def is_debug_end(cls):
        idx = cls.get_debug_idx()
        if idx == cls.max_len-1:
            return True
        return False

    @classmethod
    def get_debug_max_len(cls):
        return cls.max_len
