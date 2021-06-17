def xp_years(value):
    xp_rule = value % 10
    xp_div = value // 10
    if (xp_rule == 1) and (xp_div != 1):
        xp_text = 'год'
    elif (xp_rule > 1) and (xp_rule < 5) and (xp_div != 1):
        xp_text = 'года'
    else:
        xp_text = 'лет'
    return xp_text

def how_price_is_it(value):
    rub = int(value)
    kop = int((value - rub) * 100)
    if (kop == 0):
        return '{} руб.'.format(rub)
    else:
        return '{} руб. {} коп.'.format(rub, kop)