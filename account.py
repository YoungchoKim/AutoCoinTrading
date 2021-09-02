from collections import defaultdict
import logging
class Account:

    def __init__(self, release, trade):
        if release == True:
            self.user_file_name = 'user_file'
        else :
            self.user_file_name = 'user_file_debug'
        self.trade = trade
        user_file = open(self.user_file_name, 'r')
        user_file_stream = user_file.readlines()
        user_file.close()
        self.bought_dict = self.stream_to_dict(user_file_stream)
        logging.info('Account init success. release({})'.format(release))


    def stream_to_dict(self, user_file_stream):
        bought_dict = defaultdict(list)
        for one_line in user_file_stream:
            splited_line = one_line.replace('\n','').split(',')
            ticker = splited_line[0]
            bought_dict[ticker] = splited_line[1:]
        return bought_dict


    def get_bought_dict(self):
        return self.bought_dict


    def write_bought_dict(self, bought_dict):
        user_file = open(self.user_file_name, 'w')
        for k, v in bought_dict.items():
            if len(v) == 0:
                continue
            user_file.write('{},{},{}\n'.format(k, v[0], v[1])) #ticker, cost, cnt
        user_file.close()
        
    def buy_market_order(self, buy_list):
        for ticker, cost in buy_list:
            balance = self.trade.get_balance()
            if balance == None:
                logging.error('balance is zero or network error')
            balance = float(balance) * 0.3
            cnt = round(balance / cost, 3)
            if cnt == 0:
                logging.info('cnt is zero')
                return None
            bought_cost, bought_balance, uuid = self.trade.buy_market_order(ticker, cost, cnt)
            if bought_cost == 0:
                return None
            
            self.bought_dict[ticker] = [bought_cost, bought_balance, uuid]
            logging.info('buy, ticker:{} cost:{} balance:{}'.format(ticker, bought_cost, bought_balance))
        self.write_bought_dict(self.bought_dict)
            
            
            
    def sell_market_order(self, sell_list):
        for ticker, cost in sell_list:
            buy_cost, cnt, uuid = self.bought_dict[ticker]
            self.cancel_order(uuid)
            self.bought_dict[ticker] = []
            self.trade.sell_market_order(ticker, cost, float(cnt))
            logging.info('sell, ticker:{} cost:{} '.format(ticker, cost))
        self.write_bought_dict(self.bought_dict)

    def cancel_order(self, uuid):
        self.trade.cancel_order(uuid)
