#!/usr/bin/python

import coin
import account
import tradeapi
import logging
import logging.config

class Controller:
    def __init__(self):
        logging.basicConfig(filename='app.log', filemode='w', format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        logging.info('init success')
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
                logging.info('buy(before): {}'.format(buy_list))
                self.account.buy_market_order(buy_list)
            
            if len(sell_list) > 0:
                self.account.sell_market_order(sell_list)


if __name__ == '__main__':
    controller = Controller()
    #krw_tickers = tradeapi.get_tickers(fiat="KRW")
    #prices = tradeapi.get_current_price(krw_tickers)
    #logging.info(prices)
    #while True:

        
