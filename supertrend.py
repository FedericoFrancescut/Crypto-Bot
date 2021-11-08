import ccxt
import schedule
import time
import pandas as pd
pd.set_option('display.max_rows', None)
import warnings
warnings.filterwarnings('ignore')
from datetime import datetime
import config



exchange = ccxt.binance({
    'apiKey': config.BINANCE_API_KEY, 
    'secret': config.BINANCE_SECRET_KEY,
})

print(exchange.fetch_balance())

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

def supertrend(df, period=7, multiplier=3):
    print("Calculating Supertrend:")
    df['atr'] = atr(df, period=period)
    df['upperband'] = ((df['high'] + df['low']) / 2 + (multiplier + df['atr']))
    df['lowerband'] = ((df['high'] + df['low']) / 2 - (multiplier + df['atr']))
    df['in_uptrend'] = True


    for current in range(1, len(df.index)):
        previous = current - 1
        
        if df['close'][current] > df['upperband'][previous]:
            df['in_uptrend'][current] = True
        elif df['close'][current] < df['lowerband'][previous]:
            df['in_uptrend'][current] = False
        else:
            df['in_uptrend'][current] = df['in_uptrend'][previous]

            if df['in_uptrend'][current] and df['lowerband'][current] < df['lowerband'][previous]:
                df['lowerband'][current] = df['lowerband'][previous]

            if not df['in_uptrend'][current] and df['upperband'][current] > df['upperband'][previous]:
                df['upperband'][current] = df['upperband'][previous]

    return df
    

def check_signals(df):
    print("checking signals")
    print(df.tail(2))
    last_row_index = len(df.index) - 1
    previous_row_index = last_row_index - 1

    if not df['in_uptrend'][previous_row_index] and df['in_uptrend'][last_row_index]:
        print("changed to uptremd, BUY!!")
    
    if df['in_uptrend'][previous_row_index] and not df['in_uptrend'][last_row_index]:
        print("changed to downtrend, SELL!!")


def run_bot():
    print(f"fetching new bars for {datetime.now().isoformat()}")
    bars = exchange.fetch_ohlcv('ETH/EUR',timeframe='15m', limit=365) 
    df = pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    supertrend_data = supertrend(df)
    
    check_signals(supertrend_data)

schedule.every(2).seconds.do(run_bot)   



while True:
    schedule.run_pending()
    time.sleep(1)
