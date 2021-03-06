from TradeAlgorithm import TradeAlgorithm
from Coin import Coin
from PriceInfo import PriceInfo
from TradeTicket import TradeTicket
import State
import time 
from TimeControl import TimeControl
import logging

class YunjooAlgo(TradeAlgorithm):
    def __init__(self, mode, pInfo,queue):
        logging.info('init yunjoo algorithm. mode:{}'.format(mode))
        self.queue = queue
        self.pInfo = pInfo
        self.filter_ticker_list()

    def filter_ticker_list(self):
        self.ticker_list = []
        cur_price_dict = self.pInfo.get_current_price()
        for k,v in cur_price_dict.items():
            if v >= 300:
                self.ticker_list.append(k)
        self.pInfo.set_tickers(self.ticker_list)
        logging.info('ticker list:{}, len:{}'.format(self.ticker_list, len(self.ticker_list)))

    def check_buy_coin(self, df_day, df_min1, ticker, ticket_list):
        success = True
        if len(df_day) < 25:
            return

        before25 = df_day.iloc[0, 3]
        before5 = df_day.iloc[19, 3]
        current = df_min1.iloc[0, 3]
        if before25 * 0.8 < before5:
            #print(ticker, 'expensive fail')
            return
        
        for idx in range(20,25):
            bebefore = df_day.iloc[idx-1, 3]
            before = df_day.iloc[idx, 3]
            if bebefore > before:
                success = False
                break
        if success == False:
            #print(ticker, 'continuos 5days fail')
            return
        
        if current > (before25 + before5)/2:
            #print(ticker, 'current cost is fail')
            return

        coin = Coin(ticker, 0, 0, State.get_waitBuy(), None)
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
            df_min1 = self.ohlcv['min1'][ticker]
            if 'error' in df_day or 'error' in df_min1:
                logging.info(df_day['error'])
                continue
            df_day = df_day.tail(25)
            df_min1 = df_day.tail(1)
            if ticker not in [coin.get_ticker() for coin in have_coin_list]:
                self.check_buy_coin(df_day, df_min1, ticker, ticket_list)
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
