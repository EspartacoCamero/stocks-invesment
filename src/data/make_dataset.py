# -*- coding: utf-8 -*-
import os
import logging
import pandas as pd
import numpy as np
import datetime as dt
from utils import utils, logger_utils
import yaml
from pandas_datareader import data as pdr
import yfinance as yfin
yfin.pdr_override()

def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    
    t0 = dt.datetime.now()

    args = utils.get_args()
    all_config = yaml.safe_load(open(args.config_file_path, "r"))

    DATA = all_config['output']['data_folder']
    input_data_path = all_config['stocks']['data']
    logger = logger_utils.log_creator(all_config['output']['log_folder'], log_name='make_dataset')
    
    df_ticks_path = os.path.join('./src/data', input_data_path)
    logger.info("Reading tick and weights from %s" % df_ticks_path)
    ticks = utils.get_ticks_data(df_ticks_path)

    start_date, end_date = utils.get_start_end(all_config)
    metric = all_config['stocks']['metric']
    source = all_config['stocks']['source']
    
    logger.info("Getting stock data and SP500 evolution")
    data_path = utils.filename_maker('stocks_', DATA, start_date, end_date)
    data_sp_path = utils.filename_maker('sp500_', DATA, start_date, end_date)

    if os.path.exists(data_path):
        logger.info("Retrieving data from local path")
        df = pd.read_csv(data_path)
        sp500 = pd.read_csv(data_sp_path)
    else:
        logger.info("Getting %s data from %s since %s to %s" % (metric, source, start_date, end_date))
        df = utils.get_stock_data(ticks['TICK'].to_list(), start_date, end_date, metric)
        df.to_csv(data_path)
        logger.info("Getting %s SP500 data from %s since %s to %s" % (metric, source, start_date, end_date))
        sp500 = utils.get_stock_data(['^GSPC'], start_date, end_date, metric)
        sp500.to_csv(data_sp_path)

    t1 = dt.datetime.now()
    logger.info("Data is reaady to be used. It took %s seconds" % ((t1-t0).total_seconds()))


if __name__ == '__main__':
    main()
