import talib


def ema(df_col, rolling):
    return talib.EMA(df_col, rolling)

def rsi(df_col):
    return talib.RSI(df_col)

def bbands(df_col, sd_up=1, sd_dn=1, time=20)
    upper_sd, mid_sd, lower_sd = talib.BBANDS(df.loc[:, col], nbdevup=sd_up, nbdevdn=sd_dn, timeperiod=time)
    return upper_sd, mid_sd, lower_sd

