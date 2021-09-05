import tradeapi
import time
from collections import defaultdict,deque
import logging
class Coin:
    def __init__(self, trade):
        self.trade = trade # tradeapi.TradeApi(release)
        self.ticker_list = self.trade.get_tickers(fiat='KRW')
        self.price_dict = defaultdict(int)
        self.target_time = 10
        self.min_max_time = 600
        self.price_dict_cnt = defaultdict(int)
        self.price_list_dict = defaultdict(deque)
        self.min_dict = defaultdict(lambda : 10000000000) 
        self.max_dict = defaultdict(int)
        self.target_list_dict = defaultdict(deque)
        logging.info('ticker_list: {}'.format(self.ticker_list))
        price = self.trade.get_current_price(self.ticker_list)
        logging.info('price: {}'.format(price.keys()))
        self.ticker_list = list(price.keys())
        time.sleep(1)
        for i in range(self.min_max_time):
            price = self.trade.get_current_price(self.ticker_list)
            for ticker in self.ticker_list:
                if ticker not in price.keys():
                    logging.info('ticker not in price keys. ticker: {}'.format(ticker))
                    continue
                cost = float(price[ticker])
                self.price_dict_cnt[(ticker, cost)] += 1
                self.price_list_dict[ticker].append(cost)
                self.min_dict[ticker] = min(self.min_dict[ticker], cost)
                self.max_dict[ticker] = max(self.max_dict[ticker], cost)

        for i in range(self.target_time):
            price = self.trade.get_current_price(self.ticker_list)
            for ticker in self.ticker_list:
                if ticker not in price.keys():
                    continue
                cost = float(price[ticker])
                self.target_list_dict[ticker].append(cost)
        logging.info('coin init success') 
    def get_latest_price(self, ticker):
        sum_cost = 0
        for cost in self.target_list_dict[ticker]:
            sum_cost += cost
        return sum_cost / self.target_time

    def check_cur_state(self, bought_dict): # bought_list -> (key: ticker, value: [cost, count])
        buy_list = [] 
        sell_list = []
        date = self.trade.get_cur_time()
        price = self.trade.get_current_price(self.ticker_list)
        if price == {}:
            return date, buy_list, sell_list
        for ticker in self.ticker_list:
                 
            cost = self.price_list_dict[ticker].popleft()
            self.price_dict_cnt[(ticker, cost)] -= 1
            if self.price_dict_cnt[(ticker, cost)] == 0 and (self.min_dict[ticker] == cost or self.max_dict[ticker] == cost):
                self.min_dict[ticker] = 10000000000
                self.max_dict[ticker] = 0
                for dict_cost in self.price_list_dict[ticker]:
                    self.min_dict[ticker] = min(self.min_dict[ticker], dict_cost)
                    self.max_dict[ticker] = max(self.max_dict[ticker], dict_cost)
            cost = self.target_list_dict[ticker].popleft()
            self.price_list_dict[ticker].append(cost)
            self.price_dict_cnt[(ticker, cost)] += 1
            self.min_dict[ticker] = min(self.min_dict[ticker], cost)
            self.max_dict[ticker] = max(self.max_dict[ticker], cost)
            
            cost = float(price[ticker])
            self.target_list_dict[ticker].append(cost)
            latest_price = self.get_latest_price(ticker)

            if ticker in bought_dict:
                if len(bought_dict[ticker]) == 0:
                    continue
                bought_cost,cnt,uuid = bought_dict[ticker]
                if cost <= (self.min_dict[ticker] + self.max_dict[ticker])/2:
                    sell_list.append((ticker, cost))
                continue

            if latest_price > self.max_dict[ticker] *1.01 :
                buy_list.append((ticker, latest_price))
        return date, buy_list, sell_list



