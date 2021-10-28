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

bars = exchange.fetch_ohlcv('ETH/EUR', limit=20)

for bar in bars:
    print(bar)

df = pd.DataFrame(bars, columns=['timestamp','high','low','close','volume'])
print(df)
#bb_indicator = BollingerBands()
