import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf

# ABBREVIATIONS
# corr = correlation
# cov = covariance
# mean = mean
# mvp = minimum variance portfolio
# omp = optimum market portfolio
# pc = per cent
# rf = risk free
# sd = standard deviation
# sr = sharpe ratio
# stk = stock
# ts = ticker symbol
# var = variance
# w = weight


def download_stk(ts):
    if ts == "":
        print("No ticker symbol entered\nProgram finished")
        exit()
    stk = yf.download(tickers=ts, period="1y", interval="1d")[:252]["Close"]
    return stk


def stk_stats(stk):
    stk_pc = stk.pct_change()[1:]
    # 252 = days of one trading year
    mean = stk_pc.mean() * 252  # yearly mean (return)
    var = stk_pc.var() * 252  # yearly variance
    sd = np.sqrt(var)  # yearly standard deviation (risk)
    return mean, var, sd


def two_stk_stats(stk_1, stk_2):
    stk_1_pc = stk_1.pct_change()[1:]
    stk_2_pc = stk_2.pct_change()[1:]
    cov = np.cov(stk_1_pc, stk_2_pc)[0, 1] * 252
    corr = np.corrcoef(stk_1_pc, stk_2_pc)[0, 1]
    return cov, corr


print("\nTWO STOCKS PORTFOLIO ANALYSIS\n", "-" * 29, "\n", sep="")

# stock 1
ts_1 = input("Ticker symbol stock 1: ")
stk_1 = download_stk(ts_1)
mean_1, var_1, sd_1 = stk_stats(stk_1)

# stock 2
ts_2 = input("Ticker symbol stock 2: ")
stk_2 = download_stk(ts_2)
mean_2, var_2, sd_2 = stk_stats(stk_2)

cov, corr = two_stk_stats(stk_1, stk_2)

# risk free asset
ts_rf = "^TNX"
print("Risk free asset: {} (10 year US bond yield)".format(ts_rf))
rf = download_stk(ts_rf)
mean_rf = rf.pct_change()[1:].mean() / 10  # yearly

# portfolio table
step = 0.001
df_pt = pd.DataFrame({"w_1": np.arange(0, 1 + step, step).tolist()})
df_pt["mean"] = df_pt["w_1"] * mean_1 + (1 - df_pt["w_1"]) * mean_2
df_pt["var"] = (
    (df_pt["w_1"] ** 2) * var_1
    + ((1 - df_pt["w_1"]) ** 2) * var_2
    + 2 * (df_pt["w_1"] * (1 - df_pt["w_1"]) * cov)
)
df_pt["sd"] = np.sqrt(df_pt["var"])

# minimum variance portfolio
w_1_mvp = (var_2 - cov) / (var_1 + var_2 - 2 * cov)
if w_1_mvp > 1:
    w_1_mvp = 1
elif w_1_mvp < 0:
    w_1_mvp = 0
w_2_mvp = 1 - w_1_mvp

# minimum variance portfolio stats
mean_mvp = w_1_mvp * mean_1 + w_2_mvp * mean_2
var_mvp = (w_1_mvp**2) * var_1 + (w_2_mvp**2) * var_2 + 2 * w_1_mvp * w_2_mvp * cov
sd_mvp = np.sqrt(var_mvp)
sr_mvp = (mean_mvp - mean_rf) / sd_mvp

# optimum market portfolio
w_1_omp = ((mean_1 - mean_rf) * var_2 - (mean_2 - mean_rf) * cov) / (
    (mean_2 - mean_rf) * var_1
    + (mean_1 - mean_rf) * var_2
    - (mean_1 + mean_2 - 2 * mean_rf) * cov
)
if w_1_omp > 1:
    w_1_omp = 1
elif w_1_omp < 0:
    w_1_omp = 0
w_2_omp = 1 - w_1_omp

# optimum market portfolio stats
mean_omp = w_1_omp * mean_1 + w_2_omp * mean_2
var_omp = (w_1_omp**2) * var_1 + (w_2_omp**2) * var_2 + 2 * w_1_omp * w_2_omp * cov
sd_omp = np.sqrt(var_omp)
sr_omp = (mean_omp - mean_rf) / sd_omp

input("\nCalculation complete. Press Enter to show results ")

print("\nSTOCK STATS")
df = pd.DataFrame(
    {
        "": ["Mean:", "Variance:", "Std. Dev.:"],
        ts_1: [mean_1, var_1, sd_1],
        ts_2: [mean_2, var_2, sd_2],
    }
)
df[ts_1] = df[ts_1].round(3)
df[ts_2] = df[ts_2].round(3)
print(df.to_string(index=False))
print(" Covariance: ", cov.round(6))
print("Correlation: ", corr.round(6))

print("\nMINIMUM VARIANCE PORTFOLIO STATS")
df = pd.DataFrame(
    {
        "tags": [
            "% {}:".format(ts_1),
            "% {}:".format(ts_2),
            "Mean:",
            "Variance:",
            "Std. Dev.:",
        ],
        "data": [
            w_1_mvp * 100,
            w_2_mvp * 100,
            mean_mvp,
            var_mvp,
            sd_mvp,
        ],
    }
)
df["data"] = df["data"].round(3)
print(df.to_string(index=False, header=False))
print("Sharpe ratio: ", round(sr_mvp, 3))

print("\nOPTIMUM MARKET PORTFOLIO STATS")
df = pd.DataFrame(
    {
        "tags": [
            "% {}:".format(ts_1),
            "% {}:".format(ts_2),
            "Mean:",
            "Variance:",
            "Std. Dev.:",
        ],
        "data": [
            w_1_omp * 100,
            w_2_omp * 100,
            mean_omp,
            var_omp,
            sd_omp,
        ],
    }
)
df["data"] = df["data"].round(3)
print(df.to_string(index=False, header=False))
print("Sharpe ratio: ", round(sr_omp, 3))


graph = input("\nGraphic representation? Y/[N] ")

if graph == "Y" or graph == "y":
    plt.xlabel("Risk (standard deviation)")
    plt.ylabel("Return (mean)")
    plt.scatter(df_pt["sd"], df_pt["mean"], s=2, c="slategray")
    plt.scatter(sd_mvp, mean_mvp, s=60, c="red", label="Minimum Variance Portfolio")
    plt.scatter(sd_omp, mean_omp, s=60, c="green", label="Optimum Market Portfolio")
    plt.scatter(
        df_pt["sd"].tail(1),
        df_pt["mean"].tail(1),
        s=100,
        c="black",
        marker="2",
        label=ts_1,
    )
    plt.scatter(
        df_pt["sd"].head(1),
        df_pt["mean"].head(1),
        s=100,
        c="black",
        marker="1",
        label=ts_2,
    )
    plt.legend()
    plt.grid()
    plt.show()
    plt.close()

print("\nProgram finished")
