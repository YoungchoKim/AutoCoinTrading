class ExchangeApi:

    def get_order(self, ticker, state='wait'):
        pass

    def get_balance(self, ticker):
        pass

    def get_balances(self):
        pass

    def sell_limit_order(self,ticker, cost, count):
        pass

    def buy_limit_order(self,ticker, cost, count):
        pass

    def sell_market_order(self,ticker, count):
        pass

    def buy_market_order(self,ticker, balance):
        pass
    
    def cancel_order(self, uuid):
        pass


