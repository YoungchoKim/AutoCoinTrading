import Coin

class TradeTicket:
    def __init__(self, order, order_type, limit_cost, coin):
        self.order = order
        self.order_type = order_type
        self.limit_cost = limit_cost
        self.coin = coin

    def get_order(self):
        return self.order

    def set_order(self, order):
        self.order = order

    def get_order_type(self):
        return self.order_type

    def set_order_type(self, order_type):
        self.order_type = order_type

    def get_limit_cost(self):
        return self.limit_cost

    def set_limit_cost(self, limit_cost):
        self.limit_cost = limit_cost

    def get_coin(self):
        return self.coin

    def set_coin(self, coin):
        self.coin = coin

