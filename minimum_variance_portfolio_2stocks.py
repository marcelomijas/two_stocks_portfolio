import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


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

print('\n+------------------------------------------------------+')
print('|  MINIMUM VARIANCE PORTFOLIO CALCULATOR (TWO STOCKS)  |')
print('+------------------------------------------------------+\n')

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

# portfolio table
step = 0.001 # steps of the percentage combination (rows of the portfolio table)
perc_of_stock1 = np.arange(0, 1+step, step).tolist()
table = {'% stock1': perc_of_stock1}
df = pd.DataFrame(table)
# profits of each portfolio combination
df['portfolio mean'] = (df['% stock1'] * stock1_mean + (1 - df['% stock1']) * stock2_mean)
# variance of each portfolio combination
df['portfolio variance'] = (((df['% stock1']) ** 2) * stock1_variance + ((1 - df['% stock1']) ** 2) * stock2_variance + 2 * ((df['% stock1']) * (1 - df['% stock1']) * covariance))
# standard deviation of each portfolio combination
df['portfolio std'] = (np.sqrt(df['portfolio variance']))

# Markowitz minimum variance portfolio (mvp) calculation
mvp_perc_of_stock1 = (stock2_variance - covariance) / (stock1_variance + stock2_variance - 2 * covariance)
if mvp_perc_of_stock1 > 1:
    mvp_perc_of_stock1 = 1
elif mvp_perc_of_stock1 < 0:
    mvp_perc_of_stock1 = 0
mvp_perc_of_stock2 = (1 - mvp_perc_of_stock1)

# mvp stats
mvp_mean = (mvp_perc_of_stock1 * stock1_mean + mvp_perc_of_stock2 * stock2_mean)
mvp_variance = (mvp_perc_of_stock1 ** 2) * stock1_variance + (mvp_perc_of_stock2 ** 2) * stock2_variance + 2 * mvp_perc_of_stock1 * mvp_perc_of_stock2 * covariance
mvp_std = np.sqrt(mvp_variance)


#### RESULT PRESENTATION SECTION ####

input('\nCalculation complete. Press Enter to show results ')

print("\n__PER STOCK RESULTS__")
table1 = {' ': ['mean:', 'variance:', 'std:'], ticker1: [stock1_mean, stock1_variance, stock1_std], ticker2: [stock2_mean, stock2_variance, stock2_std]}
df1 = pd.DataFrame(table1)
df1[ticker1] = df1[ticker1].round(3)
df1[ticker2] = df1[ticker2].round(3)
print(df1.to_string(index=False))
print(' covariance: ', covariance.round(6))
print('correlation: ', correlation.round(6))

print('\n__MINIMUM VARIANCE PORTFOLIO__')
table2 = {'% ticker': ['% at {}:'.format(ticker1), '% at {}:'.format(ticker2), 'portfolio mean:', 'portfolio variance:', 'portfolio std:'], 'data': [mvp_perc_of_stock1*100, mvp_perc_of_stock2*100, mvp_mean, mvp_variance, mvp_std]}
df2 = pd.DataFrame(table2)
df2['data'] = df2['data'].round(3)
print(df2.to_string(index=False, header=False))


#### GRAPHIC REPRESENTATION SECTION ####
graphic = input('\nGraphic representation? (Y/N) ')

if graphic == 'Y' or graphic == 'YES' or graphic == 'y' or graphic == 'yes':
    ax = plt.subplot()
    ax.grid()
    ax.set_axisbelow(True)
    X = df['portfolio std']
    Y = df['portfolio mean']
    plt.scatter(X, Y, color='slategray', s=3)
    plt.scatter(df['portfolio std'].head(1), df['portfolio mean'].head(1), color='blue')
    plt.scatter(df['portfolio std'].tail(1), df['portfolio mean'].tail(1), color='blue')
    ax.plot(mvp_std, mvp_mean, "ro")
    plt.xlabel('standard deviation')
    plt.ylabel('mean')
    plt.text(mvp_std, mvp_mean, 'Minimum Variance Portfolio')
    plt.text(df['portfolio std'].head(1), df['portfolio mean'].head(1), ticker2)
    plt.text(df['portfolio std'].tail(1), df['portfolio mean'].tail(1), ticker1)
    plt.tight_layout()
    plt.show()
    plt.close()
    print('\nProcess finished')
else:
    print('\nProcess finished')