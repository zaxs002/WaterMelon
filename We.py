import re

import Exchange
import regex_utils
from print_utils import print_blue, print_green, print_red


class We:
    def __init__(self, users, exchanges):
        self.total_rmb = 0
        self.users = users
        self.exchanges = exchanges
        self.rate = 60000
        for e in self.exchanges:
            e.set_amount('eth-btc', 100)

    def __str__(self):
        us = []
        for u in self.users:
            ud = {
                'name':    u.Name,
                'account': u.AmountDict
            }
            us.append(ud)
        d = []
        for e in self.exchanges:
            ed = {
                "name":            e.Name,
                'tradeFee':        e.TradeFee,
                'symbol_length':   len(e.PriceQueue),
                'currency_length': len(e.Currency),
                'transfer_length': len(e.Transfer)
            }
            d.append(ed)

        return str(us + d)

    def get_exchange_avg_price_by_exchange(self, symbol):
        """
        获得symbol的交易所平均价格
        :param symbol:
        :return: 平均价格
        """
        total_price = 0
        total_count = 0
        es = self.exchanges
        for e in es:
            price = e.get_last_price(symbol)
            if price > 0:
                total_price += price
                total_count += 1

        return total_price / total_count

    def get_exchange_avg_price_by_exchange_currency(self, currency):
        """
        获得currency的交易所平均价格
        :param currency
        :return: 平均价格
        """
        total_price = 0
        total_count = 0
        es = self.exchanges
        for e in es:
            price = e.get_last_price(currency)
            if price > 0:
                total_price += price
                total_count += 1

        return total_price / total_count

    def get_excellent_exchange_by_symbol(self, symbol: str) -> tuple:
        """
        通过symbol获得该币种最优交易所

        哪几点确定最优交易所
        1. 该币种价格高
        2. 手续费低
        3. 交易深度
        4. 用户量大
        5. 币种数量多
        6. 转账时间短
        每项满权重100,  一共满权重600
        一. (以参考值作为权重判断依据, 来判断权重)
        (参考值权重50)
        二. (以最高项作为满权重)
        :param symbol:
        :return: 该symbol的最优交易所
        """
        es = self.exchanges

        weights_d = {}
        for e in es:
            weights_d[e] = 0
        # 价格权重
        avg_price = self.get_exchange_avg_price_by_exchange(symbol)
        for e in es:
            price = e.get_last_price(symbol)
            if price <= 0:
                print('%s 无%s价格' % (e.Name, symbol))
                continue
            duibi = price / avg_price
            price_weight = duibi * 50
            # print('%s价格权重:%f' % (e.get_name(), price_weight))
            weights_d[e] = price_weight
        # 手续费权重
        currency = re.sub('-(\w+)', '', symbol)
        avgs = self.get_avg_transfer_by_exchange(currency)
        for e in es:
            ts = e.get_transfer(currency)
            if ts is None or int(ts['CanWithdraw']) < 1:
                print('%s没有转账信息' % e.Name)
                weights_d[e] += 0
                continue
            fee_weight = float(ts['WithdrawFee']) / avgs[0]
            # fee_MinConfirmations = ts['WithdrawMinConfirmations'] / avgs[1]
            # fee_MinWithdrawFee = ts['MinWithdrawFee'] / avgs[2]
            transfer_weight = 50 - fee_weight * 50
            # print('%s转账费权重:%f' % (e.get_name(), transfer_weight))
            weights_d[e] += transfer_weight
            # print('%s最小确认权重:%f' % (e.get_name(), fee_MinConfirmations * 50))
            # print('%s最小转账费权重:%f' % (e.get_name(), fee_MinWithdrawFee * 50))
        w = sorted(weights_d.items(), key=lambda y: float(y[1]), reverse=True)
        # w = dict(w)

        return w[0]

    def get_excellent_exchange_by_currency(self, currency: str) -> tuple:
        """
        通过currency获得该币种最优交易所

        哪几点确定最优交易所
        1. 该币种价格高
        2. 手续费低
        3. 交易深度
        4. 用户量大
        5. 币种数量多
        6. 转账时间短
        每项满权重100,  一共满权重600
        一. (以参考值作为权重判断依据, 来判断权重)
        (参考值权重50)
        二. (以最高项作为满权重)
        :param currency
        :return: 该currency的最优交易所
        """
        es = self.exchanges

        weights_d = {}
        for e in es:
            weights_d[e] = 0
        # 价格权重
        avg_price = self.get_exchange_avg_price_by_exchange(currency)
        for e in es:
            price = e.get_last_price(currency)
            if price <= 0:
                print('%s 无%s价格' % (e.Name, currency))
                continue
            duibi = price / avg_price
            price_weight = duibi * 50
            # print('%s价格权重:%f' % (e.get_name(), price_weight))
            weights_d[e] = price_weight
        # 手续费权重
        avgs = self.get_avg_transfer_by_exchange(currency)
        for e in es:
            ts = e.get_transfer(currency)
            if ts is None or int(ts['CanWithdraw']) < 1:
                print('%s没有转账信息' % e.Name)
                weights_d[e] += 0
                continue
            fee_weight = float(ts['WithdrawFee']) / avgs[0]
            # fee_MinConfirmations = ts['WithdrawMinConfirmations'] / avgs[1]
            # fee_MinWithdrawFee = ts['MinWithdrawFee'] / avgs[2]
            transfer_weight = 50 - fee_weight * 50
            # print('%s转账费权重:%f' % (e.get_name(), transfer_weight))
            weights_d[e] += transfer_weight
            # print('%s最小确认权重:%f' % (e.get_name(), fee_MinConfirmations * 50))
            # print('%s最小转账费权重:%f' % (e.get_name(), fee_MinWithdrawFee * 50))
        w = sorted(weights_d.items(), key=lambda y: float(y[1]), reverse=True)
        # w = dict(w)

        return w[0]

    '''
    1.确定存币币种
    2.通过币种得到最优化交易所
    3.
    '''

    def user_depot(self, user_name, num, currency):
        current_user = None
        for u in self.users:
            if u.Name == user_name:
                current_user = u
                break
        if current_user is None:
            print('请检查用户名')
            return
        current_user.AmountDict[currency] += num

        excellent_exchange_tuple = self.get_excellent_exchange_by_currency(currency)
        excellent_exchange = excellent_exchange_tuple[0]
        excellent_exchange.set_amount(currency, num)

    '''
    1.寻找价格最低的交易所
    2.计算出显示价格
    3.买币或分配币
    4.为用户分配币  在交易所和用户里
    '''

    def user_buy(self, user_name, num, symbol):
        current_user = None
        for u in self.users:
            if u.Name == user_name:
                current_user = u
                break
        max_e, min_e, max_p, min_p, avg_p = self.getMinMaxExchange(symbol)
        avg = (max_p - min_p) / 2 + min_p
        print('显示价格:%f' % avg)
        amount = min_e.get_amount(symbol)
        if amount > 0:
            print('%s交易所有%s余额:%f' % (min_e.Name, symbol, amount))
        else:
            print('没有一家交易所有%s余额,买币或转币' % (symbol))
            # 先尝试转币
            self.exchange_coins(min_e, symbol, num)
            coin = min_e.buy_coin(symbol, num)
            print('自主购买%s,花费了%f' % (symbol, coin))
        # 我们花费的
        we_should_cost = min_e.get_last_price(symbol) * num
        # 我们实际得到的
        user_cost = avg * num
        # 利润
        profit = user_cost - we_should_cost
        self.total_rmb += profit * self.rate
        print('获得%f个比特币,花费%f个比特币,利润%f个比特币,%f人民币' % (user_cost, we_should_cost, profit, profit * self.rate))
        # current_user.AmountDict[symbol] += num

    '''
    1.计算出显示价格
    2.寻找价格最高的交易所
    3.检查该交易所余额
    4.余额足够--卖掉对应的币
    5.余额不够--待定(假设余额都足够,用户转币或自主转币保证特定价高的几个币在这几个交易所余额足够)
    '''

    def user_sell(self, user_name, num, symbol):
        current_user = None
        for u in self.users:
            if u.Name == user_name:
                current_user = u
                break
        d = current_user.AmountDict.get(symbol, 0)
        if d <= 0:
            print('%s余额不足' % symbol)
            return
        max_e, min_e, max_p, min_p, avg_p = self.getMinMaxExchange(symbol)
        avg = (max_p - min_p) / 2 + min_p
        print('显示价格:%f' % avg)
        amount = max_e.get_amount(symbol)
        if amount >= num:
            print('%s交易所有%s余额:%f, 可以卖出!' % (max_e.Name, symbol, amount))
            max_e.set_amount(symbol, -num)
            coin = max_e.sell_coin(symbol, num)
            print('获得%f个%s' % (coin, symbol))
        else:
            print('余额不够--待定(假设余额都足够,用户转币或自主转币保证特定价高的几个币在这几个交易所余额足够)')
            return
        # min_e.set_amount(symbol, -num)

    def getMinMaxExchange(self, symbol):
        max_exchange = self.exchanges[0]
        min_exchange = self.exchanges[0]
        avg_price = 0
        min_price = 1000000
        prices = 0
        avg_count = 0
        for e in self.exchanges:
            price = e.get_last_price(symbol)
            if price <= 0:
                continue
            avg_count += 1
            prices += price
            if price > avg_price:
                avg_price = price
                max_exchange = e
            if price < min_price:
                min_price = price
                min_exchange = e
        if min_price == 1000000:
            min_price = 0

        if avg_count == 0:
            print('%s没有价格' % symbol)
            return None
        # avg_price -= avg_price * 0.003
        profit = (avg_price - min_price) * self.rate
        avg = prices / avg_count
        rate_price = avg_price / 100 * 0.1 * self.rate
        # print('%s 最高价格交易所:%s 价格:%f,最低:%s 价格:%f,均价:%f, 差价:%f, 按手续费:%f,两次手续费:%f, 纯利润:%f' %
        #       (symbol, max_exchange.Name, avg_price, min_exchange.Name, min_price, avg,
        #        profit, rate_price, rate_price * 2, profit - rate_price * 2))

        # print('\033[1;32m' + 'green' + '\033[0m')
        if avg_price == min_price:
            print_blue('%s 只在一个交易所发行, 无差价' % symbol)
            # print('\033[1;34m %s 只在一个交易所发行, 无差价 \033[0m' % symbol)
        else:
            if profit - rate_price * 2 >= 0:
                print_green('%s 人民币单价:%f, 纯利润:%f元, 差价:%f元, 按手续费:%f元,两次手续费:%f元' %
                            (symbol, avg * self.rate, profit - rate_price * 2, profit, rate_price, rate_price * 2,))
            else:
                print_red('%s 人民币单价:%f, 纯利润:%f元, 差价:%f元, 按手续费:%f元,两次手续费:%f元' %
                          (symbol, avg * self.rate, profit - rate_price * 2, profit, rate_price, rate_price * 2,))

        return max_exchange, min_exchange, avg_price, min_price, prices / avg_count

    # 向to_exchange转币
    def exchange_coins(self, to_exchange, symbol, num):
        # 挑出权重最低并且余额足够的交易所
        min_weight_exchange = self.get_min_weight_exchange_with_symbol(symbol)
        # 模拟转币流程 换成手续费最低的币 转到目标交易所 再换成btc购买目标币 这个过程可以延迟 按hsr来算 转一次0.1个hsr 手续费0.2%
        amount = min_weight_exchange.get_amount(symbol)
        # todo

    def get_min_weight_exchange_with_symbol(self, symbol):
        min_weight_e = self.exchanges[0]
        min_weight = 100
        for e in self.exchanges:
            # 排除余额不足的交易所
            if e.get_amount(symbol) <= 0:
                continue
            if min_weight > e.Weight:
                min_weight = e.Weight
                min_weight_e = e
        return min_weight_e

    def get_min_weight_exchange(self):
        min_weight_e = self.exchanges[0]
        min_weight = 100
        for e in self.exchanges:
            if min_weight > e.Weight:
                min_weight = e.Weight
                min_weight_e = e
        return min_weight_e

    '''
    1.提现费用
    2.提现时间
    3.最小提现金额
    '''

    def get_avg_transfer_by_exchange(self, currency):
        total_fee = 0
        total_confirmations = 0
        total_min_withdraw_fee = 0
        fee_count = 0
        es = self.exchanges
        for e in es:
            ts = e.get_transfer(currency)
            if ts['CanWithdraw'] > 0:
                total_fee += ts['WithdrawFee']
                fee_count += 1

                confirmations = ts['WithdrawMinConfirmations']
                total_confirmations += confirmations
                min_withdraw_fee = ts['MinWithdrawFee']
                if min_withdraw_fee == -1:
                    fee_count -= 1
                    break
                total_min_withdraw_fee += min_withdraw_fee

        avg_fee = total_fee / fee_count
        avg_confirmation = total_confirmations / fee_count
        avg_min_withdraw_fee = total_min_withdraw_fee / fee_count
        return avg_fee, avg_confirmation, avg_min_withdraw_fee
