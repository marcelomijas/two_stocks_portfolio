# Two stocks minimum variance portfolio and optimum market portfolio with Python

Two stocks minimum variance portfolio and optimum market portfolio two-asset allocator with Python using Harry Max Markowitz modern portfolio theory. 

Libraries used:
* [yfinance](https://pypi.org/project/yfinance/)
* [numpy](https://numpy.org/)
* [pandas](https://pandas.pydata.org/)
* [matplotlib](https://matplotlib.org/)

## Instructions of use

1. Make sure to have installed the last version of all the libraries above.
2. Download and execute the "two\_stocks\_portfolio.py" file with Python 3+.
3. First, the program will ask you to introduce the ticker of the 1st of the two stocks that you want to create the
portfolio with. Introduce it and press Enter.
4. Then, the program will ask you to introduce the ticker of the 2nd of the two stocks that you want to create the
portfolio with. Introduce it and press Enter.
5. The program will automatically download data from the risk-free asset (10 year US bond yield)
and start the calculations.
6. When the calculations are complete, the program will prompt to press Enter to show results. Press it. Per stock and
portfolio stats will be presented.
7. Finally, the program will ask you if you want a graphic representation of the portfolios in the return-risk space.
Press 'Y' to proceed, or 'N' to finish the program.
8. If you proceed with the graphic representation, a matplotlib window will automatically appear with the plot. Here you
can zoom in, out, save as an image... with the matplotlib interface. When you are finnished, close the matplotlib window
and the program will end.

## Example

Output example using BlackBerry Limited (BB) and Advanced Micro Devices (AMD) stocks:
![Stats example](https://github.com/marcelomijas/two_stock_portfolio/tree/main/example_images/stats.png?raw=true)

![Plot example](https://github.com/marcelomijas/two_stock_portfolio/tree/main/example_images/plot.png?raw=true)
