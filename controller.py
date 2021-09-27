#!/usr/bin/python
import logging
import logging.config
import time
import State
from YunjooAlgo import YunjooAlgo
from TimeControl import TimeControl
from account import Account

class Controller:
    def __init__(self):
        logging.basicConfig(filename='app.log', filemode='w', format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        logging.info('log init success')
        
        mode = 'debug'
        TimeControl.set_mode(mode)
        self.account = Account(mode)
        self.tAlgo = YunjooAlgo(mode)
        self.sleep_time = TimeControl.get_sleep_time()
        self.coin_list = []

    def run(self):
        while True:
            coin_list = self.account.get_have_coin_list()
            self.coin_list = self.update_have_coin_list(coin_list)

            self.tradeTicket_list = self.tAlgo.get_tradeTicket_list(self.coin_list)
            self.account.request_order(self.tradeTicket_list)

            ticket_ticker_list = [ticket.get_coin().get_ticker() for ticket in self.tradeTicket_list]
            self.update_sell_wait(ticket_ticker_list)
            
            time.sleep(self.sleep_time['while'])

    def update_sell_wait(self, ticker_list):
        for ticker in ticker_list:
            for coin in self.coin_list:
                if ticker == coin.get_ticker():
                    coin.set_state(State.get_waitSell())

    def update_have_coin_list(self, coin_list):
        new_coin_list = []
        have_ticker_list = [coin.get_ticker() for coin in self.coin_list]
        if len(have_ticker_list) != 0:
            print('have_ticker_list:', have_ticker_list)
        for coin in coin_list:
            if coin.get_ticker() in have_ticker_list:
                for have_coin in self.coin_list:
                    if coin.get_ticker() == have_coin.get_ticker():
                        new_coin_list.append(have_coin)
                        break
                continue
            new_coin_list.append(coin)
        
        return new_coin_list
        
if __name__ == '__main__':
    controller = Controller()
    controller.run()

        
