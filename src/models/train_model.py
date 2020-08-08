import pandas as pd
import logging
import numpy as np
import datetime as dt
from utils import utils, logger_utils
from scipy.stats import skew, kurtosis, shapiro
import yaml
import os

def main():
    """ Runs the main descriptive stadistict about stocks and also get optimal portafolio
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
    ticks = weights['TICK'].to_list()
    skew_list = []
    kurtosis_list = []
    shapiro_list = []
    annual_vol = []
    annual_returns = []
    for tk in ticks:
        skewness = np.round(df_pc[tk].skew(), 3)
        kurt = np.round(df_pc[tk].kurtosis() + 3, 3)
        shap = np.round(shapiro(df_pc[tk])[1], 3)
        vol = np.round(df_pc[tk].std()*np.sqrt(252), 3)
        rtn = np.round((df_pc[tk].mean()*252), 3)
        
        skew_list.append(skewness)
        kurtosis_list.append(kurt)
        shapiro_list.append(shap)
        annual_vol.append(vol)
        annual_returns.append(rtn)

    logger.info("This is the summary of the stocks regaridn the anual return, anual volatility, kurtosis, shapiro and skew.")
    stocks_summary = pd.DataFrame({'STOCK': ticks,
                                   'SKEW': skew_list,
                                   'KURTOSIS': kurtosis_list,
                                   'SHAPIRO': shapiro_list,
                                   'ANNUAL_VOL': annual_vol,
                                   'ANNUAL_RETURN': annual_returns})
    stocks_summary.set_index('STOCK', inplace=True)

    logger.info(stocks_summary)
    t1 = dt.datetime.now()
    #logger.info("Process finished. It took %s seconds" % ((t1-t0).total_seconds()))

if __name__ == '__main__':
    main()