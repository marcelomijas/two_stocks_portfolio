# Two stocks portfolio analysis with Python

Simple two stocks minimum-variance portfolio and tangency (optimal) portfolio analysis with Python using Harry Max Markowitz modern 
portfolio theory.

Created by [Marcelo Moreno](https://www.linkedin.com/in/marcelomorenop/) and [Yago Cano](https://www.linkedin.com/in/yagocano/), from Universidad Rey Juan Carlos.

## Usage

1. Make sure you have installed the packages located in `requirements.txt`.
2. Download and execute `main.py` with Python.
3. The program will ask you to introduce the ticker symbol of the first asset of the portfolio. Introduce it and press `Enter`. Repeat the procedure for the second asset.
4. The program will download data from the two assets introduced and the risk-free asset.
6. When the downloads are complete, the program will prompt you to press `Enter` to perform the calculations. Press it.
7. Per asset and portfolios statistics will be displayed.
7. The program will ask you to proceed with the investment oportunity set graphic representation in the return-risk space.
8. If graphic representation is selected, a matplotlib window will appear with the plot. You can zoom in, out, save the plot as an image... using the matplotlib interface. Close the matplotlib window when you are finished.
9. To finnish the program you can press `Enter` or close the terminal window.

By default, the program uses a time period of 5 year with 1 month intervals, the 'Close' price, 
and the risk-free asset is 10 year US bond yield (^TNX). Statistics are calculated as montly.

## Example

Example using the Motorola Solutions, Inc. (MSI) and Broadcom Inc. (AVGO) stocks:

```
 ______                    __           __
/_  __/    _____      ___ / /____  ____/ /__ ___
 / / | |/|/ / _ \    (_-</ __/ _ \/ __/  '_/(_-<
/_/  |__,__/\___/ __/___/\__/\___/\__/_/\_\/___/
   ___  ___  ____/ /_/ _/__  / (_)__
  / _ \/ _ \/ __/ __/ _/ _ \/ / / _ \
 / .__/\___/_/  \__/_/ \___/_/_/\___/
/_/
Statistics are calculated as monthly

Ticker symbol of asset 1: MSI
         Motorola Solutions, Inc.
Ticker symbol of asset 2: AVGO
         Broadcom Inc.
Downloading assets: ['AVGO', 'MSI']
[*********************100%%**********************]  2 of 2 completed
Risk-free asset: ^TNX
         CBOE Interest Rate 10 Year T No
Download complete. Press Enter to perform calculations 
```

Pressing `Enter`

```
 ______                    __           __
/_  __/    _____      ___ / /____  ____/ /__ ___
 / / | |/|/ / _ \    (_-</ __/ _ \/ __/  '_/(_-<
/_/  |__,__/\___/ __/___/\__/\___/\__/_/\_\/___/
   ___  ___  ____/ /_/ _/__  / (_)__
  / _ \/ _ \/ __/ __/ _/ _ \/ / / _ \
 / .__/\___/_/  \__/_/ \___/_/_/\___/
/_/
Statistics are calculated as monthly

rf = 0.03

Performance statistics:
Ticker   AVGO    MSI
avg     2.858  1.772
stdev   9.211  6.964
Sharpe  0.306  0.249
covar  30.998
correl 0.483

Minimum-variance portfolio:
Ticker    AVGO    MSI
weigths  0.245  0.755
avg    2.038
stdev  6.649
Sharpe 0.301

Tangency portfolio:
Ticker    AVGO    MSI
weigths  0.581  0.419
avg    2.403
stdev  7.229
Sharpe 0.328

Plot the investment opportunity set? [Y/n]
```

If the answer is ```Y```, then:

![Plot example](/demo/Figure_1.png)

Lastly (having chosen ```N``` or closed the matplotlib window):

```
Program finished
```

## Resources

[1] Bodie, Z., Kane, A., & Marcus, A. J. (2014). Investments (Tenth edition). McGraw-Hill Education.

[2] Harris, C. R., Millman, K. J., Walt, S. J. et al. (2020). Array programming with NumPy. Nature, 585(7825), 357-362. https://doi.org/10.1038/s41586-020-2649-2

[3] Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. Computing in Science & Engineering, 9(3), 90-95. https://doi.org/10.1109/MCSE.2007.55

[4] Markowitz, H. (1952a). Portfolio selection*. The Journal of Finance, 7(1), 77-91. https://doi.org/10.1111/j.1540-6261.1952.tb01525.x

[5] Markowitz, H. (1952b). The utility of wealth. Journal of Political Economy, 60(2), 151-158. https://www.jstor.org/stable/1825964

[6] Markowitz, H. M. (1959). Portfolio selection: Efficient diversification of investments. Yale University Press. https://www.jstor.org/stable/j.ctt1bh4c8h

[7] The pandas development team. (2020). Pandas-dev/pandas: Pandas (latest) [Software]. Zenodo. https://doi.org/10.5281/zenodo.3509134

[8] yfinance: Download market data from yahoo! Finance api. (s. f.). [Python; OS Independent]. Retrieved March 30 of 2024, from https://github.com/ranaroussi/yfinance
