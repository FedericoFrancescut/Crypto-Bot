import os
import sys
import time
from datetime import datetime
from pprint import pprint

import ccxt

exchange = ccxt.binance({})

print(exchange.fetch_ticker("BTC/EUR"))