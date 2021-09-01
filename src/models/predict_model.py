import pandas as pd
import logging
import numpy as np
import datetime as dt


def main():
            
    t0 = dt.datetime.now()

    args = utils.get_args()
    all_config = yaml.safe_load(open(args.config_file_path, "r"))

    DATA = all_config['output']['data_folder']
    input_data_path = all_config['stocks']['data']
    logger = logger_utils.log_creator(all_config['output']['log_folder'], log_name='ticks_off')
    start_date, end_date = utils.get_start_end(all_config)

    df_ticks_path = os.path.join('./src/data', input_data_path)
    logger.info("Reading tick and weights from %s" % df_ticks_path)
    weights = utils.get_ticks_data(df_ticks_path)

    data_path = utils.filename_maker('stocks_', DATA, start_date, end_date)
    df = pd.read_csv(data_path)


if __name__ == "__main__":
    main()