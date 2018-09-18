import json
import threading
import requests
import time

import regex_utils
from Exchange import Exchange
from User import User
from We import We


def run():
    url = 'http://103.102.4.18:8080'
    url = 'http://127.0.0.1:8080'
    session = requests.session()
    while True:
        r = session.get(url).content.decode('utf-8')
        j = json.loads(r)
        es = j['exchanges']
        for e in es:
            e = e['exchange']
            name = e['name']
            ss = e['symbols']
            currency = e['currency']
            trade_fee = e['tradeFee']
            transfer = e['transfer']

            if len(exchanges) == 0:
                o = Exchange()
                o.Name = name
                exchanges.append(o)
            else:
                exist_flag = False
                for r_e in exchanges:
                    if r_e.get_name() == name:
                        exist_flag = True
                        for s in ss:
                            r_e.PriceQueue[s] = float(ss[s])
                        r_e.TradeFee = trade_fee
                        r_e.Currency = currency
                        ts = {}
                        for t in transfer:
                            j = json.loads(transfer[t])
                            ts[t] = j
                        r_e.Transfer = ts

                if not exist_flag:
                    o = Exchange()
                    o.Name = name
                    exchanges.append(o)
        time.sleep(0.5)


symbols = [
    "dashbtc", "etcbtc",
    "eosbtc", "omgbtc", "ethbtc",
    "xrpbtc", "zecbtc", "ltcbtc",
    "vitbtc", "clrbtc", "nctbtc",
    "axpbtc", "bmhbtc", "hqxbtc",
    "ldcbtc", "xmobtc", "berrybtc",
    "bstnbtc", "shipbtc", "lncbtc",
    "uncbtc", "rpxbtc", "clbtc",
    "daybtc", "daxtbtc", "fotabtc",
    "sethbtc", "nxtbtc", "qcnbtc",
    "scbtc", "steembtc", "xdnbtc",
    "xembtc", "xmrbtc", "ardrbtc"
]
exchanges = []
users = []

# 1.用户存币
# 2.用户提币
# 3.用户买币
# 4.用户卖币

if __name__ == '__main__':
    time_duration = 1

    thread = threading.Thread(target=run)
    thread.start()

    time.sleep(time_duration)

    for i in range(1, 10):
        user = User('TestUser%d' % i)
        for s in symbols:
            s = regex_utils.whole2hyphen(s)
            user.AmountDict[s] = 0.0
        users.append(user)

    symbol = 'eth-btc'
    new_symbol_dict = regex_utils.get_symbol_by_hyphen(symbol)
    currency = new_symbol_dict['coin']
    base = new_symbol_dict['base']
    we = We(users, exchanges)
    exchange_avg_price = we.get_exchange_avg_price_by_exchange(symbol)
    print('%s显示价格:%f' % (symbol, exchange_avg_price))
    we.user_depot('TestUser1', 100, currency)
    # excellent_e = we.get_excellent_exchange_by_symbol('eth-btc')

    we.user_buy('TestUser1', 50, symbol)
