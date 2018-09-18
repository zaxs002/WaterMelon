class Exchange:
    def __init__(self):
        self.PriceQueue = {}
        self.Currency = {}
        self.AmountDict = {}
        self.weightDict = {}
        self.ValidSymbols = []
        self.Name = ''
        self.Weight = 0
        self.TradeFee = {}
        self.Transfer = {}

    def get_last_price(self, symbol):
        return self.PriceQueue.get(symbol, -1)

    def get_amount(self, symbol):
        return self.AmountDict.get(symbol, 0)

    def set_amount(self, currency, num):
        self.AmountDict[currency] = self.AmountDict.get(currency, 0) + num
        print('%s交易所%s余额增加%f' % (self.Name, currency, num))
        # try:
        #     self.AmountDict[symbol]
        # except:
        #     self.AmountDict[symbol] = 0
        #     self.AmountDict[symbol] += num

    def set_user_amount(self, symbol, num, u):
        try:
            user_amount_dict = self.AmountDict[u.Name]
        except:
            self.AmountDict[u.Name] = {}
            user_amount_dict = self.AmountDict[u.Name]
        try:
            user_amount_dict[symbol]
        except:
            user_amount_dict[symbol] = 0
        user_amount_dict[symbol] += num

    def get_name(self):
        return self.Name

    # 交易所自主买币, 和用户没关系
    def buy_coin(self, symbol, num):
        price = self.get_last_price(symbol)
        # 花费比特币
        total = price * num
        self.set_amount(symbol, num)
        return total

    # 交易所自主卖币, 和用户没关系
    def sell_coin(self, symbol, num):
        price = self.get_last_price(symbol)
        # 得到比特币
        total = price * num
        self.set_amount(symbol, -num)
        return total

    def get_transfer(self, currency):
        c = self.Transfer.get(currency)
        return c
