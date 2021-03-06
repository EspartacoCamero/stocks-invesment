from argparse import ArgumentParser
import pandas_datareader as pdr
import pandas as pd
import datetime as dt
import numpy as np
import os

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

def get_stock_data(stocks, start_date, end_date, col='Adj Close', source='yahoo'):
    if len(stocks)>1:
        df = pdr.DataReader(stocks, source, start=start_date, end=end_date)[col]
    elif len(stocks)==1:
        df = pd.DataFrame(pdr.DataReader(stocks, source, start=start_date, end=end_date)[col], columns=stocks)
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
    ticks = df_input['TICK'].to_list()

    if df_input['WEIGHT'].isna().sum():
        # logger.warning("Please check weights because there are missing values. Equals weights to stocks will be asigned")
        n_stocks = df_input.shape[0]
        weights = np.repeat(1/n_stocks, n_stocks)
        df_input['WEIGHT'] = weights
    else:
        weights = df_input['WEIGHT'].to_list()

    return df_input