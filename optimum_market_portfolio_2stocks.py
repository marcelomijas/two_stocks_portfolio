import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Best example: AMD & CSCO

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

print('\n+----------------------------------------------------+')
print('|  OPTIMUM MARKET PORTFOLIO CALCULATOR (TWO STOCKS)  |')
print('+----------------------------------------------------+\n')

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

# risk free stock: 10 year US bond yield
rf_ticker = '^TNX'
print('Risk free asset: {} (10 year US bond yield, annualized)'.format(rf_ticker))
rf = stock_download(rf_ticker)
add_pct_change(rf)
rf_pc = get_pct_change_wo_nan(rf)
rf_mean = rf_pc.mean() # 10 year
rf_yr_mean = rf_mean/10 # yearly

# covariance and correlation stats
covariance, correlation = get_2stocks_stats(stock1_pc, stock2_pc)

# portfolio table
step = 0.001 # steps of the percentage combination (rows of the portfolio table)
perc_of_stock1 = np.arange(0, 1+step, step).tolist()
table_a = {'perc_of_stock1': perc_of_stock1}
df_a = pd.DataFrame(table_a)
# profits of each portfolio combination
df_a['portfolio_mean'] = (df_a['perc_of_stock1'] * stock1_yr_mean + (1 - df_a['perc_of_stock1']) * stock2_yr_mean)
# variance of each portfolio combination
df_a['portfolio_variance'] = (((df_a['perc_of_stock1']) ** 2) * stock1_yr_variance + ((1 - df_a['perc_of_stock1']) ** 2) * stock2_yr_variance + 2 * ((df_a['perc_of_stock1']) * (1 - df_a['perc_of_stock1']) * correlation * stock1_yr_std * stock2_yr_std))
# standard deviation of each portfolio combination
df_a['portfolio_std'] = (np.sqrt(df_a['portfolio_variance']))

# Markowitz optimum market portfolio (omp) calculation
omp_formula_part1 = (stock1_yr_mean - rf_yr_mean) * stock2_yr_variance - (stock2_yr_mean - rf_yr_mean) * (correlation * stock1_yr_std * stock2_yr_std)
omp_formula_part2 = (stock2_yr_mean - rf_yr_mean) * stock1_yr_variance + (stock1_yr_mean - rf_yr_mean) * stock2_yr_variance - (stock1_yr_mean + stock2_yr_mean - 2 * rf_yr_mean) * (correlation * stock1_yr_std * stock2_yr_std)
omp_perc_of_stock1 = omp_formula_part1/omp_formula_part2
if omp_perc_of_stock1 > 1:
    omp_perc_of_stock1 = 1
elif omp_perc_of_stock1 < 0:
    omp_perc_of_stock1 = 0
omp_perc_of_stock2 = (1 - omp_perc_of_stock1)

# omp stats
omp_mean = (omp_perc_of_stock1 * stock1_yr_mean + omp_perc_of_stock2 * stock2_yr_mean)
omp_variance = (omp_perc_of_stock1 ** 2) * stock1_yr_variance + (omp_perc_of_stock2 ** 2) * stock2_yr_variance + 2 * omp_perc_of_stock1 * omp_perc_of_stock2 * correlation * stock1_yr_std * stock2_yr_std
omp_std = np.sqrt(omp_variance)
sharpe_ratio = (omp_mean - rf_yr_mean)/omp_std

# omp and rf combination table
step = 0.001 # steps of the percentage combination (rows of the portfolio table)
perc_of_omp = np.arange(0, 1+step, step).tolist()
table_b = {'perc_of_omp': perc_of_omp}
df_b = pd.DataFrame(table_b)
# profits of each portfolio combination
df_b['portfolio_mean'] = rf_yr_mean + df_b['perc_of_omp'] * (omp_mean - rf_yr_mean)
# variance of each portfolio combination
df_b['portfolio_variance'] = (((df_b['perc_of_omp']) ** 2) * omp_variance)
# standard deviation of each portfolio combination
df_b['portfolio_std'] = (np.sqrt(df_b['portfolio_variance']))


#### RESULT PRESENTATION SECTION ####

input('\nCalculation complete. Press Enter to show results ')

print("\n__PER ASSET RESULTS__")
table1 = {' ': ['mean:', 'variance:', 'std:'], ticker1: [(stock1_yr_mean), stock1_yr_variance, stock1_yr_std], ticker2: [stock2_yr_mean, stock2_yr_variance, stock2_yr_std], rf_ticker: [rf_yr_mean, 0, 0]}
df1 = pd.DataFrame(table1)
df1[ticker1] = df1[ticker1].round(3)
df1[ticker2] = df1[ticker2].round(3)
df1[rf_ticker] = df1[rf_ticker].round(5)
print(df1.to_string(index=False))
print(' covariance (stocks): ', covariance.round(6))
print('correlation (stocks): ', correlation.round(6))

print('\n__OPTIMUM MARKET PORTFOLIO__')
table2 = {'% ticker': ['% @ {}:'.format(ticker1), '% @ {}:'.format(ticker2), 'omp mean:', 'omp variance:', 'omp std:'], 'data': [omp_perc_of_stock1*100, omp_perc_of_stock2*100, omp_mean, omp_variance, omp_std]}
df2 = pd.DataFrame(table2)
df2['data'] = df2['data'].round(3)
print(df2.to_string(index=False, header=False))
print('Sharpe ratio: ', round(sharpe_ratio, 3))


#### GRAPHIC REPRESENTATION SECTION ####
graphic = input('\nGraphic representation? (Y/N) ')

if graphic == 'Y' or graphic == 'YES' or graphic == 'y' or graphic == 'yes':
    ax = plt.subplot()
    ax.grid()
    ax.set_axisbelow(True)
    X1 = df_a['portfolio_std']
    Y1 = df_a['portfolio_mean']
    X2 = df_b['portfolio_std']
    Y2 = df_b['portfolio_mean']
    plt.scatter(X2, Y2, color='gold', s=3)
    plt.scatter(X1, Y1, color='slategray', s=3)
    ax.plot(omp_std, omp_mean, "ro")
    plt.xlabel('standard deviation')
    plt.ylabel('mean')
    ax.annotate('Optimum Market Portfolio', xy = (omp_std, omp_mean), xycoords = 'data', xytext = (omp_std + omp_std*0.025, omp_mean))
    plt.tight_layout()
    plt.show()
    plt.close()
    print('\nProcess finished')
else:
    print('\nProcess finished')