from argparse import ArgumentParser
import pandas_datareader as pdr

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