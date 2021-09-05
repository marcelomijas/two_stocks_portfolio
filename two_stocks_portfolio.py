import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


## FUNCTIONS SECTION

def stock_download(ticker):
    stock = yf.download(tickers=ticker, period='1y', interval='1d') # 1 year period on 1 day intervals
    return stock[0:252] # [0:252] makes all stocks df the same length

def pct_change(stock):
    column_pct_change = 'Close' # uses the close price to calculate the percent change
    stock_pc = stock[column_pct_change].pct_change()[1:]
    return stock_pc

def get_stock_stats(stock_pc):
    # 252 = days of one trading year
    mean = stock_pc.mean()*252 # yearly return
    variance = stock_pc.var()*252 # yearly variance
    std = np.sqrt(variance)*252 # yearly standard deviation
    return mean, variance, std

def get_2stocks_stats(stock1_pc, stock2_pc):
    covariance = np.cov(stock1_pc, stock2_pc)[0][1]*252
    correlation = np.corrcoef(stock1_pc, stock2_pc)[0][1]
    return covariance, correlation


## DATA INPUT AND TRANSFORMATION SECTION

print('\n+---------------------------------+')
print('|  TWO STOCKS PORTFOLIO ANALYSIS  |')
print('+---------------------------------+\n')

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

# portfolio table (pt)
step = 0.001 # steps of the percentage combination (rows of the portfolio table)
perc_of_stock1 = np.arange(0, 1+step, step).tolist()
pt = {'% at stock1': perc_of_stock1}
df_pt = pd.DataFrame(pt)
# profits of each portfolio combination
df_pt['portfolio mean'] = (df_pt['% at stock1'] * stock1_mean + (1 - df_pt['% at stock1']) * stock2_mean)
# variance of each portfolio combination
df_pt['portfolio variance'] = (((df_pt['% at stock1']) ** 2) * stock1_variance + ((1 - df_pt['% at stock1']) ** 2) * stock2_variance + 2 * ((df_pt['% at stock1']) * (1 - df_pt['% at stock1']) * covariance))
# standard deviation of each portfolio combination
df_pt['portfolio std'] = (np.sqrt(df_pt['portfolio variance']))

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
mvp_sharpe_ratio = (mvp_mean - rf_mean)/mvp_std

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
omp_sharpe_ratio = (omp_mean - rf_mean)/omp_std

# omp and rf combination table
step = 0.001 # steps of the percentage combination (rows of the portfolio table)
perc_of_omp = np.arange(0, 2+step, step).tolist()
omp_rf = {'% at omp': perc_of_omp}
df_omp_rf = pd.DataFrame(omp_rf)
# profits of each portfolio combination
df_omp_rf['portfolio mean'] = rf_mean + df_omp_rf['% at omp'] * (omp_mean - rf_mean)
# variance of each portfolio combination
df_omp_rf['portfolio variance'] = (((df_omp_rf['% at omp']) ** 2) * omp_variance)
# standard deviation of each portfolio combination
df_omp_rf['portfolio std'] = (np.sqrt(df_omp_rf['portfolio variance']))


## TABLE OF RESULTS

input('\nCalculation complete. Press Enter to show results ')

print("\nPER STOCK STATS\n---------------")
table1 = {' ': ['Mean:', 'Variance:', 'Std. Dev.:'],
          ticker1: [stock1_mean, stock1_variance, stock1_std],
          ticker2: [stock2_mean, stock2_variance, stock2_std]}
df1 = pd.DataFrame(table1)
df1[ticker1] = df1[ticker1].round(3)
df1[ticker2] = df1[ticker2].round(3)
print(df1.to_string(index=False))
print(' Covariance: ', covariance.round(6))
print('Correlation: ', correlation.round(6))

print('\nMINIMUM VARIANCE PORTFOLIO STATS\n--------------------------------')
table2 = {'% at ticker': ['% at {}:'.format(ticker1),
                          '% at {}:'.format(ticker2),
                          'Mean:',
                          'Variance:',
                          'Std. Dev.:'],
          'data': [mvp_perc_of_stock1*100, mvp_perc_of_stock2*100, mvp_mean, mvp_variance, mvp_std]}
df2 = pd.DataFrame(table2)
df2['data'] = df2['data'].round(3)
print(df2.to_string(index=False, header=False))
print('Sharpe ratio: ', round(mvp_sharpe_ratio, 3))

print('\nOPTIMUM MARKET PORTFOLIO STATS\n------------------------------')
table3 = {'% at ticker': ['% at {}:'.format(ticker1),
                          '% at {}:'.format(ticker2),
                          'Mean:',
                          'Variance:',
                          'Std. Dev.:'],
          'data': [omp_perc_of_stock1*100, omp_perc_of_stock2*100, omp_mean, omp_variance, omp_std]}
df3 = pd.DataFrame(table3)
df3['data'] = df3['data'].round(3)
print(df3.to_string(index=False, header=False))
print('Sharpe ratio: ', round(omp_sharpe_ratio, 3))


## GRAPHIC REPRESENTATION

graphic = input('\nGraphic representation? Y/[N] ')

if graphic == 'Y' or graphic == 'YES' or graphic == 'y' or graphic == 'yes':
    ax = plt.subplot()
    ax.grid()
    ax.set_axisbelow(True)
    X = df_pt['portfolio std']
    Y = df_pt['portfolio mean']
    Xa = df_omp_rf['portfolio std']
    Ya = df_omp_rf['portfolio mean']
    plt.scatter(Xa, Ya, color='black', s=0.25)
    plt.scatter(X, Y, color='slategray', s=2)
    plt.scatter(df_pt['portfolio std'].head(1), df_pt['portfolio mean'].head(1), color='blue', s=15)
    plt.scatter(df_pt['portfolio std'].tail(1), df_pt['portfolio mean'].tail(1), color='blue', s=15)
    ax.plot(mvp_std, mvp_mean, "ro", label = 'Minimum Variance Portfolio')
    ax.plot(omp_std, omp_mean, "go", label = 'Optimum Market Portfolio')
    ax.plot(0, rf_mean, "yo")
    plt.xlabel('Risk (standard deviation)')
    plt.ylabel('Return (mean)')
    plt.text(df_pt['portfolio std'].head(1), df_pt['portfolio mean'].head(1), ticker2)
    plt.text(df_pt['portfolio std'].tail(1), df_pt['portfolio mean'].tail(1), ticker1)
    ax.text(0, rf_mean, rf_ticker)
    plt.tight_layout()
    ax.set_xlim(mvp_std*(1-0.05))
    plt.legend(loc="upper left")
    plt.show()
    plt.close()
    print('\nProcess finished')
else:
    print('\nProcess finished')