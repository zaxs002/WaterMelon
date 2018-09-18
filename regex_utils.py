def get_symbol_by_hyphen(symbol):
    import re
    pattern = re.compile(r'^(?P<coin>(\w+)*)-(?P<base>(\w+)*)$')
    return next(pattern.finditer(symbol)).groupdict()


def get_symbol_by_whole(symbol):
    import re
    pattern = re.compile(r'^(?P<coin>(\w+)*)(?P<base>(btc|eth|usdt))$')
    return next(pattern.finditer(symbol)).groupdict()


def whole2hyphen(whole):
    s_dict = get_symbol_by_whole(whole)
    if len(s_dict) > 1:
        s = s_dict['coin'] + '-' + s_dict['base']
        return s
    return ''


def hyphen2whole(hyphen):
    s_dict = get_symbol_by_hyphen(hyphen)
    if len(s_dict) > 1:
        s = s_dict['coin'] + s_dict['base']
        return s
    return ''


if __name__ == '__main__':
    base_coin_by_symbol = get_symbol_by_whole('ethbtc')
    print(base_coin_by_symbol)
