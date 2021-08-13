#!/usr/bin/python

import coin
import account
import tradeapi

class Controller:
    def __init__(self):
        release = True
        self.trade = tradeapi.TradeApi(release)
        self.coin = coin.Coin(self.trade)
        self.account = account.Account(release, self.trade)
        self.run()


    def run(self):
        bought_dict = self.account.get_bought_dict()
        buy_list = []
        sell_list = []
        while True:
            date, buy_list, sell_list = self.coin.check_cur_state(bought_dict)
            if len(buy_list) > 0:
                print('buy: ' + date, end=' ')
                print(buy_list)
                self.account.buy_market_order(buy_list)
            
            if len(sell_list) > 0:
                print('sell: ' + date, end=' ')
                print(sell_list)
                self.account.sell_market_order(sell_list)


if __name__ == '__main__':
    controller = Controller()
    #krw_tickers = tradeapi.get_tickers(fiat="KRW")
    #prices = tradeapi.get_current_price(krw_tickers)
    #print(prices)
    #while True:

        


