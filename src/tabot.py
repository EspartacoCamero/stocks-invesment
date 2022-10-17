#!/usr/bin/python3
import pandas as pd
import datetime as dt
import numpy as np
import datetime as dt
from pandas_datareader import data as pdr
import yfinance as yfin
yfin.pdr_override()
import yaml
from utils import utils, telebot, logger_utils
import os

FILE_PATH = os.path.abspath(os.path.dirname(__file__))

t0 = dt.datetime.now()
all_config = yaml.safe_load(open(os.path.join(FILE_PATH, "../config_file.yml"), "r"))
logger = logger_utils.log_creator(all_config['output']['log_folder'], log_name='tabot')

logger.info("Reading tick data")
df_input = utils.get_ticks_data(os.path.join(FILE_PATH, 'data/example_data.csv'))

start_date, end_date = utils.get_start_end(all_config)
source = all_config['stocks']['source']
metric = all_config['stocks']['metric']
ticks = df_input['TICK'].to_list()

df = utils.get_stock_data(ticks, start_date, end_date, col=metric)
logger.info("Following ticks will be analyzed: \n %s" % df.columns)

df_clean = utils.get_metrics(df, all_config['model']['kpis'])
dflags = utils.get_flags(df_clean, all_config['strategy'])

# Telegram Bot
token = all_config['bot']['chat_token']
chat_id = all_config['bot']['chat_id']
bot = telebot.Tabot(token, chat_id)

# Message
total_ticks = len(df.columns)
msg_ticks = len(dflags.stock)
flags = all_config['strategy']['flags_het']

msg_title = "Stocks KPIs for {end_date}: \nWe got {msg_ticks} possible ticks from {total_ticks} with \
    at least {flags} flags. \n".format(end_date=end_date, msg_ticks=msg_ticks, total_ticks=total_ticks, flags=flags)
msg_header = '\nTICK \t PRICE RSI\n'

msgs = []
for row in dflags.itertuples():
    msgs.append('{s} \t {p} \t {rsi} \n'.format(s=row.stock, p=np.round(row.price,1), rsi=np.round(row.rsi, 1)))

msg_formated = ' '.join(msgs)
message = msg_title + msg_header + msg_formated
bot.send_message(message)
