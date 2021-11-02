import ccxt
import pandas as pd
from datetime import datetime



exchange = ccxt.binance()

bars = exchange.fetch_ohlcv('ETH/EUR',timeframe='15m', limit=30)

df = pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

df['previous_close'] = df['close'].shift(1)
df['high-low'] = df['high'] - df['low']
df['high-pc'] = df['high'] - df['previous_close']
df['low-pc'] = df['low'] - df['previous_close']
#basic upperband = [(high + low) / 2 + (multiplier * atr)]
#basic lowerband = [(high + low) / 2 - (multiplier * atr)]

print(df)


