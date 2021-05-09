import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

print('Minimum variance portfolio calculator (two stocks)')
ticker1 = input('Ticker stock 1: ')
ticker2 = input('Ticker stock 2: ')

## minimum variance portfolio with two stocks

# stock 1
stock1 = yf.download(tickers=ticker1, period='1y', interval='1d')
stock1['Perc. Change'] = stock1['Close'].pct_change()

# stock 1 without NaN
nan_array = np.isnan(stock1['Perc. Change'])
not_nan_array = ~ nan_array
sk1_pc = stock1['Perc. Change'][not_nan_array]

# stock 1 stats
stock1_mean = sk1_pc.mean()
stock1_var = sk1_pc.var()
stock1_std = np.sqrt(stock1_var)

# stock 1, year stats
sk1_mean_yr = stock1_mean*254 # stock1 yearly return
sk1_var_yr = stock1_var*254 # stock 1 yearly variance
sk1_std_yr = np.sqrt(sk1_var_yr) # stock 1 yearly standard deviation



# stock 2
stock2 = yf.download(tickers=ticker2, period='1y', interval='1d')
stock2['Perc. Change'] = stock2['Close'].pct_change()

# stock 1 without NaN
nan_array = np.isnan(stock2['Perc. Change'])
not_nan_array = ~ nan_array
sk2_pc = stock2['Perc. Change'][not_nan_array]

# stock 2 stats
stock2_mean = sk2_pc.mean()
stock2_var = sk2_pc.var()
stock2_std = np.sqrt(stock2_var)

# stock 2, year stats
sk2_mean_yr = stock2_mean*254 # stock 2 yearly return
sk2_var_yr = stock2_var*254 # stock 2 yearly variance
sk2_std_yr = np.sqrt(sk2_var_yr) # stock 2 yearly standard deviation



# covariance and correlation stats
cov = np.cov(sk1_pc, sk2_pc)[0][1]
corr = np.corrcoef(sk1_pc, sk2_pc)[0][1]


# portfolio
step = 0.001 # steps of the percentage combination
perc_sk1 = np.arange(0, 1+step, step).tolist()

table = {'perc_sk1': perc_sk1}

df = pd.DataFrame(table)

# variance of each portfolio combination
df['portfolio_var'] = (((df['perc_sk1']) ** 2)*sk1_var_yr + ((1-df['perc_sk1']) ** 2)*sk2_var_yr + 2 * ((df['perc_sk1']) * (1-df['perc_sk1']) * corr * sk1_std_yr * sk2_std_yr))

# standard deviation of each portfolio combination
df['portfolio_std'] = (np.sqrt(df['portfolio_var']))

# investment return of each portfolio combination
df['portfolio_mean'] = (df['perc_sk1']*sk1_mean_yr + (1-df['perc_sk1'])*sk2_mean_yr)


## markov minimum variance portfolio

perc_mvp_sk1 = (sk2_var_yr - corr*sk1_std_yr*sk2_std_yr) / (sk1_var_yr + sk2_var_yr - 2*corr*sk1_std_yr*sk2_std_yr)
if perc_mvp_sk1 > 1:
    perc_mvp_sk1 = 1
elif perc_mvp_sk1 < 0:
    perc_mvp_sk1 = 0

perc_mvp_sk2 = (1 - perc_mvp_sk1)

mvp_mean = (perc_mvp_sk1*sk1_mean_yr + perc_mvp_sk2*sk2_mean_yr)
mvp_var = (perc_mvp_sk1**2)*sk1_var_yr + (perc_mvp_sk2**2)*sk2_var_yr + 2*perc_mvp_sk1*perc_mvp_sk2* corr*sk1_std_yr*sk2_std_yr
mvp_std = np.sqrt(mvp_var)

# results


print("__RESULTS__")
table1 = {' ': ['mean', 'variance', 'std'], 'stock1': [sk1_mean_yr, sk1_var_yr, sk1_std_yr], 'stock2': [sk2_mean_yr, sk1_var_yr, sk2_std_yr]}
df1 = pd.DataFrame(table1)
print(df1)
print('covariance: ', cov)
print('correlation: ', corr)
print()
print('__MINIMUM VARIANCE PORTFOLIO__')
print('% stock 1: ', round(perc_mvp_sk1*100, 2),'%')
print('% stock 2: ', round(perc_mvp_sk2*100, 2),'%')
print('mean mvp: ',mvp_mean)
print('var mvp: ',mvp_var)
print('std mvp: ',mvp_std)

# graphic representation

print()
graphic = input('Graphic representation? (Y/N) ')

if graphic == 'Y':
    ax = plt.subplot()
    ax.grid()
    X = df['portfolio_std']
    Y = df['portfolio_mean']
    plt.scatter(X, Y, s = 3)
    ax.plot(mvp_std, mvp_mean, "ro")
    plt.xlabel('standard deviation')
    plt.ylabel('mean')
    ax.annotate('Minimum Variance Portfolio', xy = (mvp_std, mvp_mean), xycoords = 'data', xytext = (mvp_std + mvp_std*0.05, mvp_mean))
    plt.show()
    plt.close()