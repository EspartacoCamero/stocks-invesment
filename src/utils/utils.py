from argparse import ArgumentParser
import pandas_datareader as pdr
import pandas as pd
import datetime as dt
import numpy as np
import os
from pandas_datareader import data as pdr
import yfinance as yfin
import talib
yfin.pdr_override()

def get_args():
    """
    Parse the arguments to generate the data.

    Returns:
        Namespace object with he parsed arguments.
    """
    parser = ArgumentParser(description="Read data from yml file")
    parser.add_argument("config_file_path", type=str, help="file with all configurations")
    args = parser.parse_args()

    return args

def get_stock_data(stock, start_date, end_date, col='Adj Close'):
    df = pdr.get_data_yahoo(stock, start=start_date, end=end_date)[col]
    return df

def filename_maker(name: str, path: str, start_date, end_date) -> str:
    """
    Create the name of the main files

    Returns:
        String with the path to save the file.

    """
    return os.path.join(path, name + start_date.replace('-','') + '_' + end_date.replace('-',''))

def get_start_end(yml_config):
    start_date = yml_config['stocks']['start']
    end_date = yml_config['stocks']['end']

    if isinstance(start_date, int):
        start_date = dt.date.today() - dt.timedelta(start_date)
        start_date = start_date.isoformat()

    if end_date is None:
        end_date = dt.date.today().isoformat()
    return start_date, end_date

def get_ticks_data(path) -> pd.DataFrame:
    """
    Read the initial ticks data that the user needs to upload

    Returns:
        DataFrame with ticks and weights

    """

    df_input = pd.read_csv(path) 
    cols = df_input.columns.to_list()
    if 'TICK' not in cols:
        raise Exception("No TICK column, please add it or rename it")

    if df_input['WEIGHT'].isna().sum() > 0:
        # logger.warning("Please check weights because there are missing values. Equals weights to stocks will be asigned")
        n_stocks = df_input.shape[0]
        weights = np.repeat(1/n_stocks, n_stocks)
        df_input['WEIGHT'] = weights
    else:
        weights = df_input['WEIGHT'].to_list()

    return df_input

def get_metrics(df, kpi_config) -> pd.DataFrame:
    """
    Recieve a DataFrame with all the stock ticks to analyze (with historical values)

    Returns:
        DataFrame with tickes and main KPIs

    """
    columns = ['price', 'stock']
    for i in kpi_config:
        dict_key = list(i.keys())
        if dict_key[0] == 'rsi':
            if i['rsi'][0]==True:
                columns.append('rsi')
        if dict_key[0] == 'sma':
            if i['sma'][0]==True:
                columns = columns + ['sma_low', 'sma_up']
                sma= i
        if dict_key[0] == 'bbands':
            if i['bbands'][0]==True:
                columns = columns + ['bb_low', 'bb_mid', 'bb_up']
                bbands = i
        if dict_key[0] == 'ema':
            if i['ema'][0]==True:
                columns = columns + ['ema_low', 'ema_up']
                ema = i

    df_clean = pd.DataFrame(columns=columns)
    
    for col in df.columns.to_list():
        df_aux = pd.DataFrame()
        df_aux = df[[col]]
        df_aux.columns = ['price']
        df_aux['stock'] = col
        df_aux['rsi'] = talib.RSI(df.loc[:, col])
        df_aux['ema_low'] = talib.EMA(df.loc[:, col], ema['ema'][1])
        df_aux['ema_up'] = talib.EMA(df.loc[:, col], ema['ema'][2])
        upper_1sd, mid_1sd, lower_1sd = talib.BBANDS(df.loc[:, col], nbdevup=bbands['bbands'][1], nbdevdn=bbands['bbands'][2], timeperiod=bbands['bbands'][3])
        df_aux['bb_low'] = upper_1sd
        df_aux['bb_mid'] = mid_1sd
        df_aux['bb_up'] = lower_1sd
        df_clean = df_clean.append(df_aux)
    
    return df_clean