from PriceInfo import PriceInfo
from TradeReleaseAPI import TradeReleaseAPI
from TradeDebugAPI import TradeDebugAPI
from TradeAlgorithm import TradeAlgorithm
from queue import Queue
from Coin import Coin
from TradeTicket import TradeTicket
import State
import time 
from TimeControl import TimeControl
import logging

class YunjooAlgo(TradeAlgorithm):
    def __init__(self, mode):
        logging.info('init yunjoo algorithm. mode:{}'.format(mode))
        self.queue = Queue()
        if mode == 'release':
            self.pInfo = PriceInfo(TradeReleaseAPI(), self.queue)
        else:
            self.pInfo = PriceInfo(TradeDebugAPI, self.queue)
        self.filter_ticker_list()

        self.pInfo.daemon = True
        self.pInfo.start()

    def filter_ticker_list(self):
        self.ticker_list = []
        cur_price_dict = self.pInfo.get_current_price()
        for k,v in cur_price_dict.items():
            if v >= 300:
                self.ticker_list.append(k)
        self.pInfo.set_tickers(self.ticker_list)
        logging.info('ticker list:{}, len:{}'.format(self.ticker_list, len(self.ticker_list)))

    def check_buy_coin(self, df_day, df_min, ticker, ticket_list):
        success = True

        before25 = df_day.iloc[0, 3]
        before5 = df_day.iloc[19, 3]
        current = df_min.iloc[0, 3]
        if before25 * 0.8 < before5:
            return
        
        for idx in range(20,25):
            before = df_day.iloc[idx-1, 3]
            current = df_day.iloc[idx, 3]
            if before > current:
                success = False
                break
        if success == False:
            return
        
        if current > (before25 + before5)/2:
            return

        coin = Coin(ticker, 0, 0, State.get_waitBuy())
        ticket_list.append(TradeTicket('buy', 'market', 0, coin))

    def check_sell_coin(self, ticker, ticket_list, have_coin_list):
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
            df_min = self.ohlcv['min'][ticker]
            if 'error' in df_day or 'error' in df_min:
                logging.info(df_day['error'])
                continue
            df_day = df_day.tail(25)
            df_min = df_day.tail(1)
            if ticker not in [coin.get_ticker() for coin in have_coin_list]:
                self.check_buy_coin(df_day, df_min, ticker, ticket_list)
            else:
                self.check_sell_coin(ticker, ticket_list, have_coin_list)
        if len(ticket_list) != 0:    
            logging.info(ticket_list)
        return ticket_list

if __name__=='__main__':
    yj = YunjooAlgo('release')
    while True:
        tradeTicket_list = yj.get_tradeTicket_list()
        
        time.sleep(TimeControl.get_sleep_time()['while'])
