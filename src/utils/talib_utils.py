import talib


def ema(df_col, rolling=12):
    """

    Args:
      df_col: variable to apply the ema analysis
      rolling: (Default value = 12) window for the ema, normally between 12 and 26

    Returns: ema calculation column

    
    """
    return talib.EMA(df_col, rolling)

def rsi(df_col):
    """

    Args:
      df_col: variable to apply the rsi analysis

    Returns: rsi calculation

    
    """
    return talib.RSI(df_col)

def bbands(df_col, sd_up=1, sd_dn=1, time=20):
    """

    Args:
      df_col: variable to apply the rsi analysis
      sd_up: (Default value = 1) standar deviation for the upper value
      sd_dn: (Default value = 1) standar deviation for the lower value
      time: (Default value = 20) is the window period for the sma

    Returns: 3 variables: upper, mid and lower interval for bollinger bands

    
    """

    upper_sd, mid_sd, lower_sd = talib.BBANDS(df.loc[:, col], nbdevup=sd_up, nbdevdn=sd_dn, timeperiod=time)
    return upper_sd, mid_sd, lower_sd

