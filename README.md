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
            FISV  CDNS
     Mean: 0.267 0.394
 Variance: 0.088 0.127
Std. Dev.: 0.297 0.357
 Covariance:  0.060119
Correlation:  0.567701

MINIMUM VARIANCE PORTFOLIO STATS
   % FISV: 70.505
   % CDNS: 29.495
     Mean:  0.304
 Variance:  0.080
Std. Dev.:  0.283
Sharpe ratio:  1.076

OPTIMUM MARKET PORTFOLIO STATS
   % FISV: 35.265
   % CDNS: 64.735
     Mean:  0.349
 Variance:  0.092
Std. Dev.:  0.303
Sharpe ratio:  1.153

Graphic representation? Y/[N]
```

If the response to ```Graphic representation?``` is ```Y```, then:
![Plot example](/example_images/Figure_1.png)

Lastly (have chosen ```N``` or closed the matplotlib window):

```
Program finished
```
