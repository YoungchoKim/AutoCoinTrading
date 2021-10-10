import time
import logging

class TimeControl:
    mode = 'debug'
    debug_day = ''
    debug_min = ''
    debug_min_list = []
    debug_min_list_len = 0
    debug_min_list_idx = 0
    @classmethod
    def set_mode(cls, mode):
        cls.mode = mode
    
    @classmethod
    def set_day(cls, day):
        cls.debug_day = day
    
    @classmethod
    def set_min(cls, minute):
        cls.debug_min = minute 

    @classmethod
    def set_min_list(cls, min_list):
        cls.debug_min_list = min_list
        cls.debug_min_list_len = len(cls.debug_min_list)
        print(cls.debug_min_list, len(cls.debug_min_list))
    
    @classmethod
    def get_day(cls):
        if cls.mode == 'release':
            now = time.localtime()
            day = '%04d%02d%02d' % (now.tm_year, now.tm_mon, now.tm_mday)
            return day

        elif cls.mode == 'debug':
            return cls.debug_day
    
    @classmethod
    def get_min(cls):
        if cls.mode == 'release':
            now = time.localtime()
            minute = '%04d%02d%02d %02d:%02d:00' % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)
            return minute
        elif cls.mode == 'debug':
            if cls.debug_min_list_len == cls.debug_min_list_idx:
                return cls.debug_min_list[cls.debug_min_list_idx-1]
            res = cls.debug_min_list[cls.debug_min_list_idx]
            cls.debug_min_list_idx += 1
            return res

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

