By [Marcelo Moreno](https://www.linkedin.com/in/marcelomorenop/) and [Yago Cano](https://www.linkedin.com/in/yagocano/), from King Juan Carlos University.

# Two stocks portfolio analysis with Python

Two stocks minimum variance portfolio and optimum market portfolio analysis with Python using Harry Max Markowitz modern 
portfolio theory.

Libraries used for the project:
* [yfinance](https://pypi.org/project/yfinance/)
* [numpy](https://numpy.org/)
* [pandas](https://pandas.pydata.org/)
* [matplotlib](https://matplotlib.org/)

## Usage

1. Make sure to have installed the last version of all the libraries above.
2. Download and execute the `two_stocks_portfolio.py` file with Python (versions equal or above 3.8 are recommended).
3. First, the program will ask to introduce the ticker symbol of the 1st of the two stocks that the portfolio will be 
composed of. Introduce it and press `Enter`.
4. Secondly, the program will ask to introduce the ticker symbol of the 1st of the two stocks that the portfolio will be 
composed of. Introduce it and press `Enter`.
5. Then, the program will automatically download data from the risk-free asset and start the calculations.
6. When the calculations are complete, the program will prompt to press `Enter` to show results. Press it. Per stock and
portfolio stats will be displayed.
7. Finally, the program will ask for a graphic representation of the portfolios in the return-risk space.
Press `Y` to proceed, or `N` to finish the program.
8. If graphic representation is selected, a matplotlib window will automatically appear with the plot. Here you
can zoom in, out, save the plot as an image... with the matplotlib interface. When you are finished, close the
matplotlib window and the program will end.

By default, the program uses the time period of 1 year with 1 days intervals, the 'Close' price for its calculations, 
and the risk-free asset is 10 year US bond yield (^TNX).

## Example

Example using Advanced Micro Devices (AMD) and Tesla (TSLA) stocks:

```
TWO STOCKS PORTFOLIO ANALYSIS
-----------------------------

Ticker symbol stock 1: CDNS
[*********************100%***********************]  1 of 1 completed
Ticker symbol stock 2: FISV
[*********************100%***********************]  1 of 1 completed
Risk free asset: ^TNX (10 year US bond yield)
[*********************100%***********************]  1 of 1 completed

Calculation complete. Press Enter to show results

STOCK STATS
            CDNS  FISV
     Mean: 0.327 0.218
 Variance: 0.147 0.091
Std. Dev.: 0.384 0.302
 Covariance:  0.070983
Correlation:  0.612303

MINIMUM VARIANCE PORTFOLIO STATS
   % CDNS: 20.987
   % FISV: 79.013
     Mean:  0.241
 Variance:  0.087
Std. Dev.:  0.295
Sharpe ratio:  0.815

OPTIMUM MARKET PORTFOLIO STATS
   % CDNS: 61.936
   % FISV: 38.064
     Mean:  0.285
 Variance:  0.103
Std. Dev.:  0.321
Sharpe ratio:  0.888

Graphic representation? Y/[N]
```

If the response to ```Graphic representation?``` is ```Y```, then:
![Plot example](/example_images/Figure_1.png)

Lastly (have chosen ```N``` or closed the matplotlib window):

```
Program finished
```
