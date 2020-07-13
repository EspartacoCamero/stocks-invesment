import pandas as pd
import logging
import numpy as np
import datetime as dt
from utils import utils, logger_utils
import yaml
import os

def main():
    """ Runs the main descriptive stadistict about stocks and also get optimar portafolio
    """
        
    t0 = dt.datetime.now()

    args = utils.get_args()
    all_config = yaml.safe_load(open(args.config_file_path, "r"))

    DATA = all_config['output']['data_folder']
    input_data_path = all_config['stocks']['data']
    logger = logger_utils.log_creator(all_config['output']['log_folder'], log_name='get_stats')
    start_date, end_date = utils.get_start_end(all_config)

    df_ticks_path = os.path.join('./src/data', input_data_path)
    logger.info("Reading tick and weights from %s" % df_ticks_path)
    weights = utils.get_ticks_data(df_ticks_path)

    data_path = utils.filename_maker('stocks_', DATA, start_date, end_date)
    data_sp_path = utils.filename_maker('sp500_', DATA, start_date, end_date)

    df = pd.read_csv(data_path)
    sp = pd.read_csv(data_sp_path)

    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df_pc = df.pct_change().dropna()

    sp['Date'] = pd.to_datetime(sp['Date'])
    sp.set_index('Date', inplace=True)
    sp_pc = sp.pct_change().dropna()

    weights_np = weights['WEIGHT'].to_numpy()

    anual_cov_matrix = df_pc.cov()*252
    volatilidad_por_anual = np.sqrt(np.dot(weights_np.T, np.dot(anual_cov_matrix, weights_np)))
    logger.info("Anual portafolio volatility is %.2f" % volatilidad_por_anual)

    portafolio_anual_return = np.sum(df_pc.mean()*weights_np)*252
    logger.info("Anual portafolio return is %.2f" % portafolio_anual_return)

    
    logger.info("Mean historical return for each stock %s" % round((df_pc.mean()*252),2))
    logger.info("Anual volatility for each stock %s" % round(np.std(df_pc)*np.sqrt(252),2))
    
    # np.sum(df_pc.mean()*weights['WEIGHT'].to_numpy())*252
    

    t1 = dt.datetime.now()
    #logger.info("Process finished. It took %s seconds" % ((t1-t0).total_seconds()))

if __name__ == '__main__':
    main()