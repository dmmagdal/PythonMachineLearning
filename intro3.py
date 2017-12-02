import pandas as pd
import quandl, math
import numpy as np
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression

df = quandl.get('WIKI/GOOGL');
df = df[['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume']]
df['HL_PCT'] = (df['Adj. High'] - df['Adj. Close'])/df['Adj. Close']*100.0
df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open'])/df['Adj. Open']*100.0

df = df[['Adj. Close', 'HL_PCT', 'PCT_change', 'Adj. Volume']]

forecast_col = 'Adj. Close'                                                     # create a forcast feature column for the prices
df.fillna(-99999, inplace = True)                                               # any NaN data is filled in with -99999

forecast_out = int(math.ceil(0.01*len(df)))                                     # forecast out 1% of length of data field

df['label'] = df[forecast_col].shift(-forecast_out)                             # forecast label 
df.dropna(inplace = True)

print(df.head())
