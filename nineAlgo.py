from PriceInfo import PriceInfo
from TradeAlgorithm import TradeAlgorithm
from TimeControl import TimeControl
from Coin import Coin
from TradeTicket import TradeTicket
import State
import time 
import logging

class NineAlgo(TradeAlgorithm):
    def __init__(self, mode, pInfo, queue):
        logging.info('init nine algorithm. mode:{}'.format(mode))
        self.ticker_list = pInfo.get_tickers()
        self.queue = queue

    def check_buy_coin(self, df_day, df_min1, ticker, ticket_list):
        minute = TimeControl.get_min()
        if minute[-8:] > '09:35:00' or minute[-8:] < '08:45:00':
            return None
        if minute[-8:] == '08:45:00':
            before = df_day.iloc[0, 3]
            current = df_min1.iloc[0, 3]
            if before > current:
                return None
            coin = Coin(ticker, 0, 0, State.get_waitBuy(), None)
            ticket_list.append(TradeTicket('buy', 'market', 0, coin))
            print(minute)

    def check_sell_coin(self, ticker, ticket_list, have_coin_list):
        minute = TimeControl.get_min()
        if minute[-8:] == '09:34:00':
            for coin in have_coin_list:
                if coin.get_ticker() == ticker and coin.get_uuid() != None:
                    ticket_list.append(TradeTicket('sell', 'cancel', 0, coin))
                    break
            return None
        if minute[-8:] == '09:35:00':
            for coin in have_coin_list:
                if coin.get_ticker() == ticker and coin.get_uuid() == None:
                    ticket_list.append(TradeTicket('sell', 'market', 0, coin))
                    break
            return None
        if minute[-8:] > '09:35:00':
            return None

        for coin in have_coin_list:
            if coin.get_ticker() == ticker and coin.get_state() == State.get_bought():
                limit_cost = coin.get_cost() * 1.05
                coin.set_state(State.get_waitSell())
                ticket_list.append(TradeTicket('sell','limit',limit_cost,coin))
                break

    def get_tradeTicket_list(self, have_coin_list):
        self.ohlcv = self.queue.get()
        ticket_list = []
        for ticker in self.ticker_list:
            df_day = self.ohlcv['day'][ticker]
            df_min1 = self.ohlcv['min1'][ticker]
            if 'error' in df_day:
                logging.info(df_day['error'])
                continue
            if 'error' in df_min1:
                logging.info(df_min1['error'])
                continue
            df_day = df_day.tail(1)
            df_min1 = df_day.tail(1)
            if ticker not in [coin.get_ticker() for coin in have_coin_list]:
                self.check_buy_coin(df_day, df_min1, ticker, ticket_list)
            else:
                self.check_sell_coin(ticker, ticket_list, have_coin_list)
        if len(ticket_list) != 0:    
            logging.info(ticket_list)
        return ticket_list

