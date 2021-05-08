import plotly.graph_objs as go
import yfinance as yf
import math
import numpy as np
import pandas as pd

# minimum variance portfolio with two stocks

# stock 1
stock1 = yf.download(tickers='AMD', period='1y', interval='1d')
stock1['Perc. Change'] = stock1['Close'].pct_change()
stock1_mean = stock1['Close'].mean()
stock1_variance = stock1['Close'].var()
stock1_std = math.sqrt(stock1_variance)

# stock 1, year statistics
sk1_yr = stock1_mean*254 # stock1 yearly return
sk1_yr = stock1_variance*254 # stock 1 yearly variance
sk1_yr = stock1_std*254 # stock 1 yearly standard deviation

# stock 1 without NaN
nan_array = np.isnan(stock1['Perc. Change'])
not_nan_array = ~ nan_array
sk1_pc = stock1['Perc. Change'][not_nan_array]

# stock 2
stock2 = yf.download(tickers='NVDA', period='1y', interval='1d')
stock2['Perc. Change'] = stock2['Close'].pct_change()
stock2_mean = stock2['Close'].mean()
stock2_variance = stock2['Close'].var()
stock2_std = math.sqrt(stock2_variance)

# stock 2, year statistics
sk2_yr = stock2_mean*254 # stock 2 yearly return
sk2_yr = stock1_variance*254 # stock 2 yearly variance
sk2_yr = stock1_std*254 # stock 2 yearly standard deviation

# stock 1 without NaN
nan_array = np.isnan(stock2['Perc. Change'])
not_nan_array = ~ nan_array
sk2_pc = stock2['Perc. Change'][not_nan_array]

# covariance and correlation stats
cov = np.cov(sk1_pc, sk2_pc)[0][1]
corr = np.corrcoef(sk1_pc, sk2_pc)[0][1]


# portfolio
step = 0.1
perc_sk1 = np.arange(0, 1+step, step).tolist()

table = {'perc_sk1': perc_sk1}

df = pd.DataFrame(table)

df['portfolio_variance'] = ((df['perc_sk1'])**2)

print(df)
