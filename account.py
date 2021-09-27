from collections import defaultdict
from TradeReleaseAPI import TradeReleaseAPI
from TradeDebugAPI import TradeDebugAPI
from Coin import Coin
import State, priceQuotation
import logging
class Account:

    def __init__(self, mode):
        if mode == 'release':
            self.tApi = TradeReleaseAPI()
        elif mode == 'debug' :
            TradeDebugAPI.init()
            self.tApi = TradeDebugAPI
        self.having_list = self.tApi.get_balances()
        for item in self.having_list:
            if item['currency'] == 'KRW':
                self.myMoney = item['balance']
                break
        logging.info('my money : {}'.format(self.myMoney))
        logging.info('Account init success. mode: '.format(mode))

    def get_have_coin_list(self):
        res = self.tApi.get_balances()
        coin_list = []
        for item in res:
            if item['currency'] == 'KRW':
                self.myMoney = item['balance']
                continue
            ticker = 'KRW-{}'.format(item['currency'])
            cost = item['avg_buy_price']
            count = item['balance']
            state = State.get_bought()
            coin_list.append(Coin(ticker,cost,count,state))
        return coin_list

    def request_order(self, ticket_list):
        for ticket in ticket_list:
            if ticket.get_order() == 'buy':
                if ticket.get_order_type() == 'market':
                    balance = priceQuotation.get_price(self.myMoney * 0.3)
                    res = self.tApi.buy_market_order(ticket.get_coin().get_ticker(), balance)
                    logging.info(res)

                elif ticket.get_order_type() == 'limit':
                    pass

            elif ticket.get_order() == 'sell':
                if ticket.get_order_type == 'market':
                    pass

                elif ticket.get_order_type() == 'limit':
                    #print('sell',ticker)
                    count = ticket.get_coin().get_count()
                    limit_cost = priceQuotation.get_price(ticket.get_limit_cost())
                    res = self.tApi.sell_limit_order(ticket.get_coin().get_ticker(),limit_cost, count)
                    logging.info(res)
            
