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
2. Download and execute the "two\_stocks\_portfolio.py" file with Python (versions equal or above 3.8 are recommended).
3. First, the program will ask to introduce the ticker symbol of the 1st of the two stocks that the portfolio will be 
composed of. Introduce it and press Enter.
4. Secondly, the program will ask to introduce the ticker symbol of the 1st of the two stocks that the portfolio will be 
composed of. Introduce it and press Enter.
5. Then, the program will automatically download data from the risk-free asset and start the calculations.
6. When the calculations are complete, the program will prompt to press Enter to show results. Press it. Per stock and
portfolio stats will be presented.
7. Finally, the program will ask for a graphic representation of the portfolios in the return-risk space.
Press 'Y' to proceed, or 'N' to finish the program.
8. If graphic representation is selected, a matplotlib window will automatically appear with the plot. Here you
can zoom in, out, save the plot as an image... with the matplotlib interface. When you are finished, close the
matplotlib window and the program will end.

By default, the program uses the time period of 1 year with 1 days intervals, the 'Close' price for its calculations, 
and the risk-free asset is 10 year US bond yield (^TNX).

## Example

Use example using Advanced Micro Devices (AMD) and BlackBerry Limited (BB) stocks:

```
+---------------------------------+
|  TWO STOCKS PORTFOLIO ANALYSIS  |
+---------------------------------+

Ticker symbol stock 1: AMD
[*********************100%***********************]  1 of 1 completed
Ticker symbol stock 2: BB
[*********************100%***********************]  1 of 1 completed
Risk free asset: ^TNX (10 year US bond yield, annualized)
[*********************100%***********************]  1 of 1 completed

Calculation complete. Press Enter to show results 

PER STOCK STATS
---------------
             AMD    BB
     Mean: 0.407 1.339
 Variance: 0.158 1.089
Std. Dev.: 0.398 1.044
 Covariance:  0.042684
Correlation:  0.102864

MINIMUM VARIANCE PORTFOLIO STATS
--------------------------------
 Pct. AMD: 90.062
  Pct. BB:  9.938
     Mean:  0.500
 Variance:  0.147
Std. Dev.:  0.383
Sharpe ratio:  1.304

OPTIMUM MARKET PORTFOLIO STATS
------------------------------
 Pct. AMD: 66.526
  Pct. BB: 33.474
     Mean:  0.719
 Variance:  0.211
Std. Dev.:  0.459
Sharpe ratio:  1.565

Graphic representation? Y/[N]  
```

If the response to ```Graphic representation?``` is ```Y```, then:
![Plot example](/example_images/plot.png)

Lastly (have chosen ```N``` or closed the matplotlib window):

```
Process finished
```