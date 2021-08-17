import pyupbit
import time
from collections import defaultdict
class TradeApi:
    def __init__(self, release):
        self.release = release
        if release == False:
            self.debug_file = open('price_file_date', 'r')
            self.debug_stream = self.debug_file.readlines()
            self.debug_cur_line = 1
            self.debug_max_line = len(self.debug_stream)
            self.debug_ticker_list = self.get_tickers('KRW')
            self.balance = 1000000

        else :
            f = open('upbit.txt')
            lines = f.readlines()
            access = lines[0].strip()
            secret = lines[1].strip()
            f.close()
            self.upbit = pyupbit.Upbit(access, secret)
        print('trade api init success. release({})'.format(self.release))

    def get_current_price(self, tickers):
        if self.release == True:
            time.sleep(1)
            return pyupbit.get_current_price(tickers)
        else:
            if self.debug_cur_line >= self.debug_max_line - 1:
                if self.debug_end == False:
                    print('debug end. balance : {}'.format(self.balance))
                self.debug_end = True
                return {}
            self.debug_end = False
            line = (self.debug_stream[self.debug_cur_line]).replace('\n','').split(',')
            self.cur_time = line[0]
            price_list = line[1:]
            self.debug_cur_line += 1
            price_dict = defaultdict(int)
            for idx in range(len(self.debug_ticker_list)):
                price_dict[self.debug_ticker_list[idx]] = price_list[idx]
            return price_dict

    def get_tickers(self, fiat):
        if self.release == True:
            return pyupbit.get_tickers(fiat)

        else :
            return (self.debug_stream[0]).replace('\n','').split(',')[1:-1]

    def get_cur_time(self):
        if self.release == True:
            now = time.localtime()
            return "%04d-%02d-%02d %02d:%02d:%02d," % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

        else :
            return self.cur_time

    def get_balance(self):
        if self.release == True:
            time.sleep(0.3)
            self.balance = self.upbit.get_balance("KRW")
        return self.balance


    def sell_market_order(self, ticker, cost, cnt):
        if self.release == True:
            time.sleep(0.3)
            balance = self.upbit.get_balance(ticker)
            self.upbit.sell_market_order(ticker, balance)
        else:
            self.balance += cost * cnt

    def buy_market_order(self, ticker, cost, cnt):
        if self.release == True:
            res = self.upbit.buy_market_order(ticker, cnt*cost)
            uuid = res['uuid']
            cnt = 0
            while True:
                sleep(1)
                cur_cost = pyupbit.get_current_price(ticker)
                if cur_cost < cost:
                    self.upbit.cancel_order(uuid)
                    print('buy market order is canceled. cur_cost{}, cost{}'.format(cur_cost, cost))
                    return 0,0
                balance = self.upbit.get_balance(ticker)
                if balance != 0:
                    return cur_cost, balance
                if cnt > 10:
                    self.upbit.cancel_order(uuid)
                    print('buy market order is canceled. cnt is 10')
                    return 0,0
                cnt+=1
            return 0,0

        else :
            self.balance -= cost * cnt
            return cost * cnt


