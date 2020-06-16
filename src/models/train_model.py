import pandas as pd
import logging
import datetime as dt

def main():
    """ Runs the main descriptive stadistict about stocks and also get optimar portafolio
    """
        
    t0 = dt.datetime.now()

    args = utils.get_args()
    all_config = yaml.safe_load(open(args.config_file_path, "r"))

    args = utils.get_args()
    all_config = yaml.safe_load(open(args.config_file_path, "r"))

    DATA = all_config['output']['data_folder']
    df = pd.DataFrame(os.path.join(DATA,'raw',))

    t1 = dt.datetime.now()
    logger.info("Process finished. It took %s seconds" % ((t1-t0).total_seconds()))

if __name__ == '__main__':
    main()