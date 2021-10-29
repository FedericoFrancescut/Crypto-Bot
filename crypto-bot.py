import os
import sys
import time
from datetime import datetime
from pprint import pprint

import config
import ccxt
import pandas as pd
from ta import add_all_ta_features
from ta.utils import dropna
from ta.volatility import BollingerBands, AverageTrueRange

exchange = ccxt.binance({
    'apiKey': config.BINANCE_API_KEY,
    'secret': config.BINANCE_SECRET_KEY
})

print(exchange.fetch_ticker("BTC/EUR")['last'])

bars = exchange.fetch_ohlcv('ETH/EUR', limit=21)

df = pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])


bb_indicator = BollingerBands(close=df['close'], window=20, window_dev=2, )
df['upper_band'] = bb_indicator.bollinger_hband()
df['lower_band'] = bb_indicator.bollinger_lband()
df['moving_avarage'] = bb_indicator.bollinger_mavg()

atr_indicator = AverageTrueRange(df['high'], df['low'], df['close'])
df['atr'] = atr_indicator.average_true_range()

print(df)
