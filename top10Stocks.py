import math
import yfinance as yf
import pandas as pd
from scipy import stats
from statistics import mean
from datetime import datetime, timedelta


def fetchSnP500Tickers():
    table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    table = table.rename({"Symbol": "Ticker"}, axis='columns')
    return table

def getTopTenStocks(tickers):
	output = ['Ticker',
	    'Price',
	    'Price-to-Earnings Ratio',
	    'Price-to-Earnings Percentile',
	    'Price-to-Book Ratio',
	    'Price-to-Book Percentile',
	    'Enterprise to EBITDA Ratio',
	    'Enterprise to EBITDA Percentile',
	    'Enterprise to Revenue',
	    'Enterprise to Revenue Percentile',
	    'Score'
    ]

	output = pd.DataFrame(columns = output)

	for ticker in tickers[:50]:
	  stock = yf.Ticker(ticker)
	  previousValue = stock.info.get('previousClose', 0)
	  PERatio = stock.info.get('forwardPE', 0)
	  PBRatio = stock.info.get('priceToBook', 0)
	  enterpriseToEbitda = stock.info.get('enterpriseToEbitda', 0)
	  enterpriseToRevenue = stock.info.get('enterpriseToRevenue', 0)
	  nextRow = {
	    'Ticker' : ticker,
	    'Price' : previousValue,
	    'Price-to-Earnings Ratio' : PERatio,
	    'Price-to-Earnings Percentile' : '0',
	    'Price-to-Book Ratio' : PBRatio,
	    'Price-to-Book Percentile' : '0',
	    'Enterprise to EBITDA Ratio' : enterpriseToEbitda,
	    'Enterprise to EBITDA Percentile' : '0',
	    'Enterprise to Revenue' : enterpriseToRevenue,
	    'Enterprise to Revenue Percentile' : '0',
	    'Score' : '0'
	  }
	  output.loc[len(output)] = nextRow;


	metrics = {
	    'Price-to-Earnings Ratio' : 'Price-to-Earnings Percentile',
	    'Price-to-Book Ratio' : 'Price-to-Book Percentile',
	    'Enterprise to EBITDA Ratio' : 'Enterprise to EBITDA Percentile',
	    'Enterprise to Revenue' : 'Enterprise to Revenue Percentile',
	}

	for row in output.index:
	    for metric in metrics.keys():
	        output.loc[row, metrics[metric]] = stats.percentileofscore(output[metric], output.loc[row, metric])/100

	mask = (output['Price-to-Earnings Percentile'] < 0.50) & (output['Price-to-Book Percentile'] < 0.50) & (output['Enterprise to EBITDA Percentile'] < 0.50) & (output['Enterprise to Revenue Percentile'] < 0.50)
	filteredOutput = output[mask]

	for row in filteredOutput.index:
	    value_percentiles = []
	    for metric in metrics.keys():
	        value_percentiles.append(filteredOutput.loc[row, metrics[metric]])
	    filteredOutput.loc[row, 'Score'] = mean(value_percentiles)

	filteredOutput.sort_values(by = 'Score', inplace = True)
	topTenStocks = filteredOutput[:10]
	topTenStocks.reset_index(drop = True, inplace = True)
	print(topTenStocks[['Ticker', 'Price']])

def main():
    snp500 = fetchSnP500Tickers()
    getTopTenStocks(snp500['Ticker'].tolist())


if __name__ == "__main__":
    main()
