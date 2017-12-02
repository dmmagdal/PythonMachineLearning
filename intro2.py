import pandas as pd
import quandl

df = quandl.get('WIKI/GOOGL');
df = df[['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume']]    # streamline data only to be the "adjusted" values (Values adjusted for stock splits)
df['HL_PCT'] = (df['Adj. High'] - df['Adj. Close'])/df['Adj. Close']*100.0      # high-low comparison
df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open'])/df['Adj. Open']*100.0   # percent change based on opening/closing prices

df = df[['Adj. Close', 'HL_PCT', 'PCT_change', 'Adj. Volume']]                  # new data frame to be printed out

print(df.head())
