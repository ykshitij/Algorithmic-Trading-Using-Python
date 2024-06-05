# Algorithmic-Trading-Using-Python
Fundamental financial indicators to get the top 10 stocks

Quantitative Value Investment Strategy
Value Investment Strategies typically focus on stocks that are trading at a lower value as compared to their intrinsic value. They look for companies with strong fundamentals, such as low price-to-earnings (P/E) ratios, low price-to-book (P/B) ratios, high dividend yields, and other metrics that suggest the stock is fundamentally strong. 

In this project, we selected the top 10 fundamentally strong stocks from the S&P 500 list. We used yahoo finance APIs, to extract the stock data. We focused on four different parameters : 
1. Price To Earnings Ratio
2. Price To Book Ratio
3. Enterprise To EBITDA Ratio
4. Enterprise To Revenue Ratio

The lower the parameter values, the better performing stock. 
We then calculated the percentile values according to these four parameters, and selected all stocks which have a percentile value of less that 0.5 for all four parameters. We the calculated the mean value for all four percentile values and selected the ten least mean values. 
