class Coin:
    def __init__(self, name, base_coin='btc'):
        self.Name = name
        self.Symbols = [base_coin]

    def set_symbol(self, base_coin):
        if self.Symbols.count(base_coin) <= 0:
            self.Symbols.append(base_coin)
