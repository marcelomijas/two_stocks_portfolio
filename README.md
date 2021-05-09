# Minimum variance and market optimal portfolio with Python

Minimum variance portfolio and market optimal portfolio finder using the packages:
- yfinance
- numpy
- pandas
- matplotlib

Right now is only available for Python IDEs, planning to release on Windows and Linux.

Formula for the minimum variance portfolio (using Markowitz model):

<img src="https://render.githubusercontent.com/render/math?math=W^*_{sk1}=\frac{\sigma^2_{sk2}-cov(sk1,sk2)}{\sigma^2_{sk1} %2B \sigma^2_{sk2} - 2 \times cov(sk1,sk2)}">

<img src="https://render.githubusercontent.com/render/math?math=W^*_{sk2}=1-W^*_{sk1}">

### Roadmap

:earth_americas::wavy_dash::rocket::wavy_dash::wavy_dash::wavy_dash::wavy_dash::wavy_dash::wavy_dash::wavy_dash::new_moon: v1.0.0

:heavy_check_mark: Proof of Concept (basic functionality)

:heavy_check_mark: Minimum variance portfolio with two stocks

:construction: Optimal market portfolio with two stocks

:construction: Add more statistics and data to display: beta, sharpe ratio, etc.

:construction: More object oriented programming (class) code

:construction: Web interface, replacing matplotlib with plotly

:construction: Custom time interval and frequency selection (by default: int: 1y, freq: 1d)

## Version 0.1.0 - Released 2021-05-09

New features:
* Working minimum variance portfolio with two stocks (mvp.py)
