import ccxt
import pandas as pd
from datetime import datetime



exchange = ccxt.binance()

bars = exchange.fetch_ohlcv('ETH/EUR',timeframe='15m', limit=30)

df = pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

def tr(df):
    df['previous_close'] = df['close'].shift(1)
    df['high-low'] = df['high'] - df['low']
    df['high-pc'] = abs(df['high'] - df['previous_close'])
    df['low-pc'] = abs(df['low'] - df['previous_close'])
    tr = df[['high-low', 'high-pc', 'low-pc']].max(axis=1)

    return tr

def atr(df, period=14):
    df['tr'] = tr(df)
    the_atr = df['tr'].rolling(period).mean()

    return the_atr


#basic upperband = [(high + low) / 2 + (multiplier * atr)]
#basic lowerband = [(high + low) / 2 - (multiplier * atr)]

def supertrend(df, period=14, multiplier=3):
    print("Calculating Supertrend:")
    df['atr'] = atr(df, period=period)
    df['basic_upperband'] = ((df['high'] + df['low']) / 2 + (multiplier + df['atr']))
    df['basic_lowerband'] = ((df['high'] + df['low']) / 2 - (multiplier + df['atr']))

    print(df)

supertrend(df)


