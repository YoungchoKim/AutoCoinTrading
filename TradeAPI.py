class TradeAPI:

    def get_tickers(self, fiat):
        pass
    
    def get_current_price(self, ticker_list):
        pass

    def get_ohlcv(self, ticker, count=200, interval='day', to='20210922'):
        pass

    def get_orderbook(self, tickers):
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
    
