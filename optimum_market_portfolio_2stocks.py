import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Best example: AMD & CSCO

#### FUNCTIONS SECTION ####

def stock_download(ticker):
    stock = yf.download(tickers=ticker, period='1y', interval='1d')
    return stock

def pct_change(stock):
    column_pct_change = 'Close'
    stock_pc = stock[column_pct_change].pct_change()[1:]
    return stock_pc

def get_stock_stats(stock_pc):
    # 253 = days of one trading year
    mean = stock_pc.mean()*253 # yearly return
    variance = stock_pc.var()*253 # yearly variance
    std = np.sqrt(variance)*253 # yearly std
    return mean, variance, std

def get_2stocks_stats(stock1_pc, stock2_pc):
    covariance = np.cov(stock1_pc, stock2_pc)[0][1]*253
    correlation = np.corrcoef(stock1_pc, stock2_pc)[0][1]
    return covariance, correlation


#### DATA INPUT AND TRANSFORMATION SECTION ####

print('\n+----------------------------------------------------+')
print('|  OPTIMUM MARKET PORTFOLIO CALCULATOR (TWO STOCKS)  |')
print('+----------------------------------------------------+\n')

# stock 1
ticker1 = input('Ticker stock 1: ')
stock1 = stock_download(ticker1)
stock1_pc = pct_change(stock1)
stock1_mean, stock1_variance, stock1_std = get_stock_stats(stock1_pc)

# stock 2
ticker2 = input('Ticker stock 2: ')
stock2 = stock_download(ticker2)
stock2_pc = pct_change(stock2)
stock2_mean, stock2_variance, stock2_std = get_stock_stats(stock2_pc)

# covariance and correlation stats
covariance, correlation = get_2stocks_stats(stock1_pc, stock2_pc)

# risk free stock: 10 year US bond yield
rf_ticker = '^TNX'
print('Risk free asset: {} (10 year US bond yield, annualized)'.format(rf_ticker))
rf = stock_download(rf_ticker)
rf_pc = pct_change(rf)
rf_mean = rf_pc.mean()/10 # yearly

# portfolio table
step = 0.001 # steps of the percentage combination (rows of the portfolio table)
perc_of_stock1 = np.arange(0, 1+step, step).tolist()
table = {'% stock1': perc_of_stock1}
df_a = pd.DataFrame(table)
# profits of each portfolio combination
df_a['portfolio mean'] = (df_a['% stock1'] * stock1_mean + (1 - df_a['% stock1']) * stock2_mean)
# variance of each portfolio combination
df_a['portfolio variance'] = (((df_a['% stock1']) ** 2) * stock1_variance + ((1 - df_a['% stock1']) ** 2) * stock2_variance + 2 * ((df_a['% stock1']) * (1 - df_a['% stock1']) * covariance))
# standard deviation of each portfolio combination
df_a['portfolio std'] = (np.sqrt(df_a['portfolio variance']))

# Markowitz optimum market portfolio (omp) calculation
omp_formula_part1 = (stock1_mean - rf_mean) * stock2_variance - (stock2_mean - rf_mean) * covariance
omp_formula_part2 = (stock2_mean - rf_mean) * stock1_variance + (stock1_mean - rf_mean) * stock2_variance - (stock1_mean + stock2_mean - 2 * rf_mean) * covariance
omp_perc_of_stock1 = omp_formula_part1/omp_formula_part2
if omp_perc_of_stock1 > 1:
    omp_perc_of_stock1 = 1
elif omp_perc_of_stock1 < 0:
    omp_perc_of_stock1 = 0
omp_perc_of_stock2 = (1 - omp_perc_of_stock1)

# omp stats
omp_mean = (omp_perc_of_stock1 * stock1_mean + omp_perc_of_stock2 * stock2_mean)
omp_variance = (omp_perc_of_stock1 ** 2) * stock1_variance + (omp_perc_of_stock2 ** 2) * stock2_variance + 2 * omp_perc_of_stock1 * omp_perc_of_stock2 * covariance
omp_std = np.sqrt(omp_variance)
sharpe_ratio = (omp_mean - rf_mean)/omp_std

# omp and rf combination table
step = 0.001 # steps of the percentage combination (rows of the portfolio table)
perc_of_omp = np.arange(0, 1+step, step).tolist()
table_b = {'% omp': perc_of_omp}
df_b = pd.DataFrame(table_b)
# profits of each portfolio combination
df_b['portfolio mean'] = rf_mean + df_b['% omp'] * (omp_mean - rf_mean)
# variance of each portfolio combination
df_b['portfolio variance'] = (((df_b['% omp']) ** 2) * omp_variance)
# standard deviation of each portfolio combination
df_b['portfolio std'] = (np.sqrt(df_b['portfolio variance']))


#### RESULT PRESENTATION SECTION ####

input('\nCalculation complete. Press Enter to show results ')

print("\n__PER ASSET RESULTS__")
table1 = {' ': ['mean:', 'variance:', 'std:'], ticker1: [stock1_mean, stock1_variance, stock1_std], ticker2: [stock2_mean, stock2_variance, stock2_std], rf_ticker: [rf_mean, 0, 0]}
df1 = pd.DataFrame(table1)
df1[ticker1] = df1[ticker1].round(3)
df1[ticker2] = df1[ticker2].round(3)
df1[rf_ticker] = df1[rf_ticker].round(5)
print(df1.to_string(index=False))
print(' covariance (stocks): ', covariance.round(6))
print('correlation (stocks): ', correlation.round(6))

print('\n__OPTIMUM MARKET PORTFOLIO__')
table2 = {'% ticker': ['% @ {}:'.format(ticker1), '% @ {}:'.format(ticker2), 'portfolio mean:', 'portfolio variance:', 'portfolio std:'], 'data': [omp_perc_of_stock1*100, omp_perc_of_stock2*100, omp_mean, omp_variance, omp_std]}
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
    X1 = df_a['portfolio std']
    Y1 = df_a['portfolio mean']
    X2 = df_b['portfolio std']
    Y2 = df_b['portfolio mean']
    plt.scatter(X2, Y2, color='gold', s=3)
    plt.scatter(X1, Y1, color='slategray', s=3)
    plt.scatter(df_a['portfolio std'].head(1), df_a['portfolio mean'].head(1), color='blue')
    plt.scatter(df_a['portfolio std'].tail(1), df_a['portfolio mean'].tail(1), color='blue')
    ax.plot(omp_std, omp_mean, "ro")
    plt.xlabel('standard deviation')
    plt.ylabel('mean')
    plt.text(omp_std, omp_mean, 'Optimum Market Portfolio')
    plt.text(df_a['portfolio std'].head(1), df_a['portfolio mean'].head(1), ticker2)
    plt.text(df_a['portfolio std'].tail(1), df_a['portfolio mean'].tail(1), ticker1)
    plt.tight_layout()
    plt.show()
    plt.close()
    print('\nProcess finished')
else:
    print('\nProcess finished')