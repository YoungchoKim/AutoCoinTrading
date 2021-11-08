#!/usr/bin/env python3
import os
import logging
import logging.config
import time
import State
import numpy as np
from queue import Queue
from YunjooAlgo import YunjooAlgo
from nineAlgo import NineAlgo
from quotationRelApi import QuotationRelApi
from quotationDebugApi import QuotationDebugApi
from multiprocessing import shared_memory, Semaphore
from PriceInfo import PriceInfo
from TimeControl import TimeControl
from account import Account

class Controller:
    def __init__(self):
        self.log_init()
        self.mode = 'release'
        TimeControl.set_mode(self.mode)

        self.queue = Queue()
        if self.mode == 'release':
            self.pInfo = PriceInfo(QuotationRelApi(), self.queue)
        elif self.mode == 'debug':
            self.shm_init()
            TimeControl.init(self.shm.name, self.sem)
            self.pInfo = PriceInfo(QuotationDebugApi(), self.queue, self.shm.name, self.sem)

        self.account = Account(self.mode)

        self.yunjooAlgo = YunjooAlgo(self.mode, self.pInfo, self.queue)
        self.nineAlgo = NineAlgo(self.mode, self.pInfo, self.queue)
        self.tAlgo = self.nineAlgo

        self.pInfo.daemon = True
        self.pInfo.start()
        self.sleep_time = TimeControl.get_sleep_time()
        self.coin_list = []

    def shm_init(self):
        self.shm = shared_memory.SharedMemory(create=True, size=64)
        self.np_shm = np.ndarray((1,1), dtype='u8', buffer=self.shm.buf)
        self.np_shm[0] = 201
        self.sem = Semaphore()
        print('shm init good')

    def increase_shm(self):
        self.sem.acquire()
        new_shm = shared_memory.SharedMemory(name=self.shm.name)
        tmp_arr = np.ndarray((1,1), dtype='u8', buffer=new_shm.buf)
        tmp_arr[0] += 1
        print('{}/{}'.format(tmp_arr[0], TimeControl.get_debug_max_len()-1))
        self.sem.release()

    def log_init(self):
        if not os.path.isdir('log'):
            os.mkdir('log')
        now = time.strftime('%c', time.localtime(time.time()))
        now = now.replace(' ','_')
        print(now)
        logging.basicConfig(filename='log/{}.log'.format(now), filemode='w', format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        logging.info('log init success')


    def run(self):
        while True:
            now = TimeControl.get_min()

            coin_list = self.account.get_have_coin_list()
            self.coin_list = self.update_have_coin_list(coin_list)

            self.tradeTicket_list = self.tAlgo.get_tradeTicket_list(self.coin_list)
            self.account.request_order(self.tradeTicket_list)

            ticket_ticker_list = [ticket.get_coin().get_ticker() for ticket in self.tradeTicket_list]
            self.update_sell_wait(ticket_ticker_list)
            time.sleep(self.sleep_time['while'])

            if self.mode == 'debug':
                self.increase_shm()
                if TimeControl.is_debug_end():
                    self.account.print_total()
                    return

    def update_sell_wait(self, ticker_list):
        for ticker in ticker_list:
            for coin in self.coin_list:
                if ticker == coin.get_ticker():
                    coin.set_state(State.get_waitSell())

    def update_have_coin_list(self, coin_list):
        new_coin_list = []
        have_ticker_list = [coin.get_ticker() for coin in self.coin_list]
        if len(have_ticker_list) != 0:
            logging.info('have_ticker_list: {}'.format(have_ticker_list))
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
    print('debug end')

        
