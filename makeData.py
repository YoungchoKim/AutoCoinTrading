#!/usr/bin/python
import pyupbit
from TimeControl import TimeControl
import time
import pandas as pd
import os
import logging

def make_minute1(ticker_list, init_date, count):
    df = {}
    N = len(ticker_list)
    remove_ticker_list = []
    for idx, ticker in enumerate(ticker_list):
        df[ticker] = []
        date = init_date
        for cnt in range(count, 0, -200):
            if cnt > 200:
                df[ticker].append(pyupbit.get_ohlcv(ticker, count=200, interval='minute1', to=date))
            else:
                df[ticker].append(pyupbit.get_ohlcv(ticker, count=cnt, interval='minute1', to=date))
            if len(df[ticker][-1]) == 0:
                remove_ticker_list.append(ticker)
                logging.info('remove ticker(minute): {}'.format(ticker))
                break
            date = df[ticker][-1].index[0]
            time.sleep(0.1)
        logging.info('Please wait a minute(minute). {}/{}'.format(idx+1, N))
        df[ticker] = pd.concat(df[ticker])
        df[ticker] = df[ticker].sort_index()
        df[ticker].to_csv('debug/min1-{}.csv'.format(ticker))
    return remove_ticker_list

def make_day(ticker_list, init_date, count):
    df = {}
    N = len(ticker_list)
    remove_ticker_list = []
    for idx, ticker in enumerate(ticker_list):
        df[ticker] = []
        date = init_date
        for cnt in range(count, 0, -200):
            if cnt > 200:
                df[ticker].append(pyupbit.get_ohlcv(ticker, count=200, interval='day', to=date))
            else:
                df[ticker].append(pyupbit.get_ohlcv(ticker, count=cnt, interval='day', to=date))
            if len(df[ticker][-1]) == 0:
                remove_ticker_list.append(ticker)
                logging.info('remove ticker(minute): {}'.format(ticker))
                break
            date = df[ticker][-1].index[0]
            time.sleep(0.1)
        logging.info('Please wait a minute(day). {}/{}'.format(idx+1, N))
        df[ticker] = pd.concat(df[ticker])
        df[ticker] = df[ticker].sort_index()
        df[ticker].to_csv('debug/day-{}.csv'.format(ticker))
    return remove_ticker_list
        

if __name__ == '__main__':
    if not os.path.isdir('debug'):
        os.mkdir('debug')

    ticker_list = pyupbit.get_tickers('KRW')
    day_count = 200
    min_count = day_count * 60 * 24
    
    TimeControl.set_mode('release')
    day_now = TimeControl.get_day()
    min_now = TimeControl.get_min()
    
    remove_ticker_list = []
    res = make_minute1(ticker_list, min_now, min_count+200)
    if len(res) != 0:
        remove_ticker_list += res
    res = make_day(ticker_list, day_now, day_count+200)
    if len(res) != 0:
        remove_ticker_list += res

    if len(remove_ticker_list) != 0:
        ticker_list = list(set(ticker_list) - set(remove_ticker_list))

    with open('debug/ticker_list', mode='w') as f:
        f.write(','.join(ticker_list))
        f.write('\n')
        f.write(','.join(list(set(remove_ticker_list))))

    
    


