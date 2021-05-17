import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#### FUNCTIONS SECTION ####

def stock_download(ticker):
    stock = yf.download(tickers=ticker, period='1y', interval='1d')
    return stock

column_pct_change = 'Close'

def add_pct_change(stock):
    stock['{} pct. Change'.format(column_pct_change)] = stock[column_pct_change].pct_change()

def get_pct_change_wo_nan(stock):
    nan_array = np.isnan(stock['{} pct. Change'.format(column_pct_change)])
    not_nan_array = ~ nan_array
    stock_pc = stock['{} pct. Change'.format(column_pct_change)][not_nan_array]
    return stock_pc

def get_stock_stats(stock_pc):
    mean = stock_pc.mean() # mean daily profits
    variance = stock_pc.var()
    std = np.sqrt(variance)
    return mean, variance, std

def get_yearly_stats(mean, variance):
    # 253 = days of one trading year
    yr_mean = mean*253 # yearly mean profits
    yr_variance = variance*253 # yearly variance
    yr_std = np.sqrt(yr_variance) # yearly standard deviation
    return yr_mean, yr_variance, yr_std

def get_2stocks_stats(stock1_pc, stock2_pc):
    covariance = np.cov(stock1_pc, stock2_pc)[0][1]
    correlation = np.corrcoef(stock1_pc, stock2_pc)[0][1]
    return covariance, correlation


#### DATA INPUT AND TRANSFORMATION SECTION ####

print('\n+------------------------------------------------------+')
print('|  MINIMUM VARIANCE PORTFOLIO CALCULATOR (TWO STOCKS)  |')
print('+------------------------------------------------------+\n')

# stock 1
ticker1 = input('Ticker stock 1: ')
stock1 = stock_download(ticker1)
add_pct_change(stock1)
stock1_pc = get_pct_change_wo_nan(stock1)
stock1_mean, stock1_variance, stock1_std = get_stock_stats(stock1_pc)
stock1_yr_mean, stock1_yr_variance, stock1_yr_std = get_yearly_stats(stock1_mean, stock1_variance)

# stock 2
ticker2 = input('Ticker stock 2: ')
stock2 = stock_download(ticker2)
add_pct_change(stock2)
stock2_pc = get_pct_change_wo_nan(stock2)
stock2_mean, stock2_variance, stock2_std = get_stock_stats(stock2_pc)
stock2_yr_mean, stock2_yr_variance, stock2_yr_std = get_yearly_stats(stock2_mean, stock2_variance)

# covariance and correlation stats
covariance, correlation = get_2stocks_stats(stock1_pc, stock2_pc)

# portfolio table
step = 0.001 # steps of the percentage combination (rows of the portfolio table)
perc_of_stock1 = np.arange(0, 1+step, step).tolist()
table = {'perc_of_stock1': perc_of_stock1}
df = pd.DataFrame(table)
# profits of each portfolio combination
df['portfolio_mean'] = (df['perc_of_stock1'] * stock1_yr_mean + (1 - df['perc_of_stock1']) * stock2_yr_mean)
# variance of each portfolio combination
df['portfolio_variance'] = (((df['perc_of_stock1']) ** 2) * stock1_yr_variance + ((1 - df['perc_of_stock1']) ** 2) * stock2_yr_variance + 2 * ((df['perc_of_stock1']) * (1 - df['perc_of_stock1']) * correlation * stock1_yr_std * stock2_yr_std))
# standard deviation of each portfolio combination
df['portfolio_std'] = (np.sqrt(df['portfolio_variance']))

# Markowitz minimum variance portfolio (mvp) calculation
mvp_perc_of_stock1 = (stock2_yr_variance - correlation * stock1_yr_std * stock2_yr_std) / (stock1_yr_variance + stock2_yr_variance - 2 * correlation * stock1_yr_std * stock2_yr_std)
if mvp_perc_of_stock1 > 1:
    mvp_perc_of_stock1 = 1
elif mvp_perc_of_stock1 < 0:
    mvp_perc_of_stock1 = 0
mvp_perc_of_stock2 = (1 - mvp_perc_of_stock1)

# mvp stats
mvp_mean = (mvp_perc_of_stock1 * stock1_yr_mean + mvp_perc_of_stock2 * stock2_yr_mean)
mvp_variance = (mvp_perc_of_stock1 ** 2) * stock1_yr_variance + (mvp_perc_of_stock2 ** 2) * stock2_yr_variance + 2 * mvp_perc_of_stock1 * mvp_perc_of_stock2 * correlation * stock1_yr_std * stock2_yr_std
mvp_std = np.sqrt(mvp_variance)


#### RESULT PRESENTATION SECTION ####

input('\nCalculation complete. Press Enter to show results ')

print("\n__PER STOCK RESULTS__")
table1 = {' ': ['mean:', 'variance:', 'std:'], ticker1: [(stock1_yr_mean), stock1_yr_variance, stock1_yr_std], ticker2: [stock2_yr_mean, stock2_yr_variance, stock2_yr_std]}
df1 = pd.DataFrame(table1)
df1[ticker1] = df1[ticker1].round(3)
df1[ticker2] = df1[ticker2].round(3)
print(df1.to_string(index=False))
print(' covariance: ', covariance.round(6))
print('correlation: ', correlation.round(6))

print('\n__MINIMUM VARIANCE PORTFOLIO__')
table2 = {'% ticker': ['% @ {}:'.format(ticker1), '% @ {}:'.format(ticker2), 'portfolio mean:', 'portfolio variance:', 'portfolio std:'], 'data': [mvp_perc_of_stock1*100, mvp_perc_of_stock2*100, mvp_mean, mvp_variance, mvp_std]}
df2 = pd.DataFrame(table2)
df2['data'] = df2['data'].round(3)
print(df2.to_string(index=False, header=False))


#### GRAPHIC REPRESENTATION SECTION ####
graphic = input('\nGraphic representation? (Y/N) ')

if graphic == 'Y' or graphic == 'YES' or graphic == 'y' or graphic == 'yes':
    ax = plt.subplot()
    ax.grid()
    ax.set_axisbelow(True)
    X = df['portfolio_std']
    Y = df['portfolio_mean']
    plt.scatter(X, Y, color='slategray', s=3)
    ax.plot(mvp_std, mvp_mean, "ro")
    plt.xlabel('standard deviation')
    plt.ylabel('mean')
    ax.annotate('Minimum Variance Portfolio', xy = (mvp_std, mvp_mean), xycoords = 'data', xytext = (mvp_std + mvp_std*0.025, mvp_mean))
    plt.tight_layout()
    ax.set_ylim(ymin=0)
    ax.set_xlim(xmin=0)
    plt.show()
    plt.close()
    print('\nProcess finished')
else:
    print('\nProcess finished')