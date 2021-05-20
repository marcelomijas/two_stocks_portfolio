# Minimum Variance Portfolio and Optimum Market Portfolio with Python

Minimum Variance Portfolio and Optimum Market Portfolio asset allocator with Python using:
* yfinance
* numpy
* pandas
* matplotlib

Right now is only available for Python IDEs, planning to release on Windows and Linux.

### Roadmap

:heavy_check_mark: Proof of Concept (basic functionality)

:heavy_check_mark: Minimum Variance Portfolio with two stocks

:heavy_check_mark: Optimum Market Portfolio with two stocks

:construction: Add more statistics and data to display: beta, sharpe ratio, etc.

:construction: Add export option

:construction: Web interface, replacing matplotlib with plotly

:construction: Custom time interval and frequency selection (by default: int: 1y, freq: 1d)

:construction: Possibility to go with more than two stocks

## Version release history

### Version 0.4.0 - Released 2021-05-20

Unified version of minimum variance portfolio and optimum market portfolio.

Improvements:
* Chart xmin and ymax update.

### Version 0.3.2 - Released 2021-05-18

New features:
* The graphic representation now shows where is located the 100% of each stock.

Improvements:
* Number of functions reduced.
* More understandable code and portfolio formulas.
* Graphic representation branding.

Bug fixes:
* Now the covariance stat is adapted to the trading year (*253).

### Version 0.3.1 - Released 2021-05-17

Changes:
* Plot color change.

### Version 0.3.0 - Released 2021-05-16

Now the Optimum Market Portfolio with 2 stocks is fully functional.

Changes:
* Plot color change.
* The plot now uses a tight layout.

New features:
* Added Sharpe ratio to the Optimum Market Portfolio stats.

Bug fixes:
* The graph grid is now below the plot.

### Version 0.2.0 - Released 2021-05-14

Now the Minimum Variance Portfolio with 2 stocks is fully functional.

Additions:
* Creation of an Optimum Market Portfolio with 2 stocks file to start a PoC in the following days.

New features:
* New results appearance.
* Additional step to show results.
* Function definition.
* Code reorganization.

Bug fixes:
* The graphic representation option now accepts 'Y', 'YES', 'y' and 'yes' values.

### Version 0.1.0 - Released 2021-05-09

New features:
* Working minimum variance portfolio with two stocks.
