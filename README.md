# Minimum variance and market optimal portfolio with Python

Minimum variance portfolio and market optimal portfolio finder using the packages:
- yfinance
- numpy
- pandas
- matplotlib

Right now is only available for Python IDEs, planning to release on Windows and Linux.

Formula for the minimum variance portfolio (using Markowitz model):

<img src="https://render.githubusercontent.com/render/math?math=W^*_{stock 1}=\frac{\sigma^2_{stock 2}-cov(sk1,sk2)}{\sigma^2_{stock 1} %2B \sigma^2_{stock 2} - 2 \times cov(stock 1, stock 2)}">

<img src="https://render.githubusercontent.com/render/math?math=W^*_{stock 2}=1-W^*_{stock 1}">

(<img src="https://render.githubusercontent.com/render/math?math=W^*_{i}="> stock i minimum variance portfolio ponderation (i = 1, 2).

### Roadmap

:earth_americas::wavy_dash::wavy_dash::wavy_dash::rocket::wavy_dash::wavy_dash::wavy_dash::wavy_dash::wavy_dash::new_moon: v1.0.0

:heavy_check_mark: Proof of Concept (basic functionality)

:heavy_check_mark: Minimum variance portfolio with two stocks

:construction: Optimal market portfolio with two stocks

:construction: Add more statistics and data to display: beta, sharpe ratio, etc.

:construction: Web interface, replacing matplotlib with plotly

:construction: Custom time interval and frequency selection (by default: int: 1y, freq: 1d)

## Version release history

### Version 0.2.0 - Released 2021-05-15

Now the Minimum Variance Portfolio with 2 stocks (minimum_variance_portfolio_2stocks.py) is fully functional.

Additions:
* Creation of a Market Optimum Portfolio with 2 stocks (market_optimum_portfolio_2stocks.py) file to start a proof of concept in the following days.

New features:
* New results appearance.
* Additional step to show results.
* Function definition.
* Code reorganization.

Bug fixes:
* The graphic representation option now accepts 'Y', 'YES', 'y' and 'yes' values.

### Version 0.1.0 - Released 2021-05-09

New features:
* Working minimum variance portfolio with two stocks (mvp.py).
