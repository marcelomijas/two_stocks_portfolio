import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
from os import system

# avg = average
# stdev = standard deviation
# var = variance
# covar = covariance
# correl = correlation
# rf = risk-free asset
# rp = risk premium
# w = weight
# Sr = Sharpe ratio
# MIN = minimum-variance portfolio
# O = tangency portfolio (optimal portfolio)

banner = r"""
 ______                    __           __      
/_  __/    _____      ___ / /____  ____/ /__ ___
 / / | |/|/ / _ \    (_-</ __/ _ \/ __/  '_/(_-<
/_/  |__,__/\___/ __/___/\__/\___/\__/_/\_\/___/
   ___  ___  ____/ /_/ _/__  / (_)__            
  / _ \/ _ \/ __/ __/ _/ _ \/ / / _ \           
 / .__/\___/_/  \__/_/ \___/_/_/\___/           
/_/                                             
Statistics are calculated as monthly
"""


def input_tickers():
    tickers = []
    for i in range(2):
        try:
            ticker = input(f"Ticker symbol of asset {i+1}: ")
            ticker_info = yf.Ticker(ticker).info
            print("\t", ticker_info["longName"])
            tickers.append(ticker_info["symbol"])
        except:
            input("Invalid ticker symbol\nProgram finished ")
            exit()
    return tickers


def download_rf(ticker: str = "^TNX"):
    print(f"Risk-free asset: {ticker}")
    ticker_info = yf.Ticker(ticker).info
    print("\t", ticker_info["longName"])
    rf = ticker_info["previousClose"] / (10 * 12)  # monthly risk-free return
    return rf


def download_assets(tickers: list):
    print(f"Downloading assets: {tickers}")
    assets_hist_close = yf.download(tickers=tickers, period="5y", interval="1mo")[
        "Close"
    ]
    return assets_hist_close


def assets_stats(assets_hist_close: pd.DataFrame):
    assets_retruns = assets_hist_close.pct_change() * 100
    avg = assets_retruns.mean()  # monthly return
    stdev = assets_retruns.std()  # montly risk
    covar = assets_retruns.cov().iloc[0, 1]
    correl = assets_retruns.corr().iloc[0, 1]
    return avg, stdev, covar, correl


def minimum_variance_portfolio(stdev, covar):
    tickers = stdev.index
    var_1, var_2 = stdev.iloc[0] ** 2, stdev.iloc[1] ** 2
    w_1 = (var_2 - covar) / (var_1 + var_2 - 2 * covar)
    if w_1 > 1:
        w_1 = 1
    elif w_1 < 0:
        w_1 = 0
    w_2 = 1 - w_1
    return pd.DataFrame([w_1, w_2], index=tickers, columns=["weigths"])


def tangency_portfolio(avg, stdev, covar, rf):
    tickers = avg.index
    avg_1, avg_2 = avg.iloc[0], avg.iloc[1]
    var_1, var_2 = stdev.iloc[0] ** 2, stdev.iloc[1] ** 2
    rp_1, rp_2 = avg_1 - rf, avg_2 - rf
    w_1 = (rp_1 * var_2 - rp_2 * covar) / (
        rp_1 * var_2 + rp_2 * var_1 - (rp_1 + rp_2) * covar
    )
    if w_1 > 1:
        w_1 = 1
    elif w_1 < 0:
        w_1 = 0
    w_2 = 1 - w_1
    return pd.DataFrame([w_1, w_2], index=tickers, columns=["weigths"])


def portfolio_stats(avg, stdev, covar, weights):
    avg_1, avg_2 = avg.iloc[0], avg.iloc[1]
    stdev_1, stdev_2 = stdev.iloc[0], stdev.iloc[1]
    w_1, w_2 = weights.iloc[0].values, weights.iloc[1].values
    avg_p = w_1 * avg_1 + w_2 * avg_2
    var_p = (w_1 * stdev_1) ** 2 + (w_2 * stdev_2) ** 2 + 2 * w_1 * w_2 * covar
    stdev_p = np.sqrt(var_p)
    return avg_p[0], stdev_p[0]


def sharpe_ratio(avg, stdev, rf):
    Sr = (avg - rf) / stdev
    return Sr


def portfolio_table(avg, stdev, covar, step: float = 0.001):
    avg_1, avg_2 = avg.iloc[0], avg.iloc[1]
    stdev_1, stdev_2 = stdev.iloc[0], stdev.iloc[1]
    pt = pd.DataFrame({"w_1": np.arange(0, 1 + step, step).tolist()})
    pt["w_2"] = 1 - pt["w_1"]
    pt["avg"] = pt["w_1"] * avg_1 + pt["w_2"] * avg_2
    pt["var"] = (
        (pt["w_1"] * stdev_1) ** 2
        + (pt["w_2"] * stdev_2) ** 2
        + 2 * pt["w_1"] * pt["w_2"] * covar
    )
    pt["stdev"] = np.sqrt(pt["var"])
    return pt


def main():
    print(banner)
    tickers = input_tickers()  # not sorted!
    tickers.sort()
    assets_hist_close = download_assets(tickers)
    rf = download_rf()
    input("Download complete. Press Enter to perform the calculations ")
    system("cls")
    print(f"rf = {rf:.2f}")

    print("\nPerformance statistics:")
    avg, stdev, covar, correl = assets_stats(assets_hist_close)
    Sr = sharpe_ratio(avg, stdev, rf)
    print(
        pd.concat([avg, stdev, Sr], axis=1, keys=["avg", "stdev", "Sharpe"]).T.round(3)
    )
    print(f"covar  {covar:.3f}")
    print(f"correl {correl:.3f}")

    print("\nMinimum-variance portfolio:")
    w_MIN = minimum_variance_portfolio(stdev, covar)
    print(w_MIN.T.round(3))
    avg_MIN, stdev_MIN = portfolio_stats(avg, stdev, covar, w_MIN)
    Sr_MIN = sharpe_ratio(avg_MIN, stdev_MIN, rf)
    print(f"avg    {avg_MIN:.3f}")
    print(f"stdev  {stdev_MIN:.3f}")
    print(f"Sharpe {Sr_MIN:.3f}")

    print("\nTangency portfolio:")
    w_O = tangency_portfolio(avg, stdev, covar, rf)
    print(w_O.T.round(3))
    avg_O, stdev_O = portfolio_stats(avg, stdev, covar, w_O)
    Sr_O = sharpe_ratio(avg_O, stdev_O, rf)
    print(f"avg    {avg_O:.3f}")
    print(f"stdev  {stdev_O:.3f}")
    print(f"Sharpe {Sr_O:.3f}")

    do_plt = input("\nPlot the investment opportunity set? [Y/n] ")
    if do_plt not in ("n", "N", False, 0):
        pt = portfolio_table(avg, stdev, covar)
        plt.xlabel("Risk (standard deviation)")
        plt.ylabel("Return (average)")
        plt.scatter(pt["stdev"], pt["avg"], s=2, c="slategray")
        plt.scatter(
            stdev_MIN,
            avg_MIN,
            s=60,
            c="red",
            label="Minimum-variance portfolio",
        )
        plt.scatter(stdev_O, avg_O, s=40, c="green", label="Tangency portfolio")
        plt.scatter(
            pt["stdev"].tail(1),
            pt["avg"].tail(1),
            s=100,
            c="black",
            marker="1",
            label=avg.index[0],
        )
        plt.scatter(
            pt["stdev"].head(1),
            pt["avg"].head(1),
            s=100,
            c="black",
            marker="2",
            label=avg.index[1],
        )
        plt.legend()
        plt.grid()
        plt.show()
        plt.close()

    input("\nProgram finished ")


main()
