class Coin:
    def __init__(self, ticker, cost, count, state):
        self.ticker = ticker
        self.cost = cost
        self.count = count
        self.state = state
    
    def get_ticker(self):
        return self.ticker

    def set_ticker(self, ticker):
        self.ticker = ticker
    
    def get_cost(self):
        return self.cost

    def set_cost(self, cost):
        self.cost = cost

    def get_count(self):
        return self.count

    def set_count(self, count):
        self.count = count

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state
