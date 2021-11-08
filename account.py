from collections import defaultdict
from exchangeRelApi import ExchangeRelApi
from exchangeDebugApi import ExchangeDebugApi
from Coin import Coin
from TimeControl import TimeControl
import time
import State, priceQuotation
import logging
class Account:

    def __init__(self, mode):
        if mode == 'release':
            self.tApi = ExchangeRelApi()
        elif mode == 'debug' :
            ExchangeDebugApi.init()
            self.tApi = ExchangeDebugApi
        self.having_list = self.tApi.get_balances()
        for item in self.having_list:
            if item['currency'] == 'KRW':
                self.myMoney = float(item['balance'])
                break
        self.ratio = 0.1
        logging.info('my initial ratio : {}'.format(self.ratio))
        logging.info('my money : {}'.format(self.myMoney))
        logging.info('Account init success. mode: '.format(mode))

    def set_ratio(self, ratio):
        self.ratio = ratio

    def get_have_coin_list(self):
        res = self.tApi.get_balances()
        coin_list = []
        for item in res:
            if item['currency'] == 'KRW':
                self.myMoney = float(item['balance'])
                continue
            ticker = 'KRW-{}'.format(item['currency'])
            cost = float(item['avg_buy_price'])
            count = float(item['balance'])
            state = State.get_bought()
            coin_list.append(Coin(ticker,cost,count,state,None))
        return coin_list

    def request_order(self, ticket_list):
        for ticket in ticket_list:
            time.sleep(TimeControl.get_sleep_time()['account'])
            if ticket.get_order() == 'buy':
                if ticket.get_order_type() == 'market':
                    balance = priceQuotation.get_price(self.myMoney * self.ratio)
                    res = self.tApi.buy_market_order(ticket.get_coin().get_ticker(), balance)
                    if 'error' in res:
                        logging.info(res)
                        continue

                elif ticket.get_order_type() == 'limit':
                    pass

            elif ticket.get_order() == 'sell':
                if ticket.get_order_type() == 'market':
                    count = ticket.get_coin().get_count()
                    res = self.tApi.sell_market_order(ticket.get_coin().get_ticker(), count)
                    if 'error' in res:
                        logging.info(res)
                        continue

                elif ticket.get_order_type() == 'limit':
                    #print('sell',ticker)
                    count = ticket.get_coin().get_count()
                    limit_cost = priceQuotation.get_price(ticket.get_limit_cost())
                    res = self.tApi.sell_limit_order(ticket.get_coin().get_ticker(),limit_cost, count)
                    if 'error' in res:
                        logging.info(res)
                        continue
                    ticket.get_coin().set_uuid(res['uuid'])

                elif ticket.get_order_type() == 'cancel':
                    uuid = ticket.get_coin().get_uuid()
                    res = self.tApi.cancel_order(uuid)
                    if 'error' in res:
                        logging.info(res)
                        continue
                    ticket.get_coin().set_uuid(None)

    def print_total(self):
        self.tApi.print_total()

