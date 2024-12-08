import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go

# Function to calculate Supertrend
def supertrend(df, period, multiplier):
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

# Load data for NIFTY
def load_data(ticker):
    df = yf.download(ticker, period="1y", interval="75m")
    return df

# Plot the strategy on the chart
def plot_chart(df, supertrend_upper, supertrend_lower, adx, di_plus, di_minus):
    fig = go.Figure()

    # Candlestick chart
    fig.add_trace(go.Candlestick(x=df.index,
                                 open=df['Open'], high=df['High'],
                                 low=df['Low'], close=df['Close'], 
                                 name='Candlesticks'))

    # Supertrend
    fig.add_trace(go.Scatter(x=df.index, y=supertrend_upper, 
                             mode='lines', line={'color': 'green'}, 
                             name='Supertrend Upper'))
    fig.add_trace(go.Scatter(x=df.index, y=supertrend_lower, 
                             mode='lines', line={'color': 'red'}, 
                             name='Supertrend Lower'))

    # ADX
    fig.add_trace(go.Scatter(x=df.index, y=adx, 
                             mode='lines', line={'color': 'blue'}, 
                             name='ADX'))
    fig.add_trace(go.Scatter(x=df.index, y=di_plus, 
                             mode='lines', line={'color': 'green'}, 
                             name='DI+'))
    fig.add_trace(go.Scatter(x=df.index, y=di_minus, 
                             mode='lines', line={'color': 'red'}, 
                             name='DI-'))

    fig.update_layout(title="Futures Supertrend Strategy",
                      xaxis_title="Date",
                      yaxis_title="Price")
    st.plotly_chart(fig)

# Main Streamlit App
def main():
    st.title("Futures Supertrend Strategy")

    # Choose the instrument
    ticker = st.selectbox("Select instrument", ['^NSEBANK', '^NSEI'])

    # Load data
    df = load_data(ticker)

    # Calculate indicators
    supertrend_upper, supertrend_lower = supertrend(df, 10, 2)
    adx, di_plus, di_minus = adx(df)

    # Plot the data
    plot_chart(df, supertrend_upper, supertrend_lower, adx, di_plus, di_minus)

    # Display the strategy logic
    st.subheader("Strategy Logic")
    st.write("""
    - **Long Trade**: 
        - Entry: Price > Supertrend (10,2) and ADX (DI+ > DI-)
        - Exit: Price < Supertrend (10,2)
    - **Short Trade**: 
        - Entry: Price < Supertrend (10,2) and ADX (DI- > DI+)
        - Exit: Price > Supertrend (10,2)
    """)

if __name__ == "__main__":
    main()
