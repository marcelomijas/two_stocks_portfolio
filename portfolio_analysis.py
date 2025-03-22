import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
from os import system, name

# exp_ret = expected return
# std_dev = standard deviation
# var = variance
# cov = covariance
# corr = correlation
# rf = risk-free asset
# rp = risk premium
# w = portfolio weights
# sharpe = Sharpe ratio
# mvp = minimum-variance portfolio
# omp = tangency portfolio (optimal portfolio)

BANNER = r"""
 ______                    __           __      
/_  __/    _____      ___ / /____  ____/ /__ ___
 / / | |/|/ / _ \    (_-</ __/ _ \/ __/  '_/(_-<
/_/  |__,__/\___/ __/___/\__/\___/\__/_/\_\/___/
   ___  ___  ____/ /_/ _/__  / (_)__            
  / _ \/ _ \/ __/ __/ _/ _ \/ / / _ \           
 / .__/\___/_/  \__/_/ \___/_/_/\___/           
/_/                                             
"""

RF_TICKER = "^TNX"
PERIOD = "1y"
INTERVAL = "1wk"
PERIOD_MULTIPLIER = 52
RISK_FREE_DIVISOR = 10
SHORT_SELLING = False


def input_tickers() -> list[str]:
    """Prompt user to input ticker symbols for two assets."""
    tickers = []
    for i in range(2):
        try:
            ticker = input(f"Ticker symbol of asset {i+1}: ")
            ticker_info = yf.Ticker(ticker).info
            print("\t", ticker_info["longName"])
            tickers.append(ticker_info["symbol"])
        except AttributeError:
            input("Invalid ticker symbol\nProgram finished ")
            exit()
    return tickers


def download_rf(ticker: str = RF_TICKER) -> float:
    """Download risk-free asset data and return monthly risk-free return."""
    print(f"Risk-free asset: {ticker}")
    ticker_info = yf.Ticker(ticker).info
    print("\t", ticker_info["longName"])
    rf = ticker_info["previousClose"] / RISK_FREE_DIVISOR
    return rf


def download_assets(tickers: list[str]) -> pd.DataFrame:
    """Download historical close prices for the given tickers."""
    print(f"Downloading assets: {tickers}")
    hist_prices = yf.download(tickers=tickers, period=PERIOD, interval=INTERVAL)
    return hist_prices["Close"]


def assets_stats(
    assets_hist_close: pd.DataFrame,
) -> tuple[pd.Series, pd.Series, float, float]:
    """Calculate statistics for the given assets."""
    assets_retruns = assets_hist_close.pct_change() * 100
    exp_ret = assets_retruns.mean() * PERIOD_MULTIPLIER
    std_dev = assets_retruns.std() * np.sqrt(PERIOD_MULTIPLIER)
    cov = assets_retruns.cov().iloc[0, 1] * PERIOD_MULTIPLIER
    corr = assets_retruns.corr().iloc[0, 1]
    return exp_ret, std_dev, cov, corr


def minimum_variance_portfolio(std_dev: pd.Series, cov: float) -> pd.DataFrame:
    """Calculate the minimum-variance portfolio weights."""
    tickers = std_dev.index
    var_1, var_2 = std_dev.iloc[0] ** 2, std_dev.iloc[1] ** 2
    w_1 = (var_2 - cov) / (var_1 + var_2 - 2 * cov)
    if not SHORT_SELLING:
        if w_1 > 1:
            w_1 = 1
        elif w_1 < 0:
            w_1 = 0
    w_2 = 1 - w_1
    return pd.DataFrame([w_1, w_2], index=tickers, columns=["weigths"])


def tangency_portfolio(
    exp_ret: pd.Series, std_dev: pd.Series, cov: float, rf: float
) -> pd.DataFrame:
    """Calculate the tangency portfolio weights."""
    tickers = exp_ret.index
    exp_ret_1, exp_ret_2 = exp_ret.iloc[0], exp_ret.iloc[1]
    var_1, var_2 = std_dev.iloc[0] ** 2, std_dev.iloc[1] ** 2
    rp_1, rp_2 = exp_ret_1 - rf, exp_ret_2 - rf
    w_1 = (rp_1 * var_2 - rp_2 * cov) / (
        rp_1 * var_2 + rp_2 * var_1 - (rp_1 + rp_2) * cov
    )
    if not SHORT_SELLING:
        if w_1 > 1:
            w_1 = 1
        elif w_1 < 0:
            w_1 = 0
    w_2 = 1 - w_1
    return pd.DataFrame([w_1, w_2], index=tickers, columns=["weigths"])


def portfolio_stats(
    exp_ret: pd.Series, std_dev: pd.Series, cov: float, w: pd.DataFrame
) -> tuple[float, float]:
    """Calculate the expected return and standard deviation of the portfolio."""
    exp_ret_1, exp_ret_2 = exp_ret.iloc[0], exp_ret.iloc[1]
    std_dev_1, std_dev_2 = std_dev.iloc[0], std_dev.iloc[1]
    w_1, w_2 = w.iloc[0].values, w.iloc[1].values
    exp_ret_p = w_1 * exp_ret_1 + w_2 * exp_ret_2
    var_p = (w_1 * std_dev_1) ** 2 + (w_2 * std_dev_2) ** 2 + 2 * w_1 * w_2 * cov
    std_dev_p = np.sqrt(var_p)
    return exp_ret_p[0], std_dev_p[0]


def sharpe_ratio(exp_ret: pd.Series, std_dev: pd.Series, rf: float) -> float:
    """Calculate and return the Sharpe ratio."""
    return (exp_ret - rf) / std_dev


def portfolio_table(
    exp_ret: pd.Series, std_dev: pd.Series, cov: float, step: float = 0.001
) -> pd.DataFrame:
    """Generate a table of portfolio statistics."""
    exp_ret_1, exp_ret_2 = exp_ret.iloc[0], exp_ret.iloc[1]
    std_dev_1, std_dev_2 = std_dev.iloc[0], std_dev.iloc[1]
    table = pd.DataFrame({"w_1": np.arange(0, 1 + step, step).tolist()})
    table["w_2"] = 1 - table["w_1"]
    table["exp_ret"] = table["w_1"] * exp_ret_1 + table["w_2"] * exp_ret_2
    table["var"] = (
        (table["w_1"] * std_dev_1) ** 2
        + (table["w_2"] * std_dev_2) ** 2
        + 2 * table["w_1"] * table["w_2"] * cov
    )
    table["std_dev"] = np.sqrt(table["var"])
    return table


def main():
    """Main function to execute the portfolio analysis."""
    print(BANNER)
    tickers = input_tickers()
    tickers.sort()
    hist_prices = download_assets(tickers)
    rf = download_rf()
    input("Download complete. Press Enter to perform the calculations ")
    system("cls" if name == "nt" else "clear")
    print(f"rf = {rf:.2f}")

    print("\nPerformance statistics:")
    exp_ret, std_dev, cov, corr = assets_stats(hist_prices)
    sharpe = sharpe_ratio(exp_ret, std_dev, rf)
    print(
        pd.concat(
            [exp_ret, std_dev, sharpe],
            axis=1,
            keys=["Expected return", "Standard deviation", "Sharpe ratio"],
        ).T.round(3)
    )
    print(f"Covariance  {cov:.3f}")
    print(f"Correlation {corr:.3f}")

    print("\nMinimum-variance portfolio:")
    w_mvp = minimum_variance_portfolio(std_dev, cov)
    print(w_mvp.T.round(3))
    exp_ret_mvp, std_dev_mvp = portfolio_stats(exp_ret, std_dev, cov, w_mvp)
    sharpe_mvp = sharpe_ratio(exp_ret_mvp, std_dev_mvp, rf)
    print(f"Expected return     {exp_ret_mvp:.3f}")
    print(f"Standard deviation  {std_dev_mvp:.3f}")
    print(f"Sharpe ratio        {sharpe_mvp:.3f}")

    print("\nTangency portfolio:")
    w_omp = tangency_portfolio(exp_ret, std_dev, cov, rf)
    print(w_omp.T.round(3))
    exp_ret_omp, std_dev_omp = portfolio_stats(exp_ret, std_dev, cov, w_omp)
    sharpe_omp = sharpe_ratio(exp_ret_omp, std_dev_omp, rf)
    print(f"Expected return     {exp_ret_omp:.3f}")
    print(f"Standard deviation  {std_dev_omp:.3f}")
    print(f"Sharpe ratio        {sharpe_omp:.3f}")

    plot_ios = input("\nPlot the investment opportunity set? [Y/n] ")
    if plot_ios not in ("n", "N"):
        table = portfolio_table(exp_ret, std_dev, cov)
        plt.xlabel("Risk (standard deviation)")
        plt.ylabel("Return (expected return)")
        plt.scatter(table["std_dev"], table["exp_ret"], s=2, c="slategray")
        plt.scatter(
            std_dev_mvp,
            exp_ret_mvp,
            s=60,
            c="red",
            label="Minimum-variance portfolio",
        )
        plt.scatter(
            std_dev_omp, exp_ret_omp, s=40, c="green", label="Tangency portfolio"
        )
        plt.scatter(
            table["std_dev"].tail(1),
            table["exp_ret"].tail(1),
            s=100,
            c="black",
            marker="1",
            label=exp_ret.index[0],
        )
        plt.scatter(
            table["std_dev"].head(1),
            table["exp_ret"].head(1),
            s=100,
            c="black",
            marker="2",
            label=exp_ret.index[1],
        )
        plt.legend()
        plt.grid()
        plt.show()
        plt.close()

    input("\nProgram finished ")


if __name__ == "__main__":
    main()
