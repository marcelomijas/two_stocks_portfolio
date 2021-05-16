# Minimum variance and market optimal portfolio with Python

Minimum Variance Portfolio and Optimum Market Portfolio asset allocator with Python using:
* yfinance
* numpy
* pandas
* matplotlib

Right now is only available for Python IDEs, planning to release on Windows and Linux.

### Roadmap

:earth_americas::wavy_dash::wavy_dash::wavy_dash::wavy_dash::rocket::wavy_dash::wavy_dash::wavy_dash::wavy_dash::new_moon: v1.0.0

:heavy_check_mark: Proof of Concept (basic functionality)

:heavy_check_mark: Minimum Variance Portfolio with two stocks

:heavy_check_mark: Optimum Market Portfolio with two stocks

:construction: Add more statistics and data to display: beta, sharpe ratio, etc.

:construction: Add export option

:construction: Web interface, replacing matplotlib with plotly

:construction: Custom time interval and frequency selection (by default: int: 1y, freq: 1d)

:construction: Possibility to go with more than two stocks

## Version release history

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
