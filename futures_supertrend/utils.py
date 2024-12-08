import yfinance as yf
import pandas_ta as ta

# Load data function
def load_data(ticker, period="1y", interval="75m"):
    df = yf.download(ticker, period=period, interval=interval)
    return df

# Function to calculate Supertrend
def supertrend(df, period=10, multiplier=2):
    hl2 = (df['High'] + df['Low']) / 2
    atr = ta.ATR(df['High'], df['Low'], df['Close'], timeperiod=period)
    upperband = hl2 + (multiplier * atr)
    lowerband = hl2 - (multiplier * atr)
    
    final_upperband = upperband.copy()
    final_lowerband = lowerband.copy()
    
    for i in range(1, len(df)):
        if df['Close'][i] > final_upperband[i-1]:
            final_upperband[i] = max(upperband[i], final_upperband[i-1])
        else:
            final_upperband[i] = upperband[i]
        
        if df['Close'][i] < final_lowerband[i-1]:
            final_lowerband[i] = min(lowerband[i], final_lowerband[i-1])
        else:
            final_lowerband[i] = lowerband[i]
    
    return final_upperband, final_lowerband

# Function to calculate ADX
def adx(df, period=14):
    adx = ta.ADX(df['High'], df['Low'], df['Close'], timeperiod=period)
    di_plus = ta.PLUS_DI(df['High'], df['Low'], df['Close'], timeperiod=period)
    di_minus = ta.MINUS_DI(df['High'], df['Low'], df['Close'], timeperiod=period)
    return adx, di_plus, di_minus
