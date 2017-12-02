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

forecast_col = 'Adj. Close'
df.fillna(-99999, inplace = True)                                                   # still drop any NaN information from the dta frame

forecast_out = int(math.ceil(0.01*len(df)))

df['label'] = df[forecast_col].shift(-forecast_out)
df.dropna(inplace = True)

x = np.array(df.drop(['label'], 1))                                                 # define X (features) to be the entire data frame except for the label column, converted to a numpy array
y = np.array(df['label'])                                                           # define y (labels) corresponding to X to be the label column of the dataframe, converted to a numpy array

x = preprocessing.scale(x)                                                          # use preprocessing module to do some preprocessing and scale X

x = x[:-forecast_out+1]
df.dropna(inplace = True)
y = np.array(df['label'])

print(len(x), len(y))
