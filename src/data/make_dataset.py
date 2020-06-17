# -*- coding: utf-8 -*-
import os
import logging
import pandas as pd
import numpy as np
import datetime as dt
from utils import utils, logger_utils
import yaml

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
    
    df_input_path = os.path.join('./src/data', input_data_path)
    df_input = pd.read_csv(df_input_path)
    logger.info("Reading tick and weights from %s" % df_input_path)
    
    ticks = df_input['TICK'].to_list()

    if df_input['WEIGHT'].isna().sum():
        logger.warning("Please check weights because there are missing values. Equals weight be stocks will be asigned")
        n_stocks = df_input.shape[0]
        weights = np.repeat(1/n_stocks, n_stocks)
    else:
        weights = df_input['WEIGHT'].to_list()

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
        df = utils.get_stock_data(ticks, start_date, end_date, metric, source)
        df.to_csv(data_path)
        logger.info("Getting %s SP500 data from %s since %s to %s" % (metric, source, start_date, end_date))
        sp500 = utils.get_stock_data(['^GSPC'], start_date, end_date, metric, source)
        sp500.to_csv(data_sp_path)

    t1 = dt.datetime.now()
    logger.info("Data is reaady to be used. It took %s seconds" % ((t1-t0).total_seconds()))


if __name__ == '__main__':
    main()
