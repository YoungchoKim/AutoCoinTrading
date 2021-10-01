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

    def check_buy_coin(self, df, ticker, ticket_list):
        success = True

        before25 = df.iloc[0, 3]
        before5 = df.iloc[19, 3]
        before1 = df.iloc[24, 3]
        if before25 * 0.8 < before5:
            return
        
        for idx in range(20,25):
            before = df.iloc[idx-1, 3]
            current = df.iloc[idx, 3]
            if before > current:
                success = False
                break
        if success == False:
            return
        
        if before1 > (before25 + before5)/2:
            return

        coin = Coin(ticker, 0, 0, State.get_waitBuy())
        ticket_list.append(TradeTicket('buy', 'market', 0, coin))

    def check_sell_coin(self, df, ticker, ticket_list, have_coin_list):
        limit_cost = df.iloc[24,3] * 1.05
        for coin in have_coin_list:
            if coin.get_ticker() == ticker and coin.get_state() == State.get_bought():
                coin.set_state(State.get_waitSell())
                ticket_list.append(TradeTicket('sell','limit',limit_cost,coin))
                break

    def get_tradeTicket_list(self, have_coin_list):
        self.ohlcv = self.queue.get()
        ticket_list = []
        for ticker in self.ticker_list:
            df = self.ohlcv['day'][ticker]
            if 'error' in df:
                logging.info(df['error'])
                continue
            df = df.tail(25)
            if ticker not in [coin.get_ticker() for coin in have_coin_list]:
                self.check_buy_coin(df, ticker, ticket_list)
            else:
                self.check_sell_coin(df, ticker, ticket_list, have_coin_list)
        if len(ticket_list) != 0:    
            logging.info(ticket_list)
        return ticket_list

if __name__=='__main__':
    yj = YunjooAlgo('release')
    while True:
        tradeTicket_list = yj.get_tradeTicket_list()
        
        time.sleep(TimeControl.get_sleep_time()['while'])
